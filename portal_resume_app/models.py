from django.db import models
from portal_user_app.models import User

class PersonalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_infos')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summarys')
    description = models.TextField()

    def __str__(self):
        return self.description

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    year = models.CharField(max_length=15)
    cgpa = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.degree} - {self.college}"

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.role} at {self.company}"

class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.language} - {self.proficiency}"

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.CharField(max_length=15)

    def __str__(self):
        return self.title

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.skill} - {self.proficiency}"
    
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    certificate = models.CharField(max_length=255)
    year = models.CharField(max_length=25)

    def __str__(self):
        return self.certificate
    
class Hobbie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hobbies')
    hobbie = models.CharField(max_length=255)

    def __str__(self):
        return self.hobbie
    
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=255)
    html_content = models.TextField()
    image = models.ImageField(upload_to='portal_resume_app/resumes/images/')
    pdf_file = models.FileField(upload_to='portal_resume_app/resumes/pdfs/')

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name