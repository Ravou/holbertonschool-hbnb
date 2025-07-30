const places = [
  { name: "Maison de charme", price: 100 },
  { name: "Appartement moderne", price: 80 },
];

const placesList = document.getElementById('places-list');

places.forEach(place => {
  const card = createPlaceCard(place);
  placesList.appendChild(card);
});

function createPlaceCard(place) {
  const card = document.createElement('div');
  card.className = 'place-card';

  // Nom du lieu
  const title = document.createElement('h2');
  title.textContent = place.name;

  // Prix par nuit
  const price = document.createElement('p');
  price.textContent = `Prix par nuit : ${place.price} €`;

  // Bouton "Voir les détails"
  const button = document.createElement('button');
  button.className = 'details-button';
  button.textContent = 'View Details';

  // Ajoute l'écouteur pour rediriger vers place.html avec le nom du lieu en paramètre
  button.addEventListener('click', () => {
    window.location.href = `place.html?place=${encodeURIComponent(place.name)}`;
  });

  // Ajout des éléments dans la carte
  card.appendChild(title);
  card.appendChild(price);
  card.appendChild(button);

  return card;
}

// Insertion des cartes dans la section #places-list
document.addEventListener('DOMContentLoaded', () => {
  const placesList = document.getElementById('places-list');

  places.forEach(place => {
    const card = createPlaceCard(place);
    placesList.appendChild(card);
  });
});

// Example data to simulate fetching from a database
const places = [
  {
    name: "Appartement moderne",
    host: "John Doe",
    price: 80,
    description: "A cozy apartment in the city center.",
    amenities: ["Wi-Fi", "Air Conditioning", "Fully Equipped Kitchen"],
    reviews: [
      { userName: "Alice", comment: "Great stay!", rating: 5 },
      { userName: "Bob", comment: "A bit noisy at night.", rating: 3 }
    ]
  },
  // other places ...
];

// Function to extract URL parameter
function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

// Get the place name from URL
const placeName = getQueryParam('place');

// Find the matching place
const place = places.find(p => p.name === placeName);

// Create a review card element from a review object
function createReviewCard(review) {
  // Basic escaping to avoid HTML injection
  const safeComment = review.comment.replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const safeUser = review.userName.replace(/</g, "&lt;").replace(/>/g, "&gt;");

  const card = document.createElement('div');
  card.className = 'review-card';

  card.innerHTML = `
    <p><em>"${safeComment}"</em></p>
    <p><strong>By:</strong> ${safeUser}</p>
    <p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
  `;

  return card;
}

// Render place details
function renderPlaceDetails(place) {
  const placeInfo = document.getElementById('place-info');
  if (!place) {
    placeInfo.innerHTML = "<p>Place not found.</p>";
    return;
  }

  placeInfo.innerHTML = `
    <h1>${place.name}</h1>
    <p><strong>Host:</strong> ${place.host}</p>
    <p><strong>Price per night:</strong> €${place.price}</p>
    <p>${place.description}</p>
    <h3>Amenities:</h3>
    <ul>${place.amenities.map(a => `<li>${a}</li>`).join('')}</ul>
  `;
}

// Render reviews list
function renderReviews(reviews) {
  const reviewsList = document.getElementById('reviews-list');
  reviewsList.innerHTML = '';

  if (!reviews || reviews.length === 0) {
    reviewsList.innerHTML = "<p>No reviews for this place yet.</p>";
    return;
  }

  reviews.forEach(review => {
    const card = createReviewCard(review);
    reviewsList.appendChild(card);
  });
}

// Simple logged-in check (adjust according to your auth logic)
const isLoggedIn = true;

function renderReviewAction() {
  const reviewAction = document.getElementById('review-action');
  reviewAction.innerHTML = '';

  if (!isLoggedIn) return; // not logged in, show nothing

  reviewAction.innerHTML = `
    <form class="add-review form" id="review-form">
      <h3>Add a Review</h3>
      <textarea id="review-text" name="review-text" rows="4" required placeholder="Write your review here..."></textarea>
      <br/>

