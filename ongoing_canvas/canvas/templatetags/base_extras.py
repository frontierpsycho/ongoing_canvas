from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
	if request.path in (reverse(url) for url in  urls.split()):
		return "active"
	return ""

@register.filter
def format(value, arg):
	"""
	Alters default filter "stringformat" to not add the % at the front,
	so the variable can be placed anywhere in the string.
	"""
	try:
		if value:
			return (unicode(arg)) % value
		else:
			return u''
	except (ValueError, TypeError):
		return u''
