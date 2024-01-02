document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new-post-form').addEventListener('submit', newpost);
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
            console.log("SERVER MESSAGE: ", result.message)
            console.log("SERVER CONTENT: ", result.post)
            document.querySelector('#newpost').value = "";
        } else {
        console.error("Error sending email:", result.error);
        }
    })
    .catch(error => {
        console.error("Error in POST", error);
    });

}