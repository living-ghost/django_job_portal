function getCSRFToken() {
    return $('input[name="csrfmiddlewaretoken"]').val();
}

function submitForm(formId) {
    var form = $('#' + formId);
    var formData = form.serialize(); // Serialize the form data

    // Prevent default form submission (in case it's triggered manually)
    form.on('submit', function(event) {
        event.preventDefault(); // Prevent full-page reload on form submit
    });

    $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: formData,
        headers: {
            'X-CSRFToken': getCSRFToken() // Include CSRF token in headers
        },
        success: function(response) {
            if (response.success) {
                location.reload();
                alert(response.message);
            } else {
                alert('Server responded with an error: ' + response.message);
            }
        },
        error: function(xhr, status, error) {
            var errorMessage = xhr.responseText || 'An unknown error occurred.';
            alert('AJAX request failed: ' + errorMessage);
        }
    });
}

//

function deleteHobbie(hobbieId) {
    if (confirm('Are you sure you want to delete this hobby?')) {
        fetch(DelHobURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'hobbie_id': hobbieId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload the page to reflect changes
            } else {
                alert('Failed to delete hobby.');
            }
        });
    }
}

function deleteSkill(skillId) {
    if (confirm('Are you sure you want to delete this skill?')) {
        fetch(DelSkillURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'skill_id': skillId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload the page to reflect changes
            } else {
                alert('Failed to delete skill.');
            }
        });
    }
}

function deleteCertificate(certificateId) {
    if (confirm('Are you sure you want to delete this certificate?')) {
        fetch(DelCertiURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'certificate_id': certificateId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload the page to reflect changes
            } else {
                alert('Failed to delete certificate.');
            }
        });
    }
}

function deleteProject(projectId) {
    if (confirm('Are you sure you want to delete this project?')) {
        fetch(DelProURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'project_id': projectId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload the page to reflect changes
            } else {
                alert('Failed to delete project.');
            }
        });
    }
}

function deleteLanguage(languageId) {
    if (confirm('Are you sure you want to delete this language?')) {
        fetch(DelLangURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'language_id': languageId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload the page to reflect changes
            } else {
                alert('Failed to delete language.');
            }
        });
    }
}

function deleteExperience(experienceId) {
    if (confirm('Are you sure you want to delete this experience?')) {
        fetch(DelExpURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'experience_id': experienceId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload the page to reflect changes
            } else {
                alert('Failed to delete experience.');
            }
        });
    }
}

function deleteEducation(educationId) {
    if (confirm('Are you sure you want to delete this experience?')) {
        fetch(DelEduURL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'education_id': educationId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload(); // Reload the page to reflect changes
            } else {
                alert('Failed to delete education.');
            }
        });
    }
}