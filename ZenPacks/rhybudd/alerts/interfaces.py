###########################################################################
#
# This program is part of Rhybudd http://blog.NetworksAreMadeOfString.co.uk/Rhybudd/
# Copyright (C) 2013 Gareth Llewellyn
# 
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>
###########################################################################

import Globals

from zope.schema.vocabulary import SimpleVocabulary

from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.Zuul.interfaces import IInfo

from Products.Zuul.interfaces.actions import (
   ICommandActionContentInfo, IEmailActionContentInfo,
   ISnmpTrapActionContentInfo,
)

#IInfo works
#class IConfigurableGCMActionContentInfo(IInfo):
#    
#    gcmdeviceid = schema.Text(
#        title       = _t(u'Rhybudd Device ID'),
#        description = _t(u'A unique string to identify your Android device.'),
#        default = _t(u'AABBCCDDEEFF00112233')
#    )

class IConfigurableGCMActionContentInfo(IInfo):
    
    gcmdeviceid = schema.Text(
        title       = _t(u'Rhybudd Push Key'),
        description = _t(u'The Push Key generated when you enabled Rhybudd Push in the app'),
        default = _t(u'AABBCCDDEEFF00112233')
    )
