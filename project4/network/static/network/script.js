document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('click', (event) => { 
        if (!event.target.classList.contains('edit-link')) {
            return; // Exit early if not an edit link
        }

        event.preventDefault();

        const postContainer = event.target.closest('.post-container');
        const postId = postContainer.dataset.postId;
        const postContent = postContainer.querySelector(`#post-content-${postId}`);

        const originalContent = postContent.textContent;
        const textarea = document.createElement('textarea');
        textarea.value = originalContent;
        textarea.classList.add('form-control'); // Add Bootstrap class for styling
        postContent.replaceWith(textarea);

        const saveBtn = document.createElement('button');
        saveBtn.textContent = 'Save';
        saveBtn.className = 'btn btn-primary ml-2';  // Add margin
        textarea.parentNode.insertBefore(saveBtn, textarea.nextSibling);

        saveBtn.addEventListener('click', () => {
            const newContent = textarea.value.trim(); // Trim whitespace
            
            if (newContent === originalContent) {
                // No changes, revert back
                textarea.replaceWith(postContent);
                saveBtn.remove();
                return;
            }

            fetch(`/posts/${postId}/edit/`, {
                method: 'POST',
                body: JSON.stringify({ content: newContent }),
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') }
            })
            .then(response => {
                if (!response.ok) { // Check for HTTP errors
                    throw new Error('Network response was not ok.');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    alert(data.message); 
                } else if (data.error) {
                    alert(data.error);   
                } else {
                    // Handle unexpected response format
                    alert('An error occurred while processing the response.');
                }
                postContent.textContent = newContent;
                textarea.replaceWith(postContent);
                saveBtn.remove();
                event.target.style.display = 'inline'; // Show the edit link again
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while editing the post.');
                // Revert changes on error
                textarea.replaceWith(postContent);
                saveBtn.remove();
            });

        });
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});