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
    var baseFontSize = $.cookie('base-font-size');
    if(baseFontSize != undefined) {
        setBaseFontSize(parseInt(baseFontSize));
    }
});

var toggleNavigation = function() {
    var sidebar = $('#sidebar');
    /*console.log(navigation.css('left'));*/
    /*console.log(navigation.attr('data-value'));*/
    if(sidebar.css('left') !== '0px') {
        if(sidebar.attr('data-value') === undefined) {
            sidebar.attr('data-value', sidebar.css('left'));
        }
        sidebar.show();
        sidebar.animate({
            left: '0'
        }, 1000, function() {
            /*console.log('[animate] complete');*/

            //to nothing
        });
    } else {
        sidebar.animate({
            left: sidebar.attr('data-value')
        }, 1000, function() {
            /*console.log('[animate] complete');*/
            sidebar.hide();
            //to nothing
        });
    }
};

var toggleSubNavigation = function(node) {
    /*console.log('[toggleSubNavigation]');*/
    var siteId = $(node).attr('data-id');
    /*console.log('#sub-'+siteId);*/
    $('#sub-'+siteId).toggle();
    $('#toggle-icon-'+siteId).toggleClass('icon-plus3 icon-minus3')
}

var fontSize = 16;
var setBaseFontSize = function(size) {
    if(size < 12 || size > 24) {
        return;
    }
    fontSize = size;
    $('html').css('font-size', size + 'px');
    $.cookie('base-font-size', fontSize, { path: '/' });
    $('#sidebar').attr('data-value', '-' + $('#navigation').outerWidth());
}

var changeFontSize = function(increment) {
    setBaseFontSize(fontSize + increment);
}

var setLang = function(selectNode) {
    window.location.href='/'+$(selectNode).val()+'/';
};
