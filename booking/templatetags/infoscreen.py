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
from booking.models import VisitorGroup, SeminarUnit
from datetime import datetime, timedelta
from pytz import timezone

register = template.Library()

@register.inclusion_tag(u'booking/infoscreen.html')
def infoscreen(menu_site_id):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    group = VisitorGroup.objects.filter(arrival__range=(
        datetime.now(tz=timezone('Europe/Berlin')) - timedelta(minutes=15),
        datetime.now(tz=timezone('Europe/Berlin')) + timedelta(hours=1))).first()
    print group
    first_unit = None
    if group is not None:
        first_unit = SeminarUnit.objects.filter(seminar=group.seminar).order_by('start').first()
    print first_unit
    return {
        u'group': group,
        u'first_unit': first_unit,
    }
