#!/usr/bin/env python3
"""Generates the original hero artwork (assets/hero-art.svg). Deterministic."""
import random, math, pathlib
random.seed(732)
W, H = 1200, 900
AMBER, TEAL, CREAM, INK = "#f0a93b", "#74d3c4", "#f4f1e6", "#14130e"
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Abstract layered system diagram">',
 '''<style>
.t{fill:none;stroke:#f4f1e6;stroke-opacity:.28;stroke-width:1.5}
.f{fill:none;stroke-width:2.5;stroke-linecap:round;stroke-dasharray:14 220;animation:flow 7s linear infinite}
.l{font:500 15px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#f4f1e6;fill-opacity:.78;letter-spacing:.08em}
.p{animation:tw 5s ease-in-out infinite}
@keyframes flow{to{stroke-dashoffset:-468}}
@keyframes tw{50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.f,.p{animation:none}}
</style>''']
# dither field along a diagonal band
C = 14
for gy in range(0, H // C):
    for gx in range(0, W // C):
        x, y = gx * C, gy * C
        d = abs((x - 80) * 0.55 - (H - y) + 120) / 260
        pr = max(0, 0.42 - d * 0.42) * (0.5 + 0.5 * math.sin(gx * 0.31) * math.cos(gy * 0.23) + 0.35)
        if random.random() < pr:
            col = random.choices([AMBER, TEAL, CREAM], [5, 3, 2])[0]
            op = round(random.uniform(0.12, 0.7), 2)
            cls = ' class="p" style="animation-delay:-%.1fs"' % random.uniform(0, 5) if random.random() < 0.12 else ''
            o.append(f'<rect x="{x}" y="{y}" width="{C-3}" height="{C-3}" fill="{col}" opacity="{op}"{cls}/>')
# isometric slabs
def iso(cx, cy, w, d, h, col, label):
    a, b = w * 0.5, w * 0.25
    c2, d2 = d * 0.5, d * 0.25
    top = [(cx, cy - b - d2), (cx + a + c2 - c2, cy), (cx, cy + b + d2), (cx - a, cy)]
    top = [(cx, cy - b), (cx + a, cy), (cx, cy + b), (cx - a, cy)]
    pts = lambda P: " ".join(f"{x:.0f},{y:.0f}" for x, y in P)
    left = [top[3], top[2], (top[2][0], top[2][1] + h), (top[3][0], top[3][1] + h)]
    right = [top[2], top[1], (top[1][0], top[1][1] + h), (top[2][0], top[2][1] + h)]
    o.append(f'<polygon points="{pts(left)}" fill="{INK}" fill-opacity=".92" stroke="{col}" stroke-opacity=".55" stroke-width="1.5"/>')
    o.append(f'<polygon points="{pts(right)}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".55" stroke-width="1.5"/>')
    o.append(f'<polygon points="{pts(top)}" fill="{col}" fill-opacity=".22" stroke="{col}" stroke-width="1.5"/>')
    # grid on top
    for i in range(1, 4):
        t = i / 4
        x1, y1 = top[3][0] + (top[0][0] - top[3][0]) * t, top[3][1] + (top[0][1] - top[3][1]) * t
        x2, y2 = top[2][0] + (top[1][0] - top[2][0]) * t, top[2][1] + (top[1][1] - top[2][1]) * t
        o.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-opacity=".4"/>')
        x1, y1 = top[3][0] + (top[2][0] - top[3][0]) * t, top[3][1] + (top[2][1] - top[3][1]) * t
        x2, y2 = top[0][0] + (top[1][0] - top[0][0]) * t, top[0][1] + (top[1][1] - top[0][1]) * t
        o.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-opacity=".4"/>')
    o.append(f'<line x1="{top[1][0]:.0f}" y1="{top[1][1]+h/2:.0f}" x2="{top[1][0]+70:.0f}" y2="{top[1][1]+h/2:.0f}" stroke="{CREAM}" stroke-opacity=".45"/>')
    o.append(f'<text class="l" x="{top[1][0]+82:.0f}" y="{top[1][1]+h/2+5:.0f}">{label}</text>')
cx = 520
layers = [(640, "DATA", CREAM), (500, "MODELS", TEAL), (360, "ORCHESTRATION", AMBER), (220, "INTERFACE", CREAM)]
# vertical traces between layers (drawn first, behind slabs)
for dx in (-150, 0, 150):
    p = f"M{cx+dx} 690 V200"
    o.append(f'<path class="t" d="{p}"/>')
for cy, label, col in layers:
    iso(cx, cy, 520, 520, 34, col, label)
# flowing signals over the stack
for i, (dx, col) in enumerate(((-150, AMBER), (0, TEAL), (150, AMBER))):
    o.append(f'<path class="f" stroke="{col}" style="animation-delay:-{i*2.3}s" d="M{cx+dx} 690 V200"/>')
# nodes on top layer
for dx, dy in ((-150, 0), (0, 0), (150, 0), (0, -60), (0, 60)):
    o.append(f'<rect x="{cx+dx-7}" y="{220+dy-7}" width="14" height="14" fill="{AMBER if dx else TEAL}"/>')
o.append('</svg>')
pathlib.Path(__file__).resolve().parent.parent.joinpath("assets/hero-art.svg").write_text("\n".join(o))
