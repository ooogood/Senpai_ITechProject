from django import template
from senpai.models import Module, Note

register = template.Library()

@register.filter
def get_dict_item(dic, key):
	return dic.get( key )