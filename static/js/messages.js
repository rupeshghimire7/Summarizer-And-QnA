document.addEventListener("DOMContentLoaded", function () {
    var msgElement = document.getElementById("status-msg");
    if (msgElement) {
        setTimeout(function () {
            msgElement.style.display = "none";
        }, 5000);  // 5000 milliseconds = 5 seconds
    }
});