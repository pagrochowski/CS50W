document.addEventListener('DOMContentLoaded', () => {
    const editLinks = document.querySelectorAll('.edit-link');

    editLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const postId = event.target.parentElement.parentElement.parentElement.dataset.postId;
            const postContent = document.getElementById(`post-content-${postId}`);

            const originalContent = postContent.textContent;
            const textarea = document.createElement('textarea');
            textarea.value = originalContent;
            postContent.replaceWith(textarea);

            const saveBtn = document.createElement('button');
            saveBtn.textContent = 'Save';
            saveBtn.className = 'btn btn-primary';
            textarea.parentNode.insertBefore(saveBtn, textarea.nextSibling); 

            saveBtn.addEventListener('click', () => {
                const newContent = textarea.value;
                
                fetch(`/posts/${postId}/edit/`, {
                    method: 'POST',
                    body: JSON.stringify({ content: newContent }),
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message); // Show success message
                    } else if (data.error) {
                        alert(data.error);   // Show error message
                    }
                    postContent.textContent = newContent; 
                    textarea.replaceWith(postContent);
                    saveBtn.remove();
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while editing the post.');
                });
            });
        });
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});
