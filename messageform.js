const messageForm = document.querySelector('.message-form');
const submit = document.querySelector('#submit');
const usernameInput = messageForm.elements['username'];
const messageInput = messageForm.elements['message'];

function checkInputs() {
    if (usernameInput.value.trim() && messageInput.value.trim()) {
        submit.removeAttribute('disabled');
        submit.textContent = 'Send'; 
    } else {
        submit.setAttribute('disabled', 'true');
        submit.textContent = 'Please fill all fields';
    }
}

usernameInput.addEventListener('input', checkInputs);
messageInput.addEventListener('input', checkInputs);


submit.setAttribute('disabled', 'true');
submit.textContent = 'Please fill all fields'; 
