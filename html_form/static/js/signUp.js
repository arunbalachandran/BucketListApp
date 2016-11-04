$(function() {
    $('#btnSignUp').click(function() {
        console.log('here!');
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log('what is wrong world!');
                console.log(error);
            }
        });
    });
});
