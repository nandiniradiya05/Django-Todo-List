const inputBox = document.getElementById("input-box");
const button = document.querySelector("button");
const list = document.getElementById("list-container");
const myButton = document.querySelector('#add-task');
const othersTasksLink = document.querySelector('.link-text'); // "View others' tasks" link
const authModal = document.getElementById('auth-modal');
const signupLoginBtn = document.getElementById('signup-login-btn');
const closeBtn = document.querySelector('.close-btn');
const signupForm = document.getElementById('signup-form');
const authSubmitBtn = document.getElementById('auth-submit-btn');
const modalTitle = document.getElementById('modal-title');
const switchToLogin = document.getElementById('switch-to-login');
const logoutBtn = document.getElementById('logout-btn');
const errorMessage = document.getElementById('error-message'); // Error message element
const host_url = 'http://127.0.0.1:8000';

// Function to show the signup/login modal
function showAuthModal() {
    authModal.style.display = 'block';
}

// Check authentication before performing any action
function checkAuthentication(event) {
    if (!sessionStorage.getItem('accessToken')) {
        event.preventDefault(); // Prevent the default action (navigation or form submission)
        showAuthModal(); // Show the signup/login modal
    }
}

// Event listener for "Add" button click
myButton.addEventListener("click", function(event) {
    checkAuthentication(event); // Check if the user is authenticated
    if (sessionStorage.getItem('accessToken')) {
        addTask(); // Call addTask if authenticated
    }
});

// Event listener for "View Others' Tasks" link click
othersTasksLink.addEventListener("click", function(event) {
    checkAuthentication(event); // Check if the user is authenticated
});

// Function to add a new task
async function addTask() {
    // Clear any previous error message
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';

    if (inputBox.value === '') {
        // Show error message below the input field
        errorMessage.textContent = "You must write something!";
        errorMessage.style.display = 'block';
    } else {
        const task = { title: inputBox.value, description: "" }; // Adjust task structure if needed
        try {
            const response = await fetch(`${host_url}/task/tasks/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
                },
                body: JSON.stringify(task)
            });

            if (response.ok) {
                showTask(); // Refresh task list after adding new task
                inputBox.value = '';
            } else {
                alert('Error adding task.');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

// Function to mark a task as completed or not completed
async function completeTask(taskId, currentCompletedStatus) {
    try {
        const updatedStatus = !currentCompletedStatus; // Toggle completed status
        const response = await fetch(`${host_url}/task/tasks/${taskId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
            },
            body: JSON.stringify({ completed: updatedStatus }) // Send the updated completed status
        });

        if (response.ok) {
            showTask(); // Refresh task list after marking as completed or not completed
        } else {
            alert('Error updating task status.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to show tasks from the server
async function showTask() {
    try {
        const response = await fetch(`${host_url}/task/tasks/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
            }
        });

        if (response.ok) {
            const result = await response.json();
            list.innerHTML = ''; // Clear the current list
            if (result.status === 200 && result.data.length > 0) {
                result.data.forEach(task => {
                    let li = document.createElement("li");
                    li.innerHTML = `<strong>${task.title}</strong> ${task.description}`;
                    li.setAttribute('data-completed', task.completed); // Store the completed status in the element
                    list.appendChild(li);

                    let span = document.createElement("span");
                    span.innerHTML = "x";
                    span.setAttribute('data-id', task.id); // Store task id for deletion
                    li.appendChild(span);

                    if (task.completed) {
                        li.classList.add("checked"); // Mark as completed if task is completed
                    }

                    // Add event listener for marking the task as completed or not completed
                    li.addEventListener('click', (e) => {
                        if (e.target !== span) { // Avoid triggering on the delete button
                            const currentCompletedStatus = task.completed;
                            completeTask(task.id, currentCompletedStatus); // Pass current status to toggle
                        }
                    });
                });
            } else {
                list.innerHTML = '<li>No tasks available.</li>';
            }
        } else {
            alert('Error fetching tasks.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

list.addEventListener("click", (e) => {
    if (e.target.tagName === "SPAN") {
        const taskId = e.target.getAttribute('data-id');
        deleteTask(taskId); // Call function to delete task
    }
});

// Function to delete a task
async function deleteTask(taskId) {
    try {
        const response = await fetch(`${host_url}/task/tasks/${taskId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
            }
        });

        if (response.ok) {
            showTask(); // Refresh task list after deletion
        } else {
            alert('Error deleting task.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

myButton.addEventListener("click", addTask);

// Show the modal when the signup/login button is clicked
signupLoginBtn.onclick = function () {
    authModal.style.display = 'block';
}

// Close the modal when the close button is clicked
closeBtn.onclick = function () {
    authModal.style.display = 'none';
}

// Close the modal if user clicks outside the modal
window.onclick = function (event) {
    if (event.target == authModal) {
        authModal.style.display = 'none';
    }
}

// Toggle between signup and login
switchToLogin.onclick = function (e) {
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
signupForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Set the URL based on whether we're signing up or logging in
    const url = modalTitle.textContent === 'Sign Up' ? `${host_url}/task/signup-login/` : `${host_url}/task/signup-login/`;
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

        if (response.ok) {
            // alert(data.message);
            sessionStorage.setItem('accessToken', data.access); // Store access token in session storage
            sessionStorage.setItem('refreshToken', data.refresh); // Store refresh token in session storage
            authModal.style.display = 'none';
            signupLoginBtn.style.display = 'none'; // Hide login/signup button
            logoutBtn.style.display = 'block'; // Show logout button
            showTask(); // Load tasks after login
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong.');
    }
});

// Handle logout
logoutBtn.onclick = function () {
    sessionStorage.clear(); // Clear session storage
    signupLoginBtn.style.display = 'block'; // Show login/signup button
    logoutBtn.style.display = 'none'; // Hide logout button
    list.innerHTML = ''; // Clear task list
    // alert('Logged out successfully.');
}

// Show tasks on page load if logged in
window.addEventListener("load", function () {
    if (sessionStorage.getItem('accessToken')) {
        signupLoginBtn.style.display = 'none'; // Hide login/signup button
        logoutBtn.style.display = 'block'; // Show logout button
        showTask(); // Load tasks
    }
});

