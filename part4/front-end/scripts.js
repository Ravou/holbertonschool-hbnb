document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
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

// ----------- Utilitaires -----------
function getCookie(name) {
  const cookies = document.cookie.split(';').map(c => c.trim());
  for (const c of cookies) {
    if (c.startsWith(name + '=')) {
      return c.substring(name.length + 1);
    }
  }
  return null;
}

// ----------- Login simulation -----------
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


// ----------- Gestion page login -----------

function initLoginPage() {
  const loginForm = document.getElementById('login-form');
  if (!loginForm) return;

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
    } catch {
      showError('Erreur inattendue. Veuillez réessayer.');
    }
  });
}

// ----------- Gestion page index -----------
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


function checkAuthentication() {
  const token = getCookie('token');
  const loginBtn = document.getElementById('login-btn');
  const logoutBtn = document.getElementById('logout-btn');

  if (!loginBtn || !loginBtn) return;

  if (!token) {
    loginBtn.style.display = 'inline-block';
  } else {
    loginBtn.style.display = 'none';
    logoutBtn.style.display = 'inline-block';
    fetchPlaces(token);
  }
}

function initFilter() {
  const filter = document.getElementById('price-filter');
  const placesList = document.getElementById('places-list');
  if (!filter || !placesList) return;

  filter.addEventListener('change', () => {
    const maxPrice = filter.value === 'All' ? Infinity : Number(filter.value);
    const places = placesList.querySelectorAll('.place-item');
    places.forEach(place => {
      const price = parseFloat(place.dataset.price);
      place.style.display = (price <= maxPrice) ? 'block' : 'none';
    });
  });
}

function initIndexPage() {
  checkAuthentication();
  initFilter();
}

// ----------- Initialisation globale -----------
document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('login-form')) {
    initLoginPage();
  }
  if (document.getElementById('places-list')) {
    initIndexPage();
  }
});


// ----------- Index Place card-------------------

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('article');
    card.className = 'place-card'; // <- cette classe active le style CSS

    card.innerHTML = `
      <h2>${place.name}</h2>
      <p>${place.description}</p>
      <p><strong>Location:</strong> ${place.city}, ${place.state}</p>
      <p><strong>Price:</strong> $${place.price} / night</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(card);
  });
}

// ----------- Logout ------------------------------
 
function isLoggedIn() {
	return !!localStorage.getItem('authToken');
  }

function updateUI() {
	if (isLoggedIn()) {
	   document.getElementById('login-btn').style.display = 'none';
           document.getElementById('logout-btn').style.display = 'inline-block';
        } else {
          document.getElementById('login-btn').style.display = 'inline-block';
          document.getElementById('logout-btn').style.display = 'none';
        }
      } 

      document.getElementById('login-btn').addEventListener('click', function (e) {
        e.preventDefault();
        localStorage.setItem('authToken', 'token123'); // simule un token valide
        updateUI();
        alert('Connecté !');
  });

   document.getElementById('logout-btn').addEventListener('click', function () {
     localStorage.removeItem('authToken'); // supprime le token => déconnexion
     updateUI();
    alert('Déconnecté !');
  });

 }
 
 updateUI();

});


