// RAPID²AI client-side auth guard
// Checks for a valid Google session token; redirects to sign-in if absent.
// Token TTL: 8 hours (Google ID tokens are 1hr, but we gate on session presence).

(function () {
  var TOKEN_KEY = 'rapidai_auth';
  var AUTHED_AT_KEY = 'rapidai_authed_at';
  var TTL_MS = 8 * 60 * 60 * 1000; // 8 hours

  function isAuthed() {
    var token = sessionStorage.getItem(TOKEN_KEY);
    var authedAt = parseInt(sessionStorage.getItem(AUTHED_AT_KEY) || '0', 10);
    if (!token) return false;
    if (Date.now() - authedAt > TTL_MS) {
      sessionStorage.removeItem(TOKEN_KEY);
      sessionStorage.removeItem(AUTHED_AT_KEY);
      return false;
    }
    return true;
  }

  function getClientId() {
    return (
      window.__RAPIDAI_GOOGLE_CLIENT_ID__ || document.querySelector('meta[name="rapidai-client-id"]')?.content || ''
    );
  }

  function signIn(returnTo) {
    var clientId = getClientId();
    returnTo = returnTo || window.location.pathname;
    sessionStorage.setItem('rapidai_return', returnTo);

    if (!clientId) {
      // Dev fallback: bypass auth for localhost
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        sessionStorage.setItem(TOKEN_KEY, 'dev-bypass');
        sessionStorage.setItem(AUTHED_AT_KEY, Date.now().toString());
        window.location.reload();
        return;
      }
      console.error(
        '[RAPID²AI] Google Client ID not configured. Set window.__RAPIDAI_GOOGLE_CLIENT_ID__ or <meta name="rapidai-client-id">'
      );
      document.body.innerHTML =
        '<div style="display:flex;align-items:center;justify-content:center;min-height:100vh;background:#0a0e0c;color:#c9a55c;font-family:sans-serif;text-align:center;padding:2rem;"><div><h2 style="margin-bottom:1rem">RAPID²AI</h2><p style="color:#7a8278">Google Client ID not configured.<br>Contact your administrator.</p></div></div>';
      return;
    }

    // Show the Google One Tap / full sign-in overlay
    document.getElementById('rapidai-gate')?.style.setProperty('display', 'flex');
  }

  function signOut() {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(AUTHED_AT_KEY);
    window.location.replace('/');
  }

  window.RapidAIAuth = { isAuthed: isAuthed, signIn: signIn, signOut: signOut };
})();
