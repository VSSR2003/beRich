function addRainbowBackground() {
    const container = document.querySelector('.container');
    container.classList.add('rainbow-background');
}

// Check if the page is being reloaded
if (performance.navigation.type === 1) {
    // Page is being reloaded, apply the rainbow background animation
    addRainbowBackground();
}

document.getElementById("login-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Check if username and password are "root"
    if (username === "root" && password === "root") {
        // Open the dashboard webpage
        window.location.href = "dashboard.html"; // Replace "dashboard.html" with the actual URL of your dashboard page
    } else {
        document.getElementById("error-message").textContent = "Invalid username or password";
    }
}); 