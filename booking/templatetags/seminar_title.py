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
from django.utils.translation import get_language
from booking.models import SeminarExtended

register = template.Library()


@register.simple_tag
def seminar_title(seminar_id):
    extended_seminar = SeminarExtended.objects.filter(
        id=seminar_id, language__language_code=get_language()).first()
    return extended_seminar.title
