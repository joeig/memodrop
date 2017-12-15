from django import template

register = template.Library()


@register.inclusion_tag('templatetags/card_controls.html')
def card_controls(card):
    """Display control buttons for managing one single card
    """
    return {
        'card': card,
    }
