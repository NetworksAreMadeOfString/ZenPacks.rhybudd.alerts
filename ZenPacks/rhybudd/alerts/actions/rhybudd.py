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

import logging
log = logging.getLogger("zen.useraction.actions")

import Globals

from zope.interface import implements

from pynetsnmp import netsnmp

from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenModel.interfaces import IAction
from Products.ZenModel.actions import SNMPTrapAction, _signalToContextDict, ActionExecutionException
from Products.Zuul.form.interfaces import IFormBuilder

from subprocess import call
from ZenPacks.rhybudd.alerts.interfaces import IConfigurableGCMActionContentInfo

class IActionBase(object):
    """
    Mixin class for provided some common, necessary, methods.
    """

    def configure(self, options):
        self.options = options

    def getInfo(self, notification):
        return self.actionContentInfo(notification)

    def generateJavascriptContent(self, notification):
        content = self.getInfo(notification)
        return IFormBuilder(content).render(fieldsets=False)

    def getDefaultData(self, dmd):
        return {}
        
class sendGCM(IActionBase):
    implements(IAction)

    id = 'sendgcm'
    name = 'Send Alert to Rhybudd'
    actionContentInfo = IConfigurableGCMActionContentInfo

    def setupAction(self, dmd):
        self.guidManager = GUIDManager(dmd)
        self.dmd = dmd

    def execute(self, notification, signal):
        self.setupAction(notification.dmd)
        
        data = _signalToContextDict(signal, self.options.get('zopeurl'), notification, self.guidManager)
        
        log.info('GCMID: %s',str(data['evid']))
        log.info(data['gcmdeviceid'])
        
        log.info('Preparing to call curl')
        #call(["curl","-H \"Content-Type: application/json\" -X POST -d '{\"auth_key\": \"YOUR-SERVICE-KEY\", \"incident_key\": \"${evt/evid}\", \"event_type\": \"trigger\", \"description\": \"${evt/device}: '${evt/summary}'\", \"details\": { \"device\": \"${evt/device}\", \"ipAddress\": \"${evt/ipAddress}\", \"severity\": \"${evt/severity}\", \"summary\": ${evt/summary}, \"message\": ${evt/message}, \"evid\": \"${evt/evid}\"} }' http://api.coldstart.io/1/zenoss.php"])    
        call(["curl","http://api.coldstart.io/1/zenoss.php"])
        log.info('Curl was called')
    
    def updateContent(self, content=None, data=None):
        content['gcmdeviceid'] = data.get('gcmdeviceid')
        
  