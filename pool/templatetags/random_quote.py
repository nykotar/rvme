import datetime
from django import template
from random import randint

register = template.Library()

quotes = (('Work practice targets until the ego has been dismantled, beaten, and retired.', 'Edward Riordan'),
          ('Structure! Content be damned!', 'Rob Cowart'),
          ('In order to be right, you have to be willing to be wrong.', 'Russell Targ'),
          ('Practice practice practice!', 'Everyone'))

@register.simple_tag
def random_quote():
    sel_quote = quotes[randint(0, len(quotes)-1)]
    quote = f'<p class="mb-0">{sel_quote[0]}</p>'
    author = f'<footer class="blockquote-footer">{sel_quote[1]}</footer>'
    return quote + author