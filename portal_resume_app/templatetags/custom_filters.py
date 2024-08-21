from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name='format_description')
def format_description(description):
    # Split description into lines
    lines = description.split('\n')
    
    # Format as bullet points if more than 5 lines, otherwise as a paragraph
    if len(lines) > 1:  # Adjust the number of lines as needed
        formatted_description = '<ul class="project-description">{}</ul>'.format(''.join(f'<li>{line}</li>' for line in lines))
    else:
        formatted_description = f'<p class="project-description">{description}</p>'
    
    return format_html(formatted_description)