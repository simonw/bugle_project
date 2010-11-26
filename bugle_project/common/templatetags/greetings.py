from django import template
import random

register = template.Library()

greetings = [
    'What ho, {{ name }}?',
    'Tally ho, {{ name}}!',
    'Pip pip, {{ name }}!',
    'Well met, {{ name }}!',
    'Good morrow, {{ name }}!',
    'Greetings and salutations, {{ name }}!',
    'Ahoi-hoi, {{ name }}!',
    'Ahoy, {{ name }}.',
    'How dost thou, {{ name }}?',
    'Greetings of the day to you, {{ name }}.',
    'Come in, {{ name }}, and know me better.',
    'How do you do, {{ name }}.',
    'Ah, {{ name }}, we meet again.',
    'Felicitations, {{ name }}.',
    'So we meet again, {{ name }} (if that <em>is</em> your real name)',
    'Pronto, {{ name }}.',
    'Well then, {{ name }}&hellip;',
    'Ah, {{ name }}, this time the advantage is mine.',
    'Fuck yeah, {{ name }}!',
    'Looks like you could use a drink, {{ name }}.',
    'Well, hello there {{ name }}.',
    'You look good today, {{ name }}.',
]

@register.simple_tag
def greeting(user):
    return template.Template(random.choice(greetings)).render(template.Context({
        'name': template.Template('{% if user.is_anonymous %}stranger{% else %}<strong><a href="/{{ user }}/">{{ user }}</a></strong>{% endif %}').render(template.Context({'user': user})),
    }))
    

