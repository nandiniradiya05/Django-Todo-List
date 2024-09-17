

const inputBox = document.getElementById("input-box");
const button = document.querySelector("button");
const list = document.getElementById("list-container");
const myButton = document.querySelector('#add-task');

const authModal = document.getElementById('auth-modal');
const signupLoginBtn = document.getElementById('signup-login-btn');
const closeBtn = document.querySelector('.close-btn');
const signupForm = document.getElementById('signup-form');
const authSubmitBtn = document.getElementById('auth-submit-btn');
const modalTitle = document.getElementById('modal-title');
const switchToLogin = document.getElementById('switch-to-login');
const host_url = 'http://127.0.0.1:8000';



function addTask(){
    if(inputBox.value === ''){
        alert("you must write something!");
    }else{
        let li = document.createElement("li");
        li.innerHTML = inputBox.value;
        list.appendChild(li);
        inputBox.value = '';
        let span = document.createElement("span");
        span.innerHTML = "x";
        li.appendChild(span);
    }
    saveData();
}
list.addEventListener("click", (e)=>{
    if(e.target.tagName === "LI"){
        e.target.classList.toggle("checked");
        saveData();
    }else if(e.target.tagName === "SPAN"){
        e.target.parentElement.remove();
        saveData();
    }
});

myButton.addEventListener("click", addTask);

function saveData(){
    localStorage.setItem("data", list.innerHTML);
}
function showTask(){
    const savedData = localStorage.getItem("data");
    if(savedData){
        list.innerHTML = savedData;
    }
}
window.addEventListener("load", showTask);





// Show the modal when the signup/login button is clicked
signupLoginBtn.onclick = function() {
    authModal.style.display = 'block';
}

// Close the modal when the close button is clicked
closeBtn.onclick = function() {
    authModal.style.display = 'none';
}

// Close the modal if user clicks outside the modal
window.onclick = function(event) {
    if (event.target == authModal) {
        authModal.style.display = 'none';
    }
}

// Toggle between signup and login
// Handle toggle between signup and login
switchToLogin.onclick = function(e) {
    e.preventDefault();
    const nameInput = document.getElementById('name');

    if (modalTitle.textContent === 'Sign Up') {
        // Switch to Login mode
        modalTitle.textContent = 'Login';
        authSubmitBtn.textContent = 'Login';
        nameInput.style.display = 'none';  // Hide the name input for login
        nameInput.removeAttribute('required'); // Remove the required attribute
        switchToLogin.innerHTML = `Don't have an account? <a href="#">Sign Up</a>`;
    } else {
        // Switch to Signup mode
        modalTitle.textContent = 'Sign Up';
        authSubmitBtn.textContent = 'Sign Up';
        nameInput.style.display = 'block';  // Show the name input for signup
        nameInput.setAttribute('required', 'required'); // Add the required attribute
        switchToLogin.innerHTML = `Already have an account? <a href="#">Login</a>`;
    }
}

// Handle signup/login form submission
signupForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Set the URL based on whether we're signing up or logging in
    const url = host_url+'/task/signup-login/';
    const isSignup = modalTitle.textContent === 'Sign Up';
    
    // Prepare payload for signup or login
    const payload = isSignup 
        ? { name, email, password } 
        : { email, password };

    // Send the request to the API
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();
        console.log(data);

        if (response.ok) {
            alert(data.message);
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            authModal.style.display = 'none';
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong.');
    }
});