j$ = $.noConflict();

j$(document).ready(function() {
    j$("#signinForm").submit(function(event) {
        event.preventDefault();
    });
    j$("#loginmail").hide();
    j$('#btnSignIn').click(function() {
        if ((document.getElementById("inputEmail").value).length < 256) {
            console.log("Satisfies length constraint");
            j$.ajax({
                url: '/validateLogin',
                data: j$('form').serialize(),
                type: 'POST',
                success: function(result) {
                    console.log("Got login credentials here");
                    j$('#signinForm').submit();
                    window.location.href = "/userHome";
                },
                error: function(error) {
                    j$('#loginmail').show().fadeOut(4000);
                    console.log(error);
                }
            });
        }
        else {
            console.log("Doesn't satisfy length constraint!");
            j$("#loginmail").show().fadeOut(4000);
        }
    });
});
