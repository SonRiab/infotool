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
from django import forms
from portal.models import FeedbackCategory, DamageCategory, Category
from django.utils.translation import get_language
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _


class GenericContactForm(forms.Form):
    subject = forms.CharField(label=_(u'Subject'),
                              max_length=100)
    #name = forms.CharField(label=_(u'Name'),
    #                       max_length=100,
    #                       help_text=_(u'Required'))
    #mail = forms.EmailField(label=_(u'E-Mail'),
    #                        help_text=_(u'Required'))
    message = forms.CharField(label=_(u'Message'),
                              widget=forms.Textarea,
                              help_text=_(u'Required'))

    def send_mail(self):
        category = Category.objects.filter(id=self.cleaned_data[u'subject']).first()
        subject = category.name
        #name = self.cleaned_data['name']
        #mail = self.cleaned_data['mail']
        message = self.cleaned_data['message']
        #body = _(u'Name: %s\nEmail: %s\nMessage:\n%s') % (name, mail, message)
        body = message
        contact = "%s %s <%s>" % (category.contact.prename, category.contact.name, category.contact.email)
        send_mail(subject, body, u'rene@p-pchen.de', (contact,), fail_silently=False)
        print("send mail\nto: %s\nsubject: %s\nmessage:\n%s" % (contact, subject, body))


class FeedbackForm(GenericContactForm):
    categories = FeedbackCategory.objects.filter(
        is_visible=True,
        language__language_code=get_language().split('-')[0]
    ).order_by(u'name')
    subject = forms.ChoiceField(
        label=_(u'Subject'),
        widget=forms.Select,
        choices=categories.values_list('id', 'name'))


class DamageReportForm(GenericContactForm):
    categories = DamageCategory.objects.filter(
        is_visible=True,
        language__language_code=get_language().split('-')[0]
    ).order_by(u'name')
    subject = forms.ChoiceField(
        label=_(u'Subject'),
        widget=forms.Select,
        choices=categories.values_list('id', 'name'))
