from django import template
from django.template.defaulttags import register

register = template.Library()


def get_pic(dictionary, key):
    return dictionary[key]

register.filter('get_pic', get_pic)
