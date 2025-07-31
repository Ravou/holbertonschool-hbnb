document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  // --- Affichage dynamique des boutons Login/Logout ---
  const loginBtn = document.getElementById('login-btn');
  const logoutBtn = document.getElementById('logout-btn');


  
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
          window.location.href = 'index.html'; // redirection après succès
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

// --- MOCK DATA FOR PLACES ---
const MOCK_PLACES = [
  { id: 1, name: "Studio Paris", description: "Cozy small studio", location: "Paris", price: 50 },
  { id: 2, name: "Villa Nice", description: "Large villa with pool", location: "Nice", price: 100 },
  { id: 3, name: "Room Lyon", description: "Room in a local's home", location: "Lyon", price: 10 },
  { id: 4, name: "Apartment Bordeaux", description: "Downtown apartment", location: "Bordeaux", price: 50 }
];

// --- UTILS ---
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// --- AUTHENTICATION & LOGIN LINK ---
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
      fetchPlaces(token);
    }
  } else {
    // If no login-link, still display places if authenticated
    if (token) fetchPlaces(token);
  }
}

// --- MOCK FETCH PLACES ---
async function fetchPlaces(token) {
  // Simulate network delay
  setTimeout(() => {
    displayPlaces(MOCK_PLACES);
  }, 500);
}

// --- DISPLAY PLACES ---
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;
  placesList.innerHTML = '';
  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.dataset.price = place.price;
    div.innerHTML = `
      <h3>${place.name}</h3>
      <p>${place.description}</p>
      <p><strong>City:</strong> ${place.location}</p>
      <p><strong>Price:</strong> ${place.price} €</p>
    `;
    placesList.appendChild(div);
  });
}

// --- PRICE FILTER ---
function setupPriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return;
  filter.innerHTML = `
    <option value="all">All</option>
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
  `;
  filter.addEventListener('change', (event) => {
    const value = event.target.value;
    const cards = document.querySelectorAll('.place-card');
    cards.forEach(card => {
      const price = parseInt(card.dataset.price, 10);
      if (value === 'all' || price <= parseInt(value, 10)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

// --- INIT ---
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  setupPriceFilter();
});