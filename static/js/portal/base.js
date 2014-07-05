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
    correctMaxHeight();
    $(window).resize(function() {
        correctMaxHeight();
    });
    var baseFontSize = $.cookie('base-font-size');
    if(baseFontSize != undefined) {
        setBaseFontSize(parseInt(baseFontSize));
    }
});

var correctMaxHeight = function() {
    var maxHeight = $(document).height() - ($('#header').outerHeight() + $('#footer').outerHeight());
    $('#navigation').css('maxHeight', maxHeight + 'px');
    $('#content').css('maxHeight', (maxHeight - 2 * parseInt($('#content').css('marginTop'))) + 'px');
    $('#main').css('maxHeight', maxHeight + 'px');
    /* on android phones the animated slide in of the keyboard causes wrong values so we check them twice! */
    if($(document).height() - ($('#header').outerHeight() + $('#footer').outerHeight()) != maxHeight) {
        correctMaxHeight();
    }
}

var toggleNavigation = function() {
    var navigation = $('#navigation');
    /*console.log(navigation.css('left'));*/
    /*console.log(navigation.attr('data-value'));*/
    if(navigation.css('left') !== '0px') {
        if(navigation.attr('data-value') === undefined) {
            navigation.attr('data-value', navigation.css('left'));
        }
        navigation.show();
        navigation.animate({
            left: '0'
        }, 1000, function() {
            /*console.log('[animate] complete');*/

            //to nothing
        });
    } else {
        navigation.animate({
            left: navigation.attr('data-value')
        }, 1000, function() {
            /*console.log('[animate] complete');*/
            navigation.hide();
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
    correctMaxHeight();
    $('#navigation').attr('data-value', '-' + $('#navigation').outerWidth());
}

var changeFontSize = function(increment) {
    setBaseFontSize(fontSize + increment);
}

var setLang = function(selectNode) {
    window.location.href='/'+$(selectNode).val()+'/';
};
