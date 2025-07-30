document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();


      const email = loginForm.elements['email'].value;
      const password = loginForm.elements['password'].value;

      try {
        const response = await loginUser(email, password);

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/;`;
	  window.location.href = 'index.html';
		
        } else {
          const error = await response.json();
          showError(error.message || 'Erreur de connexion');
        }
      } catch (err) {
        showError('Erreur inattendue. Veuillez réessayer.');
      }
    });
  }
});

// Fonction simulant une requête à l'API
async function loginUser(email, password) {
  return new Promise((resolve) => {
    setTimeout(() => {
      // Credentials valides simulés
      if (email === 'test@example.com' && password === '123456') {
        resolve({
          ok: true,
          json: async () => ({ access_token: 'fake-jwt-token-123456789' })
        });
      } else {
        resolve({
          ok: false,
          statusText: 'Invalid credentials',
          json: async () => ({ message: 'Email ou mot de passe incorrect' })
        });
      }
    }, 700);
  });
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

====== index.html ====

async function fetchPlaces(token) {
  // Simulation d'une requête réseau avec un délai
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, name: "Charming Apartment", description: "Near the park", city: "Paris", state: "Ile-de-France", price: 45 },
        { id: 2, name: "Cozy Loft", description: "Downtown", city: "Lyon", state: "Auvergne-Rhône-Alpes", price: 75 },
        { id: 3, name: "Luxury Villa", description: "Seaside view", city: "Nice", state: "Provence-Alpes-Côte d’Azur", price: 150 },
      ]);
    }, 500); // délai simulé 500ms
  }).then(displayPlaces);
}

