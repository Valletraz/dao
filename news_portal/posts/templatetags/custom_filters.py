from django import template

register = template.Library()

bad_words = [
    'Fuck',
]


def new_word(bw):
    return bw[0] + '***'


@register.filter()
def censor(value):
    for item in bad_words:
        if item in value:
            return value.replace(item, new_word(item))
        else:
            return value
