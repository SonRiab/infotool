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

from django.db import models
from django.contrib import admin
from tinymce import models as tinymce_models
from django.utils.translation import ugettext_lazy as _


class Language(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    languageCode = models.CharField(verbose_name=_(u'Language Code'),
                                    max_length=5,
                                    help_text=_(u'Format: xx_XX, ex: de_DE'))
    language = models.CharField(verbose_name=_(u'Language'),
                                max_length=255,)

    class Meta:
        verbose_name = _(u'Language')
        verbose_name_plural = _(u'Languages')

    def __unicode__(self):
        return self.language


class Room(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    number = models.CharField(verbose_name=_(u'Room Number'),
                              max_length=255,)
    name = models.CharField(verbose_name=_(u'Room Name'),
                            max_length=255,
                            blank=True, )

    class Meta:
        verbose_name = _(u'Room')
        verbose_name_plural = _(u'Rooms')

    def __unicode__(self):
        result = self.number
        if not self.name:
            result = u'%s (%s)' % (result, self.name)
        return result


class Seminar(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    start = models.DateTimeField(verbose_name=_(u'Start'),)
    end = models.DateTimeField(verbose_name=_(u'End'),)

    class Meta:
        verbose_name = _(u'Seminar')
        verbose_name_plural = _(u'Seminars')

    def __unicode__(self):
        return u'%s %s - %s' % (_(u'Seminar'),
                                self.start.strftime('%d.%m.%y %H:%M'),
                                self.end.strftime('%d.%m.%y %H:%M'))


class SeminarUnit(models.Model):
    """
        This is the link between a seminar and rooms

        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    start = models.DateTimeField(verbose_name=_(u'Start'),)
    end = models.DateTimeField(verbose_name=_(u'End'),)
    seminar = models.ForeignKey(Seminar,
                                verbose_name=_(u'Seminar'),)
    room = models.ForeignKey(Room,
                             verbose_name=_(u'Room'),)

    class Meta:
        verbose_name = _(u'Seminar Unit')
        verbose_name_plural = _(u'Seminar Units')

    def __unicode__(self):
        return u'%s (%s %s)' % (self.seminar.seminarextended_set.filter(seminar__id=self.seminar.id,
                                                                        language__languageCode="de_DE").title,
                                _('Room'),
                                self.room.number)


class SeminarExtended(models.Model):
    """
        This is an extention to the seminar to provide language support
        for title and description

        :Author:    Rene Jablonski
        :contact:   rene@vnull.de
    """
    seminar = models.ForeignKey(Seminar,
                                verbose_name=_(u'Seminar'),)
    language = models.ForeignKey(Language,
                                 verbose_name=_(u'Language'),)
    title = models.CharField(verbose_name=_(u'Title'),
                             max_length=255,)
    description = models.TextField(verbose_name=_(u'Description'),
                                   blank=True,)

    class Meta:
        verbose_name = _(u'Extended Seminar Information')
        verbose_name_plural = _(u'Extended Seminar Informations')

    def __unicode__(self):
        return self.title


class Contact(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    prename = models.CharField(verbose_name=_(u'Prename'),
                               max_length=255,)
    name = models.CharField(verbose_name=_(u'Name'),
                            max_length=255,)
    email = models.CharField(verbose_name=_(u'Email'),
                             max_length=255,
                             blank=True,
                             default=u"",)

    # the mobile and telephone number aren't in use
    # mobile = models.CharField(max_length=255)
    #tel = models.CharField(max_length=255)
    # #room = models.ForeignKey(Room, null=True)

    class Meta:
        verbose_name = _(u'Contact')
        verbose_name_plural = _(u'Contacts')

    def contact_name(self):
        return u'%s %s' % (self.prename, self.name)

    contact_name.short_description = _(u'Contact Name')

    def __unicode__(self):
        return u'%s (%s)' % (self.contact_name(), self.email)


class ContactAdmin(admin.ModelAdmin):
    list_display = (u'prename', u'name', u'email',)
    list_display_links = (u'prename', u'name', u'email',)
    search_fields = (u'prename', u'name', u'email',)


class VisitorGroup(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    groupname = models.CharField(verbose_name=_(u'Groupname'),
                                 max_length=255,)
    arrival = models.DateTimeField(verbose_name=_(u'Arrival'),)
    departure = models.DateTimeField(verbose_name=_(u'Departure'),)
    language = models.ForeignKey(Language,
                                 verbose_name=_(u'Language'),)
    contact = models.ForeignKey(Contact,
                                verbose_name=_(u'Contact'),)
    seminar = models.ForeignKey(Seminar,
                                verbose_name=_(u'Seminar'),)
    room = models.ManyToManyField(Room,
                                  verbose_name=_(u'Room'),)

    class Meta:
        verbose_name = _(u'Visitor Group')
        verbose_name_plural = _(u'Visitor Groups')

    def __unicode__(self):
        return u'%s (%s)' % (self.groupname, self.contact.name)


class NavigationItem(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    language = models.ForeignKey(Language,
                                 verbose_name=_(u'Language'),)
    name = models.CharField(verbose_name=_(u'Navigation Title'),
                            max_length=255,)

    class Meta:
        verbose_name = _(u'Navigation Item')
        verbose_name_plural = _(u'Navigation Items')

    def __unicode__(self):
        return self.name


class NavigationItemAdmin(admin.ModelAdmin):
    list_filter = (u'language__language',)


class Site(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    navigation_item = models.ForeignKey(NavigationItem,
                                        verbose_name=_(u'Navigation Item'),)
    title = models.CharField(verbose_name=_(u'Site Title'),
                             max_length=255,)
    content = tinymce_models.HTMLField(verbose_name=_(u'Site Content'),)
    visible = models.BooleanField(verbose_name=_(u'Visible'),
                                  default=False,)
    audio_file = models.FileField(verbose_name=_(u'Audio File'),
                                  upload_to=u'uploads/',
                                  blank=True,)

    class Meta:
        verbose_name = _(u'Site')
        verbose_name_plural = _(u'Sites')

    def site_language(self):
        return self.navigation_item.language.language

    def __unicode__(self):
        return self.title


class SiteAdmin(admin.ModelAdmin):
    list_display = (u'title', u'navigation_item', u'site_language', u'visible',)
    list_filter = (u'visible', u'navigation_item__name', u'navigation_item__language__language',)
    list_editable = (u'navigation_item', u'visible',)


class Category(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    language = models.ForeignKey(Language,
                                 verbose_name=_(u'Language'),)
    contact = models.ForeignKey(Contact,
                                verbose_name=_(u'Contact'),)
    visible = models.BooleanField(verbose_name=_(u'Visible'),
                                  default=False,)
    name = models.CharField(verbose_name=_(u'Category Name'),
                            max_length=255,)
    placeholder = models.CharField(verbose_name=_(u'Category Placholder'),
                                   max_length=255,
                                   help_text=_(u'Placeholder text which will be displayed in the form as hint.'),)

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return self.name


class CategoryAdmin(admin.ModelAdmin):
    list_display = (u'name', u'contact', u'visible',)
    list_editable = (u'contact', u'visible',)
    list_filter = (u'contact__email', u'visible',)


class FeedbackCategory(Category):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """

    class Meta:
        verbose_name = _(u'Feedback Category')
        verbose_name_plural = _(u'Feedback Categories')


class DamageCategory(Category):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """

    class Meta:
        verbose_name = _(u'Damage Category')
        verbose_name_plural = _(u'Damage Categories')
