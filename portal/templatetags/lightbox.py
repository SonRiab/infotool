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
import re
from django.utils.encoding import smart_unicode
from django import template

register = template.Library()

r_lightbox = re.compile('<a (?=[^>]*\.(jpg|gif|png))(?![^>]*lightbox)')
s_lightbox = '<a rel="lightbox" '


@register.filter
def lightbox(content):
    return r_lightbox.sub(s_lightbox, smart_unicode(content))
