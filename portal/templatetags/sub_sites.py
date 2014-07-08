"""
Copyright (C) 2014 Rene Jablonski

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from django import template
from django.template import Template, Variable, TemplateSyntaxError, loader
from portal.models import SpecialSite

register = template.Library()


@register.simple_tag(takes_context=True)
def sub_sites(context, nav_item_id):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    sub_sites_dict = SpecialSite.objects.filter(superior_site=nav_item_id, is_visible=True).order_by(u'order')
    context[u'sub_nav_items'] = sub_sites_dict
    context[u'is_sub_item_selected'] = False
    for sites in sub_sites_dict:
        if int(context[u'current_site_id']) == sites.id:
            context[u'is_sub_item_selected'] = True
    return u''