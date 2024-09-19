document.addEventListener('DOMContentLoaded', function () {


    commentFormTextInput = document.getElementById('id_text');

    replyButtons = document.querySelectorAll('.reply-button');
    

    replySample = document.getElementById('reply-sample');
    replySampleUser = document.getElementById('reply-sample-user');
    replyDiv = document.getElementById('reply-div');
    commentButton = document.getElementById('comment-button');

    replyButtons.forEach(button => {
        button.addEventListener('click', function () {

            commentId = this.getAttribute('data-commentId');
            this.dataset.commentId;

            id_parent.value = commentId;

            comment = document.getElementById('comment-' + commentId);
            commentText = comment.querySelector('#comment-text');
            commentUser = comment.querySelector('#comment-user');

            replySample.innerText = commentText.innerText;
            replySampleUser.innerText = commentUser.innerText;
            replyDiv.removeAttribute("hidden");

            commentButton.scrollIntoView();

        });
    });


    lastAtSymbol = 0;
    commentFormTextInput.addEventListener('input',function(e){

        text = input.value;
        atSymbol = text.lastIndexOf("@");

        if(atSymbol > lastAtSymbol){


        }

        console.log('typing');
       });
});
