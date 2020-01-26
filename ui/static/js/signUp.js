$ = $.noConflict();
$(document).ready(function() {
    $("#signupForm").submit(function(event) {
        event.preventDefault();
    });
    // hide the span elements which show errors (initially)
    $("#invEmail").hide();
    $("#existEmail").hide();
    $("#succSignUp").hide();
    $("#btnSignUp").click(function() {
        if ((document.getElementById("inputEmail").value).length < 256) {
            $.ajax({
                url: '/signUp',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                    console.log("Got a valid email address.");
                    console.log(response);
                    $("#succSignUp").show();
                    // one way to show a successful signUp?
                    // window.location.href = '/';
                },
                error: function(error) {
                    //  Entered email id already exists
                    $("#existEmail").show().fadeOut(4000);
                    console.log("Email Id already exists.")
                    console.log(error);
                }
            });
        }
        // Unusually long email entered
        else {
            $("#invEmail").show().fadeOut(4000);
            console.log("Email Id is too long!")
        }
    });
});
