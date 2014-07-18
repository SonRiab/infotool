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
from portal.models import Site, SpecialSite, Language, Category
from portal.forms import FeedbackForm, DamageReportForm
from django.utils.translation import get_language
from django.core import serializers
import re


def generic_context_data(context, request):

    context[u'nav_items'] = Site.objects.filter(language__language_code=get_language(),
                                                superior_site=None,
                                                is_visible=True).order_by(u'order')
    context[u'supported_languages'] = Language.objects.all().order_by(u'native')
    context[u'redirect_url'] = u'http://%s%s' % (request.get_host(),
                                                 request.get_full_path(),)
    return context


class IndexView(generic.TemplateView):
    model = SpecialSite
    template_name = u'portal/site.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(generic_context_data(context, self.request))
        site = Site.objects.filter(language__language_code=get_language(),
                                   superior_site=None,
                                   is_visible=True,).order_by(u'order').first()
        context[u'site'] = site
        context[u'current_site_id'] = site.id
        context[u'is_selected'] = True
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
        context.update(generic_context_data(context, self.request))
        pattern = re.compile(u'^.+/site/(?P<pk>\d+)/$')
        match = pattern.match(self.request.path_info)
        context[u'current_site_id'] = match.group(u'pk')

        return context


class FeedbackView(generic.FormView):
    form_class = FeedbackForm
    template_name = u'portal/contact-form.html'
    success_url = u'success/'

    def form_valid(self, form):
        form.send_mail()
        return super(FeedbackView, self).form_valid(form)

    def form_invalid(self, form):
        return super(FeedbackView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(FeedbackView, self).get_context_data(**kwargs)
        context.update(generic_context_data(context, self.request))
        context[u'is_feedback_selected'] = True
        context[u'action_url'] = u'feedback/'
        context[u'current_site_id'] = -1
        context[u'placeholders'] = serializers.serialize('json', Category.objects.filter(
            is_visible=True,
            language__language_code=get_language().split('-')[0]).order_by(u'name'),)
        return context


class DamageReportView(generic.FormView):
    form_class = DamageReportForm
    template_name = u'portal/contact-form.html'
    success_url = u'success/'

    def form_valid(self, form):
        form.send_mail()
        return super(DamageReportView, self).form_valid(form)

    def form_invalid(self, form):
        return super(DamageReportView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(DamageReportView, self).get_context_data(**kwargs)
        context.update(generic_context_data(context, self.request))
        context[u'is_damage_report_selected'] = True
        context[u'action_url'] = u'damage-report/'
        context[u'current_site_id'] = -1
        context[u'placeholders'] = serializers.serialize('json', Category.objects.filter(
            is_visible=True,
            language__language_code=get_language().split('-')[0]).order_by(u'name'),)
        return context


class FormSuccessView(generic.TemplateView):
    template_name = 'portal/contact-success.html'

    def get_context_data(self, **kwargs):
        context = super(FormSuccessView, self).get_context_data(**kwargs)
        context.update(generic_context_data(context, self.request))
        context[u'current_site_id'] = -1
        return context


class PoweredByView(generic.TemplateView):
    template_name = 'portal/powered-by.html'

    def get_context_data(self, **kwargs):
        context = super(PoweredByView, self).get_context_data(**kwargs)
        context.update(generic_context_data(context, self.request))
        context[u'current_site_id'] = -1
        return context
