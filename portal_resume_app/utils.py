from .models import PersonalInfo, Education, Experience,  Language, Project, Certificate, Hobbie, Skill, Summary

def get_user_data(user):

    personal_data = PersonalInfo.objects.filter(user=user).first()
    education_data = Education.objects.filter(user=user)
    experience_data = Experience.objects.filter(user=user)
    language_data = Language.objects.filter(user=user)
    project_data = Project.objects.filter(user=user)
    certificate_data = Certificate.objects.filter(user=user)
    hobbie_data = Hobbie.objects.filter(user=user)
    skill_data = Skill.objects.filter(user=user)
    summary_data = Summary.objects.filter(user=user).first()

    return personal_data, education_data, experience_data, language_data, project_data, certificate_data, hobbie_data, skill_data, summary_data