from django import template

register = template.Library()


@register.inclusion_tag('templatetags/card_controls.html', takes_context=True)
def card_controls(context, card_placement):
    """Display control buttons for managing one single card
    """
    return {
        'user': context['user'],
        'card_placement': card_placement,
    }
