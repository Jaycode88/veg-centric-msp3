// Nav bar dropdown for mobile
$(document).ready(function() {
    var dropdownMobile = $('.dropdown-trigger');
    dropdownMobile.dropdown();
});

//confirm password on sign up 
$(document).ready(function() {
    $('form').submit(function(event) {
        var password = $('#password').val();
        var confirm_password = $('#confirm_password').val();

        if (password !== confirm_password) {
            alert('Passwords do not match');
            event.preventDefault(); // Prevent form submission
        }
    });
});