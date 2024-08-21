// scripts.js

$(document).ready(function() {
    // Example: Smooth scrolling for anchor links
    $('a.nav-link').on('click', function(event) {
        if (this.hash !== "") {
            event.preventDefault();
            var hash = this.hash;

            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 800, function(){
                window.location.hash = hash;
            });
        }
    });

    // Example: Display an alert when a form is submitted
    $('form').on('submit', function(event) {
        // Example: Check if all required fields are filled
        var isValid = true;
        $(this).find('input[required], textarea[required]').each(function() {
            if ($.trim($(this).val()) === "") {
                isValid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Please fill all required fields.');
        }
    });
});
