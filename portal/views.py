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

from django.views import generic
from portal.models import Site, SpecialSite
from django.utils.translation import get_language


class IndexView(generic.TemplateView):
    model = SpecialSite
    template_name = u'portal/site.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context[u'nav_items'] = Site.objects.filter(language__language_code=get_language(),
                                                    superior_site=None,
                                                    is_visible=True).order_by(u'order')
        context[u'site'] = Site.objects.filter(language__language_code=get_language(),
                                               superior_site=None,
                                               is_visible=True,).order_by(u'order').first()
        return context


class SiteView(generic.DetailView):
    model = SpecialSite
    template_name = u'portal/site.html'
    context_object_name = u'site'

    def get_queryset(self):
        return Site.objects.filter(language__language_code=get_language(),
                                   is_visible=True)

    def get_context_data(self, **kwargs):
        context = super(SiteView, self).get_context_data(**kwargs)
        context[u'nav_items'] = Site.objects.filter(language__language_code=get_language(),
                                                    superior_site=None,
                                                    is_visible=True).order_by(u'order')
        return context
