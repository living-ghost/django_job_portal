$(document).ready(function() {
    // Example jQuery enhancements
    $('.resume-card').on('mouseover', function() {
        $(this).find('.view-overlay').fadeIn();
    }).on('mouseleave', function() {
        $(this).find('.view-overlay').fadeOut();
    });
});