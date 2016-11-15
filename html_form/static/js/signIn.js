$(document).ready(function() {
    $("#signinForm").submit(function(event) {
        event.preventDefault();
    });
    $("#loginmail").hide();
    $('#btnSignIn').click(function() {
        if ((document.getElementById("inputEmail").value).length < 256) {
            console.log("Satisfies length constraint");
            console.log("This is data===>>>"+$('form').serialize());
            $.ajax({
                url: '/validateLogin',
                data: $('form').serialize(),
                type: 'POST',
                success: function(result) {
                    console.log("Got login credentials here");
                    window.location.href = "/userHome";
                },
                error: function(error) {
                    $('#loginmail').show().fadeOut(4000);
                    console.log(error);
                }
            });
        }
        else {
            console.log("Doesn't satisfy length constraint!");
            $("#loginmail").show().fadeOut(4000);
        }
    });
});
