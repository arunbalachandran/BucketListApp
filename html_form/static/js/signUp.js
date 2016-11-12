j$ = $.noConflict();
j$(document).ready(function() {
    j$("#signupForm").submit(function(event) {
        event.preventDefault();
    });
    // hide the span elements which show errors (initially)
    j$("#invEmail").hide();
    j$("#existEmail").hide();
    j$("#btnSignUp").click(function() {
        if ((document.getElementById("inputEmail").value).length < 256) {
            j$.ajax({
                url: '/signUp',
                data: j$('form').serialize(),
                type: 'POST',
                success: function(response) {
                    console.log("Got a valid email address.");
                    console.log(response);
                    // one way to show a successful signUp?
                    window.location.href = '/';
                },
                error: function(error) {
                    //  Entered email id already exists
                    j$("#existEmail").show().fadeOut(4000);
                    console.log("Email Id already exists.")
                    console.log(error);
                }
            });
        }
        // Unusually long email entered
        else {
            j$("#invEmail").show().fadeOut(4000);
            console.log("Email Id is too long!")
        }
    });
});
