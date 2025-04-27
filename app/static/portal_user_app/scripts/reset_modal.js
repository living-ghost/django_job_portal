document.addEventListener('DOMContentLoaded', function () {
    const resetPasswordBtn = document.getElementById('resetPasswordBtn');
    const resetPasswordModal = new bootstrap.Modal(document.getElementById('resetPasswordModal'));
    const resetPasswordForm = document.getElementById('resetPasswordForm');

    // Show the modal when the button is clicked
    resetPasswordBtn.addEventListener('click', function () {
        resetPasswordModal.show();
    });

    // Handle form submission
    resetPasswordForm.addEventListener('submit', function (event) {
        event.preventDefault();  // Prevent default form submission

        const formData = new FormData(resetPasswordForm);
        
        Swal.fire({
            title: 'Processing...',
            text: 'Please wait while we process your request.',
            didOpen: () => {
                Swal.showLoading();
            }
        });

        fetch(UserPwdReset, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            Swal.close();  // Close the processing alert
            if (data.error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: data.error,
                });
            } else {
                Swal.fire({
                    icon: 'success',
                    title: 'Success!',
                    text: 'Your password was successfully updated!',
                    showConfirmButton: false,
                    timer: 1500  // Optional: auto-close the alert after 1.5 seconds
                }).then(() => {
                    // Redirect to dashboard after showing success message
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                });
            }
        })
        .catch(error => {
            Swal.close();  // Close the processing alert
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'An unexpected error occurred.',
            });
        });
    });
});