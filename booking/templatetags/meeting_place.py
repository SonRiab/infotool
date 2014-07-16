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
from booking.models import SeminarUnit, VisitorGroup

register = template.Library()


@register.simple_tag(takes_context=True)
def meeting_place(context, group_id):
    group = VisitorGroup.objects.get(id=group_id)
    first_seminar_unit = SeminarUnit.objects.filter(seminar=group.seminar).order_by('start').first()
    context[u'meeting_place'] = first_seminar_unit.room
    return u''
