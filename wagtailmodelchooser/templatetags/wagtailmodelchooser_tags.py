from django import template

register = template.Library()


@register.filter
def getattr(obj, attr_name):
    try:
        assert obj is not None
        return obj.__getattribute__(attr_name)
    except AttributeError:
        return obj.__dict__.get(attr_name, '')
    except:
        return ''
