// others-tasks.js

const othersTaskList = document.getElementById("list-container-others");
const logoutBtn = document.getElementById('logout-btn');
const host_url = 'http://127.0.0.1:8000';

// Function to show others' tasks from the server
async function showOthersTask() {
    try {
        const response = await fetch(`${host_url}/task/tasks/other/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${sessionStorage.getItem('accessToken')}`
            }
        });

        if (response.ok) {
            const result = await response.json();
            othersTaskList.innerHTML = ''; // Clear the current list
            if (result.status === 200 && result.data.length > 0) {
                result.data.forEach(task => {
                    let li = document.createElement("li");
                    li.innerHTML = `<strong>${task.title}</strong>: ${task.description}`;
                    othersTaskList.appendChild(li);

                    if (task.completed) {
                        li.classList.add("checked"); // Mark as completed if task is completed
                    }
                });
            } else {
                othersTaskList.innerHTML = '<li>No tasks available.</li>';
            }
        } else {
            alert('Error fetching others\' tasks.');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Call the function to show others' tasks when the page loads
window.addEventListener("load", function () {
    if (sessionStorage.getItem('accessToken')) {
        logoutBtn.style.display = 'block'; // Show logout button
        showOthersTask(); // Load others' tasks
    } else {
        window.location.href = 'todo.html'; // Redirect to login if not authenticated
    }
});

// Handle logout
logoutBtn.onclick = function () {
    sessionStorage.clear(); // Clear session storage
    // alert('Logged out successfully.');
    window.location.href = 'todo.html'; // Redirect to login page
};
