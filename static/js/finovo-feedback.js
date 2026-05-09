/**
 * Finovo — FAQ accordion + toast feedback (no dependency on game/auth internals).
 */
(function () {
    "use strict";

    var TOAST_ICONS = {
        success: "fa-circle-check",
        error: "fa-circle-exclamation",
        info: "fa-circle-info",
        warning: "fa-triangle-exclamation"
    };

    function ensureToastRoot() {
        var el = document.getElementById("fv-toast-root");
        if (!el) {
            el = document.createElement("div");
            el.id = "fv-toast-root";
            el.setAttribute("aria-live", "polite");
            document.body.appendChild(el);
        }
        return el;
    }

    function dismissToast(node, done) {
        if (!node || !node.parentNode) return;
        node.classList.remove("fv-toast--in");
        node.classList.add("fv-toast--out");
        setTimeout(function () {
            if (node.parentNode) node.parentNode.removeChild(node);
            if (typeof done === "function") done();
        }, 320);
    }

    /**
     * @param {string} message
     * @param {"success"|"error"|"info"|"warning"} type
     * @param {{ title?: string, duration?: number }} [opts]
     */
    function showToast(message, type, opts) {
        opts = opts || {};
        type = type || "info";
        var duration = typeof opts.duration === "number" ? opts.duration : 4200;
        var title = opts.title || "";

        var root = ensureToastRoot();
        var toast = document.createElement("div");
        toast.className = "fv-toast fv-toast--" + type;
        toast.setAttribute("role", "status");

        var iconName = TOAST_ICONS[type] || TOAST_ICONS.info;
        var icon = document.createElement("div");
        icon.className = "fv-toast__icon";
        icon.innerHTML = '<i class="fas ' + iconName + '" aria-hidden="true"></i>';

        var body = document.createElement("div");
        body.className = "fv-toast__body";
        if (title) {
            var t = document.createElement("p");
            t.className = "fv-toast__title";
            t.textContent = title;
            body.appendChild(t);
        }
        var p = document.createElement("p");
        p.className = "fv-toast__msg";
        p.textContent = message || "";
        body.appendChild(p);

        var close = document.createElement("button");
        close.type = "button";
        close.className = "fv-toast__close";
        close.setAttribute("aria-label", "Dismiss");
        close.innerHTML = "&times;";
        close.addEventListener("click", function () {
            dismissToast(toast);
        });

        toast.appendChild(icon);
        toast.appendChild(body);
        toast.appendChild(close);
        root.appendChild(toast);

        requestAnimationFrame(function () {
            toast.classList.add("fv-toast--in");
        });

        if (duration > 0) {
            setTimeout(function () {
                dismissToast(toast);
            }, duration);
        }
        return toast;
    }

    function pickGameFeedback(score, gameName) {
        var s = Number(score);
        if (isNaN(s)) s = 0;
        var g = (gameName || "Game").trim();
        var title = "Progress saved";
        var line = "Your score is on its way to your dashboard.";
        var tip = "Replay anytime to sharpen your skills — consistency builds confidence.";

        if (s >= 85) {
            title = "Outstanding work!";
            line = "Excellent financial decision making on " + g + ".";
            tip = "Try the next difficulty tier when you are ready for a new challenge.";
        } else if (s >= 65) {
            title = "Great job!";
            line = "Strong performance in " + g + ".";
            tip = "Review one concept you hesitated on, then run the scenario again.";
        } else if (s >= 40) {
            title = "Nice effort!";
            line = "You are building real financial literacy with " + g + ".";
            tip = "Read the in-game tips once more — small tweaks often unlock big gains.";
        } else {
            title = "Keep going!";
            line = "Every round in " + g + " builds muscle memory.";
            tip = "Focus on one learning goal per session — progress adds up fast.";
        }

        return { title: title, line: line, tip: tip };
    }

    function notifyGameProgressSaved(score, gameName) {
        var fb = pickGameFeedback(score, gameName);
        showToast(fb.line + " " + fb.tip, "success", {
            title: fb.title,
            duration: 5200
        });
    }

    function initFaqAccordion() {
        var items = document.querySelectorAll(".faq-section .faq-item");
        if (!items.length) return;

        items.forEach(function (item) {
            var q = item.querySelector(".faq-question");
            if (!q || q.dataset.fvFaqInit) return;
            q.dataset.fvFaqInit = "1";
            q.setAttribute("role", "button");
            q.setAttribute("tabindex", "0");
            q.setAttribute("aria-expanded", "false");

            function toggle() {
                var willOpen = !item.classList.contains("active");
                item.classList.toggle("active", willOpen);
                q.setAttribute("aria-expanded", willOpen ? "true" : "false");
            }

            q.addEventListener("click", function (e) {
                e.preventDefault();
                toggle();
            });
            q.addEventListener("keydown", function (e) {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    toggle();
                }
            });
        });
    }

    function migrateFlashToToasts() {
        var nodes = document.querySelectorAll("main .notification.show");
        if (!nodes.length) return;
        nodes.forEach(function (n) {
            var text = (n.textContent || "").replace(/\s+/g, " ").trim();
            if (!text) {
                n.remove();
                return;
            }
            var cls = n.className || "";
            var type = "info";
            if (/\berror\b/.test(cls)) type = "error";
            else if (/\bsuccess\b/.test(cls)) type = "success";
            else if (/\bwarning\b/.test(cls)) type = "warning";
            showToast(text, type, { duration: type === "error" ? 6500 : 5200 });
            n.remove();
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initFaqAccordion();
        migrateFlashToToasts();
    });

    window.FinovoToast = {
        show: showToast,
        success: function (msg, opts) {
            return showToast(msg, "success", opts);
        },
        error: function (msg, opts) {
            return showToast(msg, "error", opts);
        },
        info: function (msg, opts) {
            return showToast(msg, "info", opts);
        },
        warning: function (msg, opts) {
            return showToast(msg, "warning", opts);
        },
        notifyGameProgressSaved: notifyGameProgressSaved
    };

    window.FinovoFAQ = { init: initFaqAccordion };
})();
