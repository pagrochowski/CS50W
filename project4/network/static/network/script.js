document.addEventListener('DOMContentLoaded', function() {

    if (document.querySelector('.edit-link')){
        document.querySelector('.edit-link').onclick = function() {
            handleEditClick(this);
        };
    }

    if (document.getElementById('followBtn')) {
        document.getElementById('followBtn').onclick = function() {
            handleFollowClick(this);
        };
    }
});

function handleFollowClick(followBtn) {
    const userId = followBtn.dataset.userId;
        fetch(`/follow/${userId}/`)
            .then(response => response.json())
            .then(data => {
                followBtn.textContent = data.message === 'Followed' ? 'Unfollow' : 'Follow';
            })
            .catch(error => console.error('Error:', error));
}


function handleEditClick(editLink) {

    const postContainer = editLink.closest('.post-container');
    const postId = postContainer.dataset.postId;
    const postContent = postContainer.querySelector(`#post-content-${postId}`);
    
    const originalContent = postContent.textContent;
    const textarea = document.createElement('textarea');
    textarea.value = originalContent;
    textarea.classList.add('form-control');
    postContent.replaceWith(textarea);

    const saveBtn = document.createElement('button');
    saveBtn.textContent = 'Save';
    saveBtn.className = 'btn btn-primary ml-2';
    textarea.parentNode.insertBefore(saveBtn, textarea.nextSibling);

    saveBtn.addEventListener('click', () => {
        const newContent = textarea.value.trim();

        if (newContent === originalContent) {
            revertToEdit(textarea, postContent, saveBtn);
            return;
        }

        const currentPath = window.location.pathname;
        const editUrl = currentPath.startsWith('/profile/')
            ? `/profile/${currentPath.split('/')[2]}/${postId}/edit/` // Profile URL
            : `/posts/${postId}/edit/`; // Index page URL

        fetch(editUrl, {
            method: 'POST',
            body: JSON.stringify({ content: newContent }),
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    console.log("Post saved correctly.");
                } else if (data.error) {
                    alert(data.error);
                } else {
                    alert('An error occurred while processing the response.');
                }
                postContent.textContent = newContent;
                revertToEdit(textarea, postContent, saveBtn);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while editing the post.');
                revertToEdit(textarea, postContent, saveBtn);
            });
    });
}

function revertToEdit(textarea, postContent, saveBtn) {
    textarea.replaceWith(postContent);
    saveBtn.remove();
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}