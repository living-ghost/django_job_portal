$(document).ready(function() {
    const requestOtpBtn = $('#requestOtpBtn');
    const verifyOtpBtn = $('#verifyOtpBtn');
    const resendOtpBtn = $('#resendOtpBtn');
    const subscriptionForm = $('#subscriptionForm');
    const emailInput = $('#subscriberEmail');
    const otpInput = $('#otpCode');
    const emailSection = $('#emailSection');
    const otpSection = $('#otpSection');
    const hiddenEmailInput = $('#hiddenEmail');

    // Handle OTP request
    requestOtpBtn.click(function(event) {
        event.preventDefault();
        const email = emailInput.val();

        Swal.fire({
            title: 'Processing...',
            text: 'Requesting OTP...',
            didOpen: () => {
                Swal.showLoading();
            }
        });

        $.ajax({
            type: 'POST',
            url: subscriptionForm.attr('action'),
            data: {
                subscriber_email: email,
                action: 'requestOtp',
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                Swal.close();
                if (response.success) {
                    emailSection.addClass('d-none');
                    otpSection.removeClass('d-none');
                    hiddenEmailInput.val(email);
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.error
                    });
                }
            },
            error: function(xhr) {
                Swal.close();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred: ' + xhr.responseText
                });
            }
        });
    });

    // Handle OTP verification
    verifyOtpBtn.click(function(event) {
        event.preventDefault();
        const otp = otpInput.val();
        const email = hiddenEmailInput.val();

        Swal.fire({
            title: 'Verifying...',
            text: 'Verifying OTP...',
            didOpen: () => {
                Swal.showLoading();
            }
        });

        $.ajax({
            type: 'POST',
            url: subscriptionForm.attr('action'),
            data: {
                subscriber_email: email,
                otp_code: otp,
                action: 'verifyOtp',
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                Swal.close();
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'OTP verified successfully.'
                    }).then(() => {
                        // Redirect to the index page
                        window.location.href = '/'; // Update the URL if needed
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.error
                    });
                }
            },
            error: function(xhr) {
                Swal.close();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred: ' + xhr.responseText
                });
            }
        });
    });

    // Handle OTP resend
    resendOtpBtn.click(function(event) {
        event.preventDefault();
        const email = hiddenEmailInput.val();

        Swal.fire({
            title: 'Resending...',
            text: 'Resending OTP...',
            didOpen: () => {
                Swal.showLoading();
            }
        });

        $.ajax({
            type: 'POST',
            url: subscriptionForm.attr('action'),
            data: {
                subscriber_email: email,
                action: 'resendOtp',
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                Swal.close();
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'OTP resent successfully.'
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.error
                    });
                }
            },
            error: function(xhr) {
                Swal.close();
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred: ' + xhr.responseText
                });
            }
        });
    });
});
