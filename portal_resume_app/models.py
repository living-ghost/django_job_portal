# ================================
#          Django Imports
# ================================

from django.db import models
from portal_user_app.models import User

# ================================
#        Personal Information Model
# ================================
class PersonalInfo(models.Model):
    """
    Model to store personal information of the user.
    
    Attributes:
        user (ForeignKey): The user to whom this personal information belongs.
        name (CharField): The name of the user.
        email (EmailField): The email address of the user.
        phone (CharField): The phone number of the user.
        address (CharField): The address of the user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_infos')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# ================================
#        Summary Model
# ================================
class Summary(models.Model):
    """
    Model to store a summary or description of the user's profile.
    
    Attributes:
        user (ForeignKey): The user to whom this summary belongs.
        description (TextField): The description or summary text.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summarys')
    description = models.TextField()

    def __str__(self):
        return self.description

# ================================
#        Education Model
# ================================
class Education(models.Model):
    """
    Model to store educational qualifications of the user.
    
    Attributes:
        user (ForeignKey): The user to whom this education information belongs.
        degree (CharField): The degree obtained by the user.
        college (CharField): The name of the college where the degree was obtained.
        year (CharField): The year of graduation.
        cgpa (CharField): The CGPA or grade obtained.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    year = models.CharField(max_length=15)
    cgpa = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.degree} - {self.college}"

# ================================
#        Experience Model
# ================================
class Experience(models.Model):
    """
    Model to store professional experience of the user.
    
    Attributes:
        user (ForeignKey): The user to whom this experience information belongs.
        role (CharField): The role or job title held by the user.
        company (CharField): The name of the company where the user worked.
        year (CharField): The year or duration of the experience.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.role} at {self.company}"

# ================================
#        Language Model
# ================================
class Language(models.Model):
    """
    Model to store languages known by the user.
    
    Attributes:
        user (ForeignKey): The user to whom this language information belongs.
        language (CharField): The name of the language.
        proficiency (CharField): The proficiency level in the language.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.language} - {self.proficiency}"

# ================================
#        Project Model
# ================================
class Project(models.Model):
    """
    Model to store details of projects completed by the user.
    
    Attributes:
        user (ForeignKey): The user to whom this project information belongs.
        title (CharField): The title of the project.
        description (TextField): The description of the project.
        year (CharField): The year in which the project was completed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.CharField(max_length=15)

    def __str__(self):
        return self.title

# ================================
#        Skill Model
# ================================
class Skill(models.Model):
    """
    Model to store skills possessed by the user.
    
    Attributes:
        user (ForeignKey): The user to whom this skill information belongs.
        skill (CharField): The name of the skill.
        proficiency (CharField): The proficiency level in the skill.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.skill} - {self.proficiency}"

# ================================
#        Certificate Model
# ================================
class Certificate(models.Model):
    """
    Model to store certificates obtained by the user.
    
    Attributes:
        user (ForeignKey): The user to whom this certificate information belongs.
        certificate (CharField): The name of the certificate.
        year (CharField): The year in which the certificate was obtained.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    certificate = models.CharField(max_length=255)
    year = models.CharField(max_length=25)

    def __str__(self):
        return self.certificate

# ================================
#        Hobbie Model
# ================================
class Hobbie(models.Model):
    """
    Model to store hobbies of the user.
    
    Attributes:
        user (ForeignKey): The user to whom this hobby information belongs.
        hobbie (CharField): The name of the hobby.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hobbies')
    hobbie = models.CharField(max_length=255)

    def __str__(self):
        return self.hobbie

# ================================
#        Resume Model
# ================================
class Resume(models.Model):
    """
    Model to store resumes created by the user.
    
    Attributes:
        user (ForeignKey): The user to whom this resume belongs.
        name (CharField): The name of the resume.
        html_content (TextField): The HTML content of the resume.
        image (ImageField): An image associated with the resume.
        pdf_file (FileField): The PDF file of the resume.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=255)
    html_content = models.TextField()
    image = models.ImageField(upload_to='portal_resume_app/resumes/images/')
    pdf_file = models.FileField(upload_to='portal_resume_app/resumes/pdfs/')

    def __str__(self):
        return self.name