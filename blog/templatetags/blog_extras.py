
from django.contrib.auth import get_user_model
user_model = get_user_model()
print(user_model)
from django import template
from django.utils.html import escape 
from django.utils.safestring import mark_safe
from django.utils.html import format_html

register = template.Library()

@register.filter
def author_details(author, current_user):
  if not isinstance(author, user_model):
    return ""

  if author == current_user:
    return format_html("<strong>me</strong>")
    
  if author.first_name and author.last_name:
    name = escape(f"{author.first_name} {author.last_name}")
  else:
    name = escape(f"{author.username}")

  if author.email:
    email = escape(author.email)
    prefix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html("</a>")
  else:
    prefix = ""
    suffix = ""
  
  return format_html("{}{}{}", prefix, name, suffix)
  