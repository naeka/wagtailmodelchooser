from __future__ import absolute_import, unicode_literals

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


# TODO:
# Remove the `captureas` tag as soon as Django 1.8 support is dropped
# (should use blocktrans.asvar instead)
# From: https://www.djangosnippets.org/snippets/545/

@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''
