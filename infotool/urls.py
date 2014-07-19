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

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from portal import views as portal_views
from booking import views as booking_views
from filebrowser.sites import site

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', portal_views.IndexView.as_view(), name='index'),
    url(r'^submit/feedback/(?P<current_site_id>\d+)/$', portal_views.submit_feedback, name='feedback'),
    url(r'^submit/report/(?P<current_site_id>\d+)/$', portal_views.submit_report, name='report'),
    url(r'^$', portal_views.IndexView.as_view(), name='index'),
    url(r'^powered-by/$', portal_views.PoweredByView.as_view(), name='powered_by'),
    url(r'^infoscreen/$', booking_views.InfoscreenView.as_view(), name='infoscreen'),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
)

site_pattern = patterns('',
    url(r'(?P<pk>\d+)/', portal_views.SiteView.as_view(), name='site'),
)

urlpatterns += i18n_patterns('',
    url(r'^$', portal_views.IndexView.as_view(), name='lang_index'),
    url(r'site/', include(site_pattern), ),
    url(r'(?P<pk>\d+)/success/$', portal_views.FormSuccessView.as_view(), name='success'),
)
