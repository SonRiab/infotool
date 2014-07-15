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
from portal.models import SpecialSite

register = template.Library()

@register.inclusion_tag(u'portal/nav-item.html', takes_context=True)
def nav_item(context, nav_item_id):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    item = SpecialSite.objects.filter(id=nav_item_id, is_visible=True).first()
    sub_items = SpecialSite.objects.filter(superior_site=nav_item_id, is_visible=True).order_by(u'order')
    is_selected = False
    if int(context[u'current_site_id']) == nav_item_id:
        is_selected = True
    return {
        u'nav_item': item,
        u'sub_nav_items': sub_items,
        u'is_selected': is_selected,
        u'current_site_id': context[u'current_site_id'],
    }
