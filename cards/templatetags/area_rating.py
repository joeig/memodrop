from django import template

register = template.Library()


@register.inclusion_tag('area_rating.html')
def area_rating(area):
    areas = list()
    missing_areas = list()

    for a in range(0, area):
        areas.append(a)

    for a in range(0, 6 - area):
        missing_areas.append(a)

    return {
        'areas': areas,
        'missing_areas': missing_areas,
    }
