// RAPID²AI — shared Atlas design-system behaviors: reveal-on-scroll,
// cascade stagger, tilt/sheen hover, and numeric count-up. Ported from the
// Atlas Command Center design handoff's interaction spec. Plain script,
// no build step — loaded alongside rapid-design.css.
(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function reveal() {
    document.querySelectorAll('[data-r-reveal], [data-r-cascade]').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.96) el.classList.add('is-visible');
    });
  }
  window.addEventListener('scroll', reveal, { passive: true });
  window.addEventListener('resize', reveal);
  document.addEventListener('DOMContentLoaded', reveal);
  setTimeout(reveal, 50);

  function countUp(el) {
    var raw = el.getAttribute('data-r-count') || el.textContent;
    var match = raw.match(/^(\D*)([\d,]+(?:\.\d+)?)(.*)$/);
    if (!match) return;
    var prefix = match[1];
    var numStr = match[2];
    var suffix = match[3];
    var hasComma = numStr.indexOf(',') !== -1;
    var target = parseFloat(numStr.replace(/,/g, ''));
    var decimals = (numStr.split('.')[1] || '').length;
    if (!isFinite(target)) return;

    if (reduceMotion) {
      el.textContent = raw;
      return;
    }

    var start = null;
    var dur = 900;
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min(1, (ts - start) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = target * eased;
      var text = decimals ? val.toFixed(decimals) : Math.round(val).toString();
      if (hasComma) {
        text = Number(text).toLocaleString('en-US', {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals,
        });
      }
      el.textContent = prefix + text + suffix;
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = raw;
    }
    requestAnimationFrame(frame);
  }
  function initCounts() {
    document.querySelectorAll('[data-r-count]').forEach(countUp);
  }
  document.addEventListener('DOMContentLoaded', initCounts);

  function initTilt() {
    if (reduceMotion) return;
    document.querySelectorAll('[data-r-tilt]').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform =
          'perspective(700px) rotateX(' + (py * -3.5).toFixed(2) + 'deg) rotateY(' + (px * 3.5).toFixed(2) + 'deg)';
        card.classList.add('sheen-on');
      });
      card.addEventListener('mouseleave', function () {
        card.style.transform = '';
        card.classList.remove('sheen-on');
      });
    });
  }
  document.addEventListener('DOMContentLoaded', initTilt);
})();
