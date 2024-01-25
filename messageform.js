
const messageForm = document.querySelector('.message-form');

let messageState = {};

messageForm.addEventListener('submit', onMessageFormSubmit);

 function onMessageFormSubmit(event) {
   event.preventDefault();

   const usernameInput = messageForm.elements['username'];
   const messageInput = messageForm.elements['message'];

   if (!usernameInput.value.trim() || !messageInput.value.trim()) {
     alert('Please fill all fields');
     return;
   }

   const formData = new FormData(event.target);

   for (const [key, value] of formData) {
     messageState[key] = value.trim();
   }

   console.log('Sent message:', messageState);

   messageForm.reset();
   messageState = {};
 }
