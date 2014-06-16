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

from portal.models import *

# Register your models here.
admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(FeedbackCategory, CategoryAdmin)
admin.site.register(DamageCategory, CategoryAdmin)

admin.site.register(Contact, ContactAdmin)
admin.site.register(Language)

# these stuff will be removed or disabled
admin.site.register(Room)
admin.site.register(House)
admin.site.register(VisitorGroup)
admin.site.register(Seminar)
admin.site.register(SeminarUnit)
admin.site.register(SeminarExtended)

