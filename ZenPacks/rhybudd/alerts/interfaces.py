###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2012, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
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
        title       = _t(u'Rhybudd Device ID'),
        description = _t(u'A unique string to identify your Android device.'),
        default = _t(u'AABBCCDDEEFF00112233')
    )