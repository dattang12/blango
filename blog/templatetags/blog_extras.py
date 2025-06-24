from django.contrib.auth.models import User
from django import template
from django.utils.html import format_html
from django.utils import timezone
from blog.models import Post

register = template.Library()

@register.filter
def author_details(author, current_user):
  if not isinstance(author, User):
    return ""

  if author == current_user:
    return format_html('<strong> {} </strong>', author.username)
  if author.first_name and author.last_name:
    name = f"{author.first_name} {author.last_name}"
  else: 
    name = author.username

  if author.email:
    preffix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html('</a>')
  else: 
    preffix = ""
    suffix = ""
  return format_html('{}{}{}', preffix, name, suffix)

@register.simple_tag
def row(extra_class=""):
  if extra_class:
    return format_html('<div class="row {}">', extra_class)
  return format_html('<div class="row">')

@register.simple_tag
def endrow():
  return format_html('</div>')

@register.simple_tag
def col(extra_class=""):
  if extra_class:
    return format_html('<div class="col {}">', extra_class)
  return format_html('<div class="col">')

@register.simple_tag
def endcol():
  return format_html('</div>')


@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.filter(published_at__lte=timezone.now()).exclude(id=post.id)[:5]
  return {
    'title' : 'Recent Posts',
    'posts' : posts,
  }