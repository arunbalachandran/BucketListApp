j$ = $.noConflict();
j$(function() {
    j$('#btnSignUp').click(function() {
        if ((document.getElementById("inputEmail").value).length < 256) {
            window.location.href = '/';
            j$.ajax({
                url: '/signUp',
                data: j$('form').serialize(),
                type: 'POST',
                success: function(response) {
                    console.log("Got email address here");
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
        // Create a session variable that will track error
        else {
            console.log("Toggle span id here");
            j$("#invemail").show();
            console.log("Invalid email -> too long!")
        }
    });
});
