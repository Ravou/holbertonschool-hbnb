document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM chargé, script lancé');

  const loginForm = document.getElementById('login-form');
  const loginBtn = document.getElementById('login-btn');
  const logoutBtn = document.getElementById('logout-btn');

  if (loginForm) {
    loginForm.addEventListener('submit', (event) => {
      event.preventDefault();
      console.log('Formulaire soumis');

      const email = doucument.getElementById('email').value;
      const password = document.getElementById('password').value;
      

// Fonction mock simulant une requête de login
function simulateLogin(email, password) {
  // Optionnel : Vérifie si les valeurs sont "valides"
  if (email === 'test@example.com' && password === '123456') {
    const fakeToken = 'fake-jwt-token-123abc';

    // Stocke le token dans un cookie
    document.cookie = `token=${fakeToken}; path=/`;

    // Redirige vers la page d’accueil
    window.location.href = 'index.html';
  } else {
    // Affiche un message d’erreur
    alert('Login failed: invalid credentials');
  }
}


function showError(message) {
  let errorDiv = document.getElementById('login-error');
  if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.id = 'login-error';
    errorDiv.style.color = 'red';
    errorDiv.style.marginBottom = '1em';
    document.getElementById('login-form').prepend(errorDiv);
  }
  errorDiv.textContent = message;
}

  // Fonction pour récupérer le token dans le cookie
  function getToken() {
    const match = document.cookie.match(/(?:^|; )token=([^;]*)/);
    return match ? match[1] : null;
  }

  // Affichage conditionnel des boutons login/logout
  function toggleAuthButtons() {
    const token = getToken();
    if (token) {
      loginBtn.style.display = 'none';
      logoutBtn.style.display = 'inline-block';
    } else {
      loginBtn.style.display = 'inline-block';
      logoutBtn.style.display = 'none';
    }
  }

  toggleAuthButtons();

  // Gestion du logout (disponible uniquement si logoutBtn existe)
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // Suppression du cookie token
      document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
      toggleAuthButtons();
      // Redirection vers login
      window.location.href = 'login.html';
    });
  }

  // Simulation du login (disponible uniquement si loginForm existe)
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = loginForm.email.value.trim();
      const password = loginForm.password.value.trim();

      // Ici tu simules un login valide uniquement avec ces identifiants :
      if (email === 'test@test.com' && password === '123456') {
        const fakeToken = 'mocked_jwt_token_123456';
        // Enregistre le token dans un cookie
        document.cookie = `token=${fakeToken}; path=/; max-age=3600`; // expire dans 1 heure
        // Redirige vers index.html
        window.location.href = 'index.html';
      } else {
        alert('Login failed: invalid credentials (simulation)');
      }
    });
  }
});
