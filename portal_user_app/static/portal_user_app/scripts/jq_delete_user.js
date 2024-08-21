$(document).ready(function() {
    $('#deleteAccountBtn').on('click', function(e) {
        e.preventDefault(); // Prevent the default link behavior

        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, cancel!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: UserAcDel,  // Ensure this URL matches your view's URL
                    method: 'POST',
                    data: {
                        csrfmiddlewaretoken: '{{ csrf_token }}'  // Include CSRF token
                    },
                    success: function(response) {
                        if (response.success) {
                            Swal.fire({
                                icon: 'success',
                                title: 'Deleted!',
                                text: response.message,
                            }).then(() => {
                                window.location.href = UserIndexUrl; // Redirect after deletion
                            });
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: response.message,
                            });
                        }
                    },
                    error: function() {
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: 'An unexpected error occurred. Please try again.'
                        });
                    }
                });
            }
        });
    });
});