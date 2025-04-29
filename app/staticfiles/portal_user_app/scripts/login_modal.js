document.addEventListener('DOMContentLoaded', function () {
    // Modal instances
    var LoginModal = new bootstrap.Modal(document.getElementById('LoginModal'));
    var RegisterModal = new bootstrap.Modal(document.getElementById('RegisterModal'));
    var OtpModal = new bootstrap.Modal(document.getElementById('OtpModal'));
    var ForgotPWDModal = new bootstrap.Modal(document.getElementById('ForgotPWDModal'));
    var ContactUsModal = new bootstrap.Modal(document.getElementById('ContactUsModal'));

    // Button elements
    var LoginBtn1 = document.getElementById('LoginBtn1');
    var LoginBtn2 = document.getElementById('LoginBtn2');
    var LoginBtn3 = document.getElementById('LoginBtn3');
    var ContactUsModal1 = document.getElementById('ContactUsModal1');
    var ContactUsModal2 = document.getElementById('ContactUsModal2');
    var ContactUsModal3 = document.getElementById('ContactUsModal3');
    var RegisterBtn = document.getElementById('RegisterBtn');
    var ForgotPWDBtn = document.getElementById('ForgotPWDBtn');
    
    // Handle showing modals
    LoginBtn1.addEventListener('click', function () {
        LoginModal.show();
    });
    LoginBtn2.addEventListener('click', function () {
        LoginModal.show();
    });
    LoginBtn3.addEventListener('click', function () {
        LoginModal.show();
    });
    ContactUsModal1.addEventListener('click', function () {
        ContactUsModal.show();
    });
    ContactUsModal2.addEventListener('click', function () {
        ContactUsModal.show();
    });
    ContactUsModal3.addEventListener('click', function () {
        ContactUsModal.show();
    });
    ForgotPWDBtn.addEventListener('click', function () {
        ForgotPWDModal.show();
    });

    RegisterBtn.addEventListener('click', function () {
        RegisterModal.show();
        LoginModal.hide();
    });

    // Handle login form submission
    document.getElementById('LoginForm').addEventListener('submit', function (e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const submitButton = document.querySelector('#LoginForm button[type="submit"]');
        const originalButtonText = submitButton.innerHTML;

        // Disable the submit button and show loading effect
        submitButton.disabled = true;
        submitButton.innerHTML = 'Authenticating...';

        // Optionally, show a loading spinner
        const spinner = document.createElement('span');
        spinner.className = 'spinner-border spinner-border-sm'; // Bootstrap spinner class
        submitButton.appendChild(spinner);

        fetch(UserLoginUrl, { // Make sure `UserLoginUrl` is defined with the correct endpoint
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            if (data.redirect) {
                // Redirect on successful login
                // Redirect to dashboard after a delay to show Swal.fire
                const delay = 500; // Delay in milliseconds

                Swal.fire({
                    icon: 'success',
                    title: 'Success!',
                    text: 'Successfully Authenticated'
                }).then(() => {
                    // Wait for the Swal.fire to close before redirecting
                    setTimeout(() => {
                        window.location.href = UserDashboard;
                    }, delay); // Delay before redirection
                });
            } else if (data.error) {
                // Show error message using SweetAlert
                Swal.fire({
                    icon: 'error',
                    title: 'Login Error',
                    text: data.error
                }).then(() => {
                    // Re-enable the submit button after showing the error message
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalButtonText; // Restore original text
                    if (spinner) {
                        submitButton.removeChild(spinner);
                    }
                });
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'An unexpected error occurred. Please try again.'
            }).then(() => {
                // Re-enable the submit button after showing the error message
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText; // Restore original text
                if (spinner) {
                    submitButton.removeChild(spinner);
                }
            });
        });
    });

    // Handle registration form submission
    document.getElementById('RegisterForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const otpButton = document.getElementById('OtpBtn');
        const originalButtonText = otpButton.innerHTML;

        // Disable the button and show loading effect
        otpButton.disabled = true;
        otpButton.innerHTML = 'Processing...';

        // Optionally, show a loading spinner
        const spinner = document.createElement('span');
        spinner.className = 'spinner-border spinner-border-sm'; // Bootstrap spinner class
        otpButton.appendChild(spinner);

        fetch(UserRegUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                RegisterModal.hide(); // Hide Register Modal
                OtpModal.show();     // Show OTP Modal
            } else if (data.error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: data.error
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'An unexpected error occurred. Please try again.'
            });
        })
        .finally(() => {
            // Re-enable the button and restore original text
            otpButton.disabled = false;
            otpButton.innerHTML = originalButtonText;
            if (spinner) {
                otpButton.removeChild(spinner);
            }
        });
    });

    // Handle OTP verification form submission
    document.getElementById('otpForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        formData.append('action', 'verify_otp'); // Ensure action is included

        const verifyButton = document.getElementById('verifyButton');
        const originalButtonText = verifyButton.innerHTML;

        // Disable the button and show loading effect
        verifyButton.disabled = true;
        verifyButton.innerHTML = 'Verifying...';

        const spinner = document.createElement('span');
        spinner.className = 'spinner-border spinner-border-sm'; // Bootstrap spinner class
        verifyButton.appendChild(spinner);

        fetch(UserRegVotpUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success!',
                    text: 'Account Created successfully!'
                }).then(() => {
                    window.location.href = UserIndexUrl;
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Invalid OTP',
                    text: 'Please try again.'
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'An unexpected error occurred. Please try again.'
            });
        })
        .finally(() => {
            verifyButton.disabled = false;
            verifyButton.innerHTML = originalButtonText;
            if (spinner) {
                verifyButton.removeChild(spinner);
            }
        });
    });

    // Handle OTP resend button
    document.getElementById('resendButton').addEventListener('click', function () {
        const resendButton = this;
        const originalButtonText = resendButton.innerHTML;
        
        resendButton.disabled = true;
        resendButton.innerHTML = 'Processing...';

        const spinner = document.createElement('span');
        spinner.className = 'spinner-border spinner-border-sm'; // Bootstrap spinner class
        resendButton.appendChild(spinner);

        fetch(UserRegVotpUrl, {
            method: 'POST',
            body: new URLSearchParams({ 'action': 'resend_otp' }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.resend) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success!',
                    text: 'OTP has been resent to your email.'
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error resending OTP. Please try again.'
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'An unexpected error occurred. Please try again.'
            });
        })
        .finally(() => {
            resendButton.disabled = false;
            resendButton.innerHTML = originalButtonText;
            if (spinner) {
                resendButton.removeChild(spinner);
            }
        });
    });

    // Handle forgot password form submission
    document.getElementById('ForgotPWDForm').addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        const formData = new FormData(this);
        const forgotPWDButton = document.querySelector('#ForgotPWDForm button[type="submit"]');
        const originalButtonText = forgotPWDButton.innerHTML;

        forgotPWDButton.disabled = true;
        forgotPWDButton.innerHTML = 'Reset in progress...';

        const spinner = document.createElement('span');
        spinner.className = 'spinner-border spinner-border-sm'; // Bootstrap spinner class
        forgotPWDButton.appendChild(spinner);

        fetch(UserForgotUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Indicate that this is an AJAX request
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                ForgotPWDModal.hide();
                LoginModal.show();
                Swal.fire({
                    icon: 'success',
                    title: 'Success!',
                    text: 'Check your mailbox for temporary password'
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: data.error
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'An unexpected error occurred. Please try again.'
            });
        })
        .finally(() => {
            forgotPWDButton.disabled = false;
            forgotPWDButton.innerHTML = originalButtonText;
            if (spinner) {
                forgotPWDButton.removeChild(spinner);
            }
        });
    });
});