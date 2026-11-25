// Progressive enhancement only: content is fully visible without this file.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;
  var els = document.querySelectorAll('.sec-head, .plain, .card, .paper, .hist > div');
  document.documentElement.classList.add('js');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  els.forEach(function (el) {
    el.classList.add('reveal');
    if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('in');
    io.observe(el);
  });
})();
