from django import template
from django.template import Template, Variable, TemplateSyntaxError, loader
from portal.models import SpecialSite

register = template.Library()


class NavigationItemNode(template.Node):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    def __init__(self, site_id):
        self.site_id = site_id

    def render(self, context):
        nav_item_template = loader.get_template(u'portal/nav_item.html')
        context[u'nav_item'] = SpecialSite.objects.filter(id=self.site_id, is_visible=True).first()
        context[u'sub_nav_items'] = SpecialSite.objects.filter(superior_site=self.site_id, is_visible=True)\
            .order_by(u'order')
        context[u'is_selected'] = False
        if int(context[u'current_site_id']) == self.site_id:
            context[u'is_selected'] = True

        return nav_item_template.render(context)


@register.simple_tag(takes_context=True)
def nav_item(context, nav_item_id):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    #bits = token.split_contents()
    #if len(bits) != 2:
    #    raise TemplateSyntaxError("'%s' takes one argument, the site id" % bits[0])
    return NavigationItemNode(site_id=nav_item_id, )
