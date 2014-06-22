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
    language_code = models.CharField(verbose_name=_(u'Language Code'),
                                    max_length=5,
                                    help_text=_(u'Format: '
                                                u'<a href="http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes">'
                                                u'ISO 639-1</a>'))
    language = models.CharField(verbose_name=_(u'Language'),
                                max_length=255,)
    native = models.CharField(verbose_name=_(u'Language'),
                              max_length=255,)

    class Meta:
        verbose_name = _(u'Language')
        verbose_name_plural = _(u'Languages')

    def __unicode__(self):
        return self.language


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


class Site(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    superior_site = models.ForeignKey('self',
                                      verbose_name=_(u'Superior Site'),
                                      default=None,
                                      null=True,
                                      blank=True)
    order = models.PositiveSmallIntegerField(verbose_name=_(u'Site Order'),
                                             default=0,
                                             help_text=_(u'Here you can define the order of sites. '
                                                         u'Lower numbers will be displayed first.'))
    language = models.ForeignKey(Language,
                                 verbose_name=_(u'Language'),)
    title = models.CharField(verbose_name=_(u'Site Title'),
                             max_length=255,)
    content = tinymce_models.HTMLField(verbose_name=_(u'Site Content'),)
    is_visible = models.BooleanField(verbose_name=_(u'Visible'),
                                     default=False,)
    is_special = models.BooleanField(default=False,)
    audio_file = models.FileField(verbose_name=_(u'Audio File'),
                                  upload_to=u'uploads/',
                                  blank=True,)

    class Meta:
        verbose_name = _(u'Site')
        verbose_name_plural = _(u'Sites')
        ordering = [u'superior_site__title', u'language__language_code', u'order', ]

    def __unicode__(self):
        return self.title


class SpecialSite(Site):
    """
        These sites are for special usage only! Django tags stored in db will be rendered!
        So ensure only trusted users have permission to add or modify the content!
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """

    class Meta:
        verbose_name = _(u'Special Site')
        verbose_name_plural = _(u'Special Sites')
        proxy = True

    def save(self, *args, **kwargs):
        self.is_special = True
        super(SpecialSite, self).save(*args, **kwargs)


class SiteAdmin(admin.ModelAdmin):
    list_display = (u'title', u'superior_site', u'language', u'is_visible', u'order',)
    list_filter = (u'is_visible', u'language',)
    list_editable = (u'superior_site', u'is_visible', u'order',)
    exclude = (u'is_special', )

    def queryset(self, request):
        return self.model.objects.filter(is_special=False)


class SpecialSiteAdmin(admin.ModelAdmin):
    list_display = (u'title', u'superior_site', u'language', u'is_visible', u'order',)
    list_filter = (u'is_visible', u'language',)
    list_editable = (u'superior_site', u'is_visible', u'order',)
    exclude = (u'is_special', )

    def queryset(self, request):
        return self.model.objects.filter(is_special=True)


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
