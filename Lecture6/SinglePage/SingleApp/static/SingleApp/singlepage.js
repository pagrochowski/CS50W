// Inside singlepage.js
console.log("JavaScript file loaded!"); 

// When back arrow is clicked, show previous section
window.onpopstate = function(event) {
    console.log(event.state.section);
    showSection(event.state.section);
}

// Shows given section
function showSection(section) {
    // Find section text from server
    fetch(`/sections/${section}`)
    .then(response => response.text())
    .then(text => {
        // Log text and display on page
        console.log(text);
        document.querySelector('#content').innerHTML = text;
    })
}

document.addEventListener('DOMContentLoaded', function() {
    // Add button functionality
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            const section = this.dataset.section;

            // Add the current state to the history
            history.pushState({section: section}, "", `section${section}`);
            showSection(section);
        };
    });
});