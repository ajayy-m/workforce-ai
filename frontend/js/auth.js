function saveAuth(data) {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
}

function getUser() {
    return JSON.parse(localStorage.getItem("user"));
}

function isLoggedIn() {
    return !!localStorage.getItem("token");
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "../pages/login.html";
}

function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        window.location.href = "dashboard.html";
    }
}

function redirectIfNotLoggedIn() {
    if (!isLoggedIn()) {
        window.location.href = "login.html";
    }
}