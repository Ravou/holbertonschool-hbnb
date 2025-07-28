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
  button.textContent = 'Voir les détails';


  // Ajout des éléments dans la carte
  card.appendChild(title);
  card.appendChild(price);
  card.appendChild(button);

  return card;
}


// Fonction pour afficher les détails du lieu
function renderPlaceDetails(place) {
  const detailsSection = document.getElementById('place-details');
  detailsSection.innerHTML = `
    <h1>${place.name}</h1>
    <p><strong>Hôte :</strong> ${place.host}</p>
    <p><strong>Prix par nuit :</strong> ${place.price} €</p>
    <p>${place.description}</p>
    <h3>Équipements :</h3>
    <ul>
      ${place.amenities.map(item => `<li>${item}</li>`).join('')}
    </ul>
  `;
}

// Fonction pour créer une carte d'avis
function createReviewCard(review) {
  const card = document.createElement('div');
  card.className = 'review-card';

  const comment = document.createElement('p');
  comment.textContent = review.comment;
  comment.style.fontStyle = "italic";

  const user = document.createElement('p');
  user.textContent = `Par : ${review.userName}`;
  user.style.fontWeight = "bold";

  const rating = document.createElement('p');
  rating.textContent = 'Note : ' + '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
  rating.style.color = '#f39c12';

  card.appendChild(comment);
  card.appendChild(user);
  card.appendChild(rating);

  return card;
}

function renderReviewAction(isLoggedIn) {
  const actionSection = document.querySelector('.review-action');
  actionSection.innerHTML = '';

  if (!isLoggedIn) {
    return; // Pas d'action si non connecté
  }

  // Bouton pour aller à add_review.html
  const button = document.createElement('button');
  button.textContent = "Ajouter un avis";
  button.className = 'details-button'; 
  button.addEventListener('click', () => {
    window.location.href = 'add_review.html';
  });
  actionSection.appendChild(button);
}


// Gestion de la soumission du formulaire d’ajout d’avis
function handleReviewForm() {
  const form = document.getElementById('review-form');

  form.addEventListener('submit', function(event) {
    event.preventDefault();

    const reviewText = form['review-text'].value.trim();
    // Ici, tu peux récupérer aussi le nom d'utilisateur s'il est disponible (ex: via login)
    // Pour l'exemple, on met un nom générique ou tu peux ajouter un champ dans le form
    const userName = "User";

    if (reviewText === "") {
      alert("Can you write a review.");
      return;
    }

    const newReview = {
      userName,
      comment: reviewText,
      rating: 5, // Si tu veux un champ note, il faudra l'ajouter dans le formulaire
    };

    reviews.push(newReview);

    renderReviewsList(); // mettre à jour la liste affichée

    form.reset();
  });
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
  renderPlaceDetails(place);
  renderReviewsList();
  handleReviewForm();
});
