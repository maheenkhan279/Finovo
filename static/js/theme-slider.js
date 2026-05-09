/* ===================================================================
   FINOVO - Universal slider initializer (theme-slider.js)
   - Updates the --fv-fill CSS variable so the track shows progress
   - Auto-binds amount displays for sliders that follow the
     "#xxxSlider" -> "#xxxAmount" naming convention (this fixes the
     orphaned sliders in budget_balancer_interactive.html and similar
     pages that have <input type="range"> with no event handlers)
   - Also exposes window.FinovoSlider for explicit registration
   =================================================================== */
(function () {
    "use strict";

    function pct(slider) {
        var min = parseFloat(slider.min || "0");
        var max = parseFloat(slider.max || "100");
        var val = parseFloat(slider.value || "0");
        if (!isFinite(min) || !isFinite(max) || max === min) return 0;
        return Math.max(0, Math.min(100, ((val - min) / (max - min)) * 100));
    }

    function paint(slider) {
        slider.style.setProperty("--fv-fill", pct(slider) + "%");
    }

    function formatMoney(n) {
        var num = Number(n);
        if (!isFinite(num)) return n;
        try {
            return "$" + num.toLocaleString();
        } catch (e) {
            return "$" + num;
        }
    }

    /**
     * Find a "display element" for a slider by convention:
     *   <input id="housingSlider"> -> #housingAmount, #housingValue, #housing-display
     * Returns null if none found.
     */
    function findDisplayFor(slider) {
        var id = slider.id || "";
        if (!id) return null;
        var base = id.replace(/Slider$/i, "").replace(/-slider$/i, "").replace(/_slider$/i, "");
        if (!base) return null;
        var candidates = [
            base + "Amount",
            base + "Value",
            base + "Display",
            base + "-amount",
            base + "-value",
            base + "-display",
            base + "_amount",
            base + "_value"
        ];
        for (var i = 0; i < candidates.length; i++) {
            var el = document.getElementById(candidates[i]);
            if (el) return el;
        }
        return null;
    }

    /**
     * Decide whether this slider already has an explicit handler.
     * If it does, we still set --fv-fill but do NOT touch its display.
     */
    function hasExplicitHandler(slider) {
        if (slider.getAttribute("oninput") || slider.getAttribute("onchange") || slider.getAttribute("onmousemove")) {
            return true;
        }
        if (slider.classList.contains("fv-slider-no-autoupdate")) return true;
        return false;
    }

    function initOne(slider) {
        if (slider.dataset.fvSlider === "init") return;
        slider.dataset.fvSlider = "init";

        var displayEl = findDisplayFor(slider);
        var displayMode = "money";
        if (displayEl && displayEl.dataset && displayEl.dataset.fvFormat) {
            displayMode = displayEl.dataset.fvFormat;
        } else if (slider.dataset && slider.dataset.fvFormat) {
            displayMode = slider.dataset.fvFormat;
        }

        paint(slider);

        var explicit = hasExplicitHandler(slider);

        // Opt-in sibling display for percentage-of-max. Pages that need a
        // different percentage formula (e.g. value/income) should NOT add
        // data-fv-percent and instead handle it themselves.
        var pctEl = null;
        if (slider.dataset && slider.dataset.fvPercent === "max" && slider.id) {
            var base2 = slider.id.replace(/Slider$/i, "").replace(/-slider$/i, "").replace(/_slider$/i, "");
            if (base2) {
                pctEl =
                    document.getElementById(base2 + "Percentage") ||
                    document.getElementById(base2 + "Percent") ||
                    document.getElementById(base2 + "-percent");
            }
        }

        function onMove() {
            paint(slider);
            if (!explicit && displayEl) {
                var v = slider.value;
                if (displayMode === "money") {
                    displayEl.textContent = formatMoney(v);
                } else if (displayMode === "percent") {
                    displayEl.textContent = v + "%";
                } else {
                    displayEl.textContent = String(v);
                }
            }
            if (!explicit && pctEl) {
                pctEl.textContent = Math.round(pct(slider)) + "%";
            }
        }

        slider.addEventListener("input", onMove, { passive: true });
        slider.addEventListener("change", onMove, { passive: true });
    }

    function scan(root) {
        var ctx = root || document;
        var sliders = ctx.querySelectorAll("input[type=\"range\"]");
        sliders.forEach(initOne);
        return sliders.length;
    }

    function bootstrap() {
        scan(document);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", bootstrap);
    } else {
        bootstrap();
    }

    // Watch dynamically-added sliders (e.g. retirement_road / portfolio_diversifier
    // build sliders via JS templates).
    if ("MutationObserver" in window) {
        var mo = new MutationObserver(function (muts) {
            for (var i = 0; i < muts.length; i++) {
                var nodes = muts[i].addedNodes;
                for (var j = 0; j < nodes.length; j++) {
                    var n = nodes[j];
                    if (!n || n.nodeType !== 1) continue;
                    if (n.matches && n.matches("input[type=\"range\"]")) {
                        initOne(n);
                    }
                    if (n.querySelectorAll) {
                        n.querySelectorAll("input[type=\"range\"]").forEach(initOne);
                    }
                }
            }
        });
        try {
            mo.observe(document.body || document.documentElement, { childList: true, subtree: true });
        } catch (e) { /* ignore */ }
    }

    window.FinovoSlider = {
        rescan: scan,
        repaint: function (slider) { if (slider) paint(slider); }
    };
})();
