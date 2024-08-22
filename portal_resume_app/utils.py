from .models import PersonalInfo, Education, Experience, Language, Project, Certificate, Hobbie, Skill, Summary

def get_user_data(user):
    """
    Retrieve and return all relevant data for a specific user.

    Args:
        user (User): The user for whom data is being retrieved.

    Returns:
        tuple: A tuple containing:
            - personal_data (PersonalInfo): The personal information of the user.
            - education_data (QuerySet): The user's education data.
            - experience_data (QuerySet): The user's experience data.
            - language_data (QuerySet): The user's language data.
            - project_data (QuerySet): The user's project data.
            - certificate_data (QuerySet): The user's certificate data.
            - hobbie_data (QuerySet): The user's hobbie data.
            - skill_data (QuerySet): The user's skill data.
            - summary_data (Summary): The user's summary information.
    """
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