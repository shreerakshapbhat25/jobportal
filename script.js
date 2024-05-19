// Function to toggle the chatbot modal
function toggleChatbot() {
    var modal = document.getElementById("chatbotModal");
    if (modal.style.display === "block") {
        modal.style.display = "none";
    } else {
        modal.style.display = "block";
    }
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById("chatbotModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Add event listener to chatbot icon
document.getElementById("chatIcon").addEventListener("click", toggleChatbot);
