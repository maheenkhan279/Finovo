/**
 * Client-side guard: dashboard and all /games/* require Supabase session.
 */
(function () {
  "use strict";

  function normalizedPath() {
    var p = window.location.pathname || "/";
    if (p.length > 1 && p.endsWith("/")) p = p.slice(0, -1);
    return p || "/";
  }

  function pathRequiresSupabaseAuth() {
    var p = normalizedPath();
    if (p === "/dashboard" || p === "/games") return true;
    if (p.indexOf("/games/") === 0) return true;
    return false;
  }

  function waitForSupabaseClient(maxMs) {
    maxMs = maxMs || 5000;
    return new Promise(function (resolve) {
      var start = Date.now();
      (function tick() {
        if (window.supabaseClient) return resolve(window.supabaseClient);
        if (Date.now() - start >= maxMs) return resolve(null);
        setTimeout(tick, 100);
      })();
    });
  }

  async function checkAuth() {
    var client = await waitForSupabaseClient();
    if (!client) {
      console.warn("protected-routes: Supabase client not ready");
      return;
    }
    var uwrap = await client.auth.getUser();
    var user = uwrap && uwrap.data ? uwrap.data.user : null;
    if (uwrap && uwrap.error) {
      console.warn("protected-routes getUser:", uwrap.error.message);
    }
    if (!user) {
      try { await client.auth.refreshSession(); } catch (e) { /* ignore */ }
      uwrap = await client.auth.getUser();
      user = uwrap && uwrap.data ? uwrap.data.user : null;
    }
    if (!user) {
      window.location.href = "/login";
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (pathRequiresSupabaseAuth()) checkAuth();
  });
})();
