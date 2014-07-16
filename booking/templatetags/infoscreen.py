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
from django.utils.timezone import now
from booking.models import VisitorGroup, SeminarUnit
from datetime import datetime, timedelta
from portal.models import Site

register = template.Library()


@register.inclusion_tag(u'booking/infoscreen-tag.html')
def infoscreen(menu_site_id, *args):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    seminars_now = SeminarUnit.objects.filter(start__lt=now(), end__gt=now())

    next_seminars = SeminarUnit.objects.filter(start__range=(now(), now() + timedelta(hours=1)))

    menu = None
    if 11 <= datetime.now().hour <= 13:
        menu = Site.objects.get(id=menu_site_id)

    activity_site_ids = []
    for arg in args:
        if type(arg) is int:
            activity_site_ids.insert(len(activity_site_ids), arg)

    print next_seminars
    activities = None
    if len(activity_site_ids) != 0 and menu is None:
        #if len(seminars_now) == 0 and len(next_seminars) == 0:
            activities = Site.objects.filter(id__in=activity_site_ids)
        #elif (len(seminars_now) <= 1 and len(next_seminars) <= 1) \
        #        or (len(seminars_now) == 0 and len(next_seminars) <= 2) \
        #        or (len(next_seminars) == 0 and len(seminars_now) <= 2):
        #    activities = Site.objects.filter(id=activity_site_ids[0])

    return {
        u'seminars_now': seminars_now,
        u'next_seminars': next_seminars,
        u'menu': menu,
        u'activities': activities,
    }
