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
from django.template import TemplateSyntaxError, loader
from booking.models import VisitorGroup
from datetime import datetime
from pytz import timezone

register = template.Library()


class GroupListNode(template.Node):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    def render(self, context):
        groups_template = loader.get_template(u'booking/groups.html')
        context[u'all_groups'] = VisitorGroup.objects.filter(arrival__lt=datetime.now(tz=timezone('Europe/Berlin')),
                                                             departure__gt=datetime.now(tz=timezone('Europe/Berlin')))
        return groups_template.render(context)


@register.tag
def group_list(parser, token):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    bits = token.split_contents()
    if len(bits) != 1:
        raise TemplateSyntaxError("'%s' takes no argument" % bits[0])
    return GroupListNode()
