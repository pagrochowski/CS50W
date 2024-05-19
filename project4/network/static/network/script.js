document.addEventListener('DOMContentLoaded', function() {

    // Select all edit buttons
    const editLink = document.querySelectorAll('.edit-link');
    // Use forEach to attach the event listener to each button
    editLink.forEach(button => {
        button.addEventListener('click', function() {
            console.log("Edit button clicked!");
            handleEditClick(this); // 'this' refers to the clicked button
        });
    });

     // Select all edit buttons
     const followBtn = document.querySelectorAll('#followBtn');
     // Use forEach to attach the event listener to each button
     followBtn.forEach(button => {
         button.addEventListener('click', function() {
             console.log("Follow button clicked!");
             handleFollowClick(this); // 'this' refers to the clicked button
         });
     });

    // Select all like-unlike buttons
    const likeUnlikeButtons = document.querySelectorAll('.like-unlike-button');
    // Use forEach to attach the event listener to each button
    likeUnlikeButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log("Like button clicked!");
            handleLikeUnlikeClick(this); // 'this' refers to the clicked button
        });
    });
});

function handleLikeUnlikeClick(button) {
    const postContainer = button.closest('.post-container');
    const postId = button.dataset.postId;
    
    fetch(`/like/${postId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            // Update like count and button text based on response
            button.textContent = `${data.liked ? 'Unlike' : 'Like'} (${data.likes_count})`; // Update both text and count
            const likesCountElement = postContainer.querySelector('.likes-count'); // Get updated reference
            if (likesCountElement) { 
                likesCountElement.textContent = data.likes_count;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while liking/unliking the post.');
        });
}


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