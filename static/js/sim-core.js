/**
 * Finovo shared simulation helpers (non-breaking, optional use per game).
 */
(function (global) {
  "use strict";

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function setProgressBar(fillEl, pct) {
    if (!fillEl) return;
    fillEl.style.width = clamp(pct, 0, 100) + "%";
  }

  function flashMessage(el, text, kind) {
    if (!el) return;
    el.textContent = text;
    el.className = "sim-feedback sim-feedback--" + (kind || "info");
    el.style.opacity = "1";
    clearTimeout(flashMessage._t);
    flashMessage._t = setTimeout(function () {
      el.style.opacity = "0.85";
    }, 2200);
  }

  function pickRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function saveProgressSafe(gameName, score, level) {
    var fn = typeof window.saveScore === "function" ? window.saveScore : window.saveGameProgress;
    if (typeof fn !== "function") return;
    try {
      if (fn === window.saveScore) fn(score, gameName, level || 1);
      else fn(gameName, score, level || 1);
    } catch (e) {
      console.warn("saveProgressSafe:", e);
    }
  }

  global.FinovoSim = {
    clamp: clamp,
    setProgressBar: setProgressBar,
    flashMessage: flashMessage,
    pickRandom: pickRandom,
    saveProgressSafe: saveProgressSafe,
  };
})(window);
