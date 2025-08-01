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

// ---- MOCK DATA FOR REVIEWS ----
const MOCK_REVIEWS = {
  1: [
    {
      first_name: "Alice",
      last_name: "Dupont",
      comment: "Super studio, très propre et bien situé !",
      rating: 5
    },
    {
      first_name: "Lucas",
      last_name: "Martin",
      comment: "Petit mais fonctionnel. Bon rapport qualité-prix.",
      rating: 4
    }
  ],
  2: [
    {
      first_name: "Sophie",
      last_name: "Durand",
      comment: "La villa est incroyable, surtout la piscine !",
      rating: 5
    },
    {
      first_name: "Thomas",
      last_name: "Petit",
      comment: "Très spacieux, parfait pour des vacances en famille.",
      rating: 4
    }
  ],
  3: [
    {
      first_name: "Emma",
      last_name: "Bernard",
      comment: "Hôte très sympa, chambre propre, je recommande.",
      rating: 4
    }
  ],
  4: [
    {
      first_name: "Noah",
      last_name: "Lemoine",
      comment: "Très bien situé mais un peu bruyant la nuit.",
      rating: 3
    },
    {
      first_name: "Chloé",
      last_name: "Robert",
      comment: "Appartement moderne et confortable.",
      rating: 5
    }
  ]
};

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
      <p><strong>Price:</strong> ${place.price} $</p>
      <div class="details-card">
   	 <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      </div>
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

// Fonction pour récupérer l'id place depuis l'URL
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return parseInt(params.get('id'), 10);
}

// Mock function to simulate fetching place details with extra info (amenities, reviews)
async function fetchPlaceDetailsMock(placeId) {
  // Recherche la place dans MOCK_PLACES
  const place = MOCK_PLACES.find(p => p.id === placeId);
  if (!place) return null;

  // Ajout mock d'amenities et reviews
  const amenitiesMock = {
    1: ["WiFi", "Heating", "Kitchen"],
    2: ["Pool", "WiFi", "Air Conditioning"],
    3: ["WiFi", "Parking"],
    4: ["Elevator", "Heating"]
  };
  
  return {
    place, 
    amenities: amenitiesMock[placeId] 	  
  };
}

function renderPlaceCard(place, amenities) {
  const card = document.createElement('div');
  card.className = 'place-card';

  card.innerHTML = `
    <h2>${place.name}</h2>
    <p><strong>Description:</strong> ${place.description}</p>
    <p><strong>Location:</strong> ${place.location}</p>
    <p><strong>Price:</strong> ${place.price} $ / night</p>
    <p><strong>Amenities:</strong> ${amenities.join(', ') || 'None'}</p>

  `;

  return card;
}

function renderReviews(placeId) {
  const reviewsContainer = document.getElementById('reviews-container');
  reviewsContainer.innerHTML = '<h3>Reviews</h3>'; // Titre
  const reviews = MOCK_REVIEWS[placeId] ;

  if (!reviews || reviews.length === 0) {	  
    reviewsContainer.innerHTML += '<p>No reviews yet.</p>';
    return;
  }

  reviews.forEach(review => {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `
      <h4>${review.first_name} ${review.last_name}</h4>
      <p>${review.comment}</p>
      <p><strong>Rating:</strong> ${'⭐'.repeat(review.rating)}</p>
    `;
    reviewsContainer.appendChild(card);
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  const placeId = getPlaceIdFromURL();
  const container = document.getElementById('place-details');

  if (!placeId) {
    container.textContent = "No place ID provided in URL.";
    return;
  }

  const details = await fetchPlaceDetailsMock(placeId);
  if (!details) {
    container.textContent = "Place not found.";
    return;
  }
  
  const card = renderPlaceCard(details.place, details.amenities);
  container.innerHTML = '';
  container.appendChild(card);

  renderReviews(placeId);

});
