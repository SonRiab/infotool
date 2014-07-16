"""
Copyright (C) 2014  Rene Jablonski

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
from datetime import timedelta
from django.views import generic
from django.utils.timezone import now
from booking.models import VisitorGroup
from django.utils.translation import get_language
from portal.models import Site


class InfoscreenView(generic.TemplateView):
    template_name = 'booking/infoscreen.html'

    def get_context_data(self, **kwargs):
        context = super(InfoscreenView, self).get_context_data(**kwargs)
        context[u'groups'] = VisitorGroup.objects.filter(
            arrival__range=(now() - timedelta(minutes=15), now() + timedelta(minutes=30)))
        site = Site.objects.filter(language__language_code=get_language(),
                                   superior_site=None,
                                   is_visible=True,).order_by(u'order').first()
        context[u'site'] = site
        context[u'current_site_id'] = site.id
        return context
