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
from portal.models import Language, Contact
from django.utils.translation import ugettext_lazy as _


class House(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    name = models.CharField(verbose_name=_(u'House Name'),
                            max_length=255,)

    class Meta:
        verbose_name = _(u'House')
        verbose_name_plural = _(u'Houses')

    def __unicode__(self):
        return self.name


class Room(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    number = models.CharField(verbose_name=_(u'Room Number'),
                              max_length=255,)
    name = models.CharField(verbose_name=_(u'Room Name'),
                            max_length=255,
                            blank=True,)
    floor = models.IntegerField(verbose_name=_(u'Floor'))
    house = models.ForeignKey(House,
                              verbose_name=_(u'House'))

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
    # maybe these informations could be interesting but now we do not need them
    #start = models.DateTimeField(verbose_name=_(u'Start'),
    #                             blank=True,
    #                             null=True)
    #end = models.DateTimeField(verbose_name=_(u'End'),
    #                           blank=True,
    #                           null=True)
    internal_title = models.CharField(verbose_name=_(u'Internal Title'),
                                      max_length=255,
                                      help_text=_(u'This internal title is never displayed. Please use "Extented '
                                                  u'Seminar Informations" to provide multilingual titles.'))
    contact = models.ForeignKey(Contact,
                                verbose_name=_(u'Contact'),)

    class Meta:
        verbose_name = _(u'Seminar')
        verbose_name_plural = _(u'Seminars')

    def __unicode__(self):
        return self.internal_title


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
        return u'%s (%s %s)' % (self.seminar.internal_title,
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


class VisitorGroup(models.Model):
    """
        :Author:    Rene Jablonski
        :Contact:   rene@vnull.de
    """
    groupname = models.CharField(verbose_name=_(u'Groupname'),
                                 max_length=255,)
    point_of_origin = models.CharField(verbose_name=_(u'Point of Origin'),
                                       max_length=255)
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


