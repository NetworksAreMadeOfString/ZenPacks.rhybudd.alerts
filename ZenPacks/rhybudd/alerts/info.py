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

from zope.interface import implements
from Products.Zuul.interfaces import IInfo
#from ZenPacks.zenoss.Notifications.interfaces import (
#    IUserCommandActionContentInfo, IAltEmailHostActionContentInfo,
#    IConfigurableSnmpTrapActionContentInfo
#)
from Products.Zuul.infos.actions import ActionFieldProperty
from Products.Zuul.infos import InfoBase

from ZenPacks.rhybudd.alerts.interfaces import IConfigurableGCMActionContentInfo

#Works with iinfo
#class ConfigurableGCMActionContentInfo(InfoBase):
#    implements(IConfigurableGCMActionContentInfo)
#
#    gcmdeviceid = ActionFieldProperty(IConfigurableGCMActionContentInfo, 'gcmdeviceid')

class ConfigurableGCMActionContentInfo(InfoBase):
    implements(IConfigurableGCMActionContentInfo)

    gcmdeviceid = ActionFieldProperty(IConfigurableGCMActionContentInfo, 'gcmdeviceid')
