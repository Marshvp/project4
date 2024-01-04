let currentEditingPostId = null;

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('new-post-form')) {

        document.querySelector('#new-post-form').addEventListener('submit', newpost);
    }
    if (document.getElementById('profile-page')) {
        
        const targetUserId = document.getElementById('profile-page').dataset.userId;
        isfollowing(targetUserId);
        
        const followBtn = document.getElementById('follow-btn');
        if (followBtn) {
            followBtn.addEventListener('click', () => {
                followbutton(targetUserId)
            });
        }
    }

    const editButtons = document.querySelectorAll('[data-bs-target="#editModal"]');
    if (editButtons){
        console.log("hittiing editButtons")
    }
    
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            // Set the onclick attribute of the save button with the postId
            document.getElementById('editSave').setAttribute('onclick', `saveChanges(${postId})`);
            console.log("Editing post ID:", postId);
            loadeditModal(postId);
        });
    });

});



function newpost(Event) {
    Event.preventDefault();

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var post = document.querySelector('#newpost').value;

    if (post.length > 0) {
        console.log(`This worked good job. New tweet was: ${post}`);
    } else {
        console.log("Nothing in the form")
    }

    fetch('/new_post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            content: post
        })
        
    })
    .then(res => { if (!res.ok){
        throw new Error(`HTTP error! Status: ${res.status}`);
    };
        return res.json();
    })
    .then(result => {
        console.log("Post sent");
        if (!result.error){
            console.log(result)
            console.log("SERVER MESSAGE: ", result.message)
            console.log("SERVER CONTENT: ", result.post)
            add_new_post_to_page(result.post)
            document.querySelector('#newpost').value = "";
        } else {
        console.error("Error sending email:", result.error);
        }
    })
    .catch(error => {
        console.error("Error in POST", error);
    });

}

function add_new_post_to_page (post) {

    const postElement = document.createElement('div')
    postElement.classList.add('fake-post')

    const profileUrl = `/profile/${post.user_id}/`

    postElement.innerHTML = `
        <h4><a href="${profileUrl}">${post.user}</a></h4>
        <h5 class="mt-2">${post.content}</h5>
        ${post.date}<br>
        <button class="btn btn-primary">Like Button</button> `;
    
    
    document.getElementById("all-posts").prepend(postElement);
}


function isfollowing(targetUserId) {
    console.log("isfollowing called")
    fetch(`/check_following/${targetUserId}`)
    .then(res => res.json())
    .then(data => {
        console.log("is following data: ", data)
        const followBtn = document.getElementById('follow-btn');
        if (data.is_following) {
            followBtn.innerHTML = 'Unfollow';
        } else {
            followBtn.innerHTML = 'Follow';
        }
            
    })
    
}

function followbutton(targetUserId){

    console.log("targetUserId from follow button: ", targetUserId)

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const target_user_id = targetUserId

    fetch(`/follow_unfollow/${target_user_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log("followbutton data:", data)
        isfollowing(target_user_id)
    })
    
}

function loadeditModal(postId) {
    
    console.log("Hello World")

    const pId = postId

    fetch(`/editModaldata/${postId}`)
        .then(res => res.json())
        .then(data => {
            console.log(data)
            console.log(data.content)
            document.getElementById('editModal-textarea').value = data.content;
            currentEditingPostId = postId;
        })
        .catch(error => console.error('Error', error));

    
}

function closeModal() {
    const editModalElement = document.getElementById('editModal');
    const editModal = bootstrap.Modal.getInstance(editModalElement);
    if (editModal) {
        editModal.hide();
    }
}