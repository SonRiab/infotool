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
from django.core import serializers
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from portal.forms import FeedbackForm
from portal.models import Category

register = template.Library()


@register.inclusion_tag(u'portal/contact-form.html', takes_context=True)
def feedback_form(context):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    request = context['request']
    print request
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.send_mail()
            return HttpResponseRedirect('success/')

    # if a GET (or any other method) we'll create a blank form
    placeholders = serializers.serialize('json', Category.objects.filter(
        is_visible=True,
        language__language_code=get_language().split('-')[0]).order_by(u'name'),)
    form = FeedbackForm()
    return {
        'form': form,
        'view_name': 'feedback',
        'placeholders': placeholders,
        'current_site_id': context['current_site_id'],
    }
