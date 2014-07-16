/*
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
 */

$(function() {
    var activityId = $.cookie('activity-id');
    var activities = $('.activity');
    if(activityId === undefined) {
        if(activities.length > 1) {
            $('.activity').each(function() {
                console.log(this);
                if($(this).css('display') == 'inline') {
                    console.log(this.id);
                    $.cookie('activity-id', this.id);
                }
            });
        }
        return;
    }
    if(activityId == activities.last().attr('id')) {
        $('#'+activityId).hide();
        var next = activities.first().show();
        $.cookie('activity-id', next.attr('id'));
    } else {
        var next = $('#'+activityId).hide().next().show();
        $.cookie('activity-id', next.attr('id'));
    }
});