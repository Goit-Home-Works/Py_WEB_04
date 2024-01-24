
const changeColorButton = document.querySelector('.test');
const cards = document.querySelectorAll('.card.mb-4.rounded-3.shadow-sm');
const cards1 = document.querySelectorAll('.card-header.py-3');

let currentIndex = 0;

changeColorButton.addEventListener('click', onClickChangeColorButton);

function onClickChangeColorButton() {
  cards[currentIndex].classList.remove('border-primary');
  cards1[currentIndex].classList.remove( 'border-primary', 'text-bg-primary');

  currentIndex = (currentIndex + 1) % cards.length;
  cards[currentIndex].classList.add('border-primary');
  cards1[currentIndex].classList.add( 'text-bg-primary');
  const currentArticleTitle = cards1[currentIndex].querySelector('h4').textContent;
  console.clear();
  console.log(`current article is ${currentArticleTitle}`);
  // alert(`current article is ${currentArticleTitle}`)
}


