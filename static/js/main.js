// static/js/main.js

document.addEventListener("DOMContentLoaded", () => {

    function openModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.style.display = "flex";
    }

    function closeModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.style.display = "none";
    }

    // Close modal buttons
    document.querySelectorAll(".close").forEach(el => {
        el.onclick = () => closeModal(el.dataset.close);
    });

    // Navbar buttons
    const signupBtn = document.getElementById("signupBtn");
    const signinBtn = document.getElementById("signinBtn");
    const settingsLink = document.getElementById("settingsLink");

    if (signupBtn) signupBtn.onclick = () => openModal("signupModal");
    if (signinBtn) signinBtn.onclick = () => openModal("signinModal");
    if (settingsLink) settingsLink.onclick = () => openModal("settingsModal");

    // Theme + zoom
    const applyTheme = document.getElementById("applyTheme");
    const zoomIn = document.getElementById("zoomIn");
    const zoomOut = document.getElementById("zoomOut");

    if (applyTheme) {
        applyTheme.onclick = () => {
            const theme = document.querySelector('input[name="theme"]:checked').value;
            if (theme === "black") {
                document.body.style.background = "black";
                document.body.style.color = "white";
            } else if (theme === "green") {
                document.body.style.background = "green";
                document.body.style.color = "white";
            } else {
                document.body.style.background = "#f8f9fa";
                document.body.style.color = "black";
            }
            closeModal("settingsModal");
        };
    }

    if (zoomIn) zoomIn.onclick = () => document.body.style.zoom = "115%";
    if (zoomOut) zoomOut.onclick = () => document.body.style.zoom = "100%";

    // Buy Now buttons for recommended products
    document.querySelectorAll(".buyBtn").forEach(btn => {
        btn.onclick = () => openModal(`productModal${btn.dataset.index}`);
    });
});
