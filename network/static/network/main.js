document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new-post-form').addEventListener('submit', newpost);
});


function newpost(Event) {
    Event.preventDefault();

    var post = document.querySelector('#newpost').value;

    if (post.length > 0) {
        console.log(`This worked good job. New tweet was: ${post}`);
    } else {
        console.log("Nothing in the form")
    }
}