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

import logging
log = logging.getLogger("zen.useraction.actions")

import Globals
from zope.interface import implements
from Products.ZenUtils.guid.guid import GUIDManager
from Products.ZenModel.interfaces import IAction
from Products.ZenModel.actions import _signalToContextDict, ActionExecutionException
from Products.ZenModel.NotificationSubscription import NotificationEventContextWrapper
from Products.Zuul.form.interfaces import IFormBuilder

#In order to call curl
#from subprocess import call

#OR the urllib way
import urllib
import urllib2
import httplib
import json

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

        if notification.content['gcmdeviceid'] == "AABBCCDDEEFF00112233":
            raise ActionExecutionException("Cannot send a Rhybudd GCM message with the default GCM Key")
        
	if signal.clear and data['clearEventSummary'].uuid:
	    log.info('------------------------------------ Signal clear')
        else:
            log.info('------------------------------------ Signal something else')

        #log.info(data['eventSummary'].summary)
        #log.info(data['eventSummary'].status)
        #log.info(data['eventSummary'].count)
        #log.info(data['eventSummary'].severity)
        #log.info(data['eventSummary'].event_class)
        #log.info(data['eventSummary'].event_class_key) 

        actor = signal.event.occurrence[0].actor
        device = None
        if actor.element_uuid:
            device = self.guidManager.getObject(actor.element_uuid)

        #curlCall = "curl -H \"Content-Type: application/json\" -X POST -d '{\"gcm_id\": \"%s\",\"evid\": \"%s\",\"device\": \"%s\",\"summary\": \"%s\",\"status\": \"%s\",\"count\": \"%s\",\"severity\": \"%s\",\"event_class\": \"%s\",\"event_class_key\": \"%s\"}' http://api.coldstart.io/1/zenoss.php" % (notification.content['gcmdeviceid'], signal.event.uuid,device,data['eventSummary'].summary,data['eventSummary'].status,data['eventSummary'].count,data['eventSummary'].severity,data['eventSummary'].event_class,data['eventSummary'].event_class_key)
        #call(curlCall, shell=True)

        payload = {
        'gcm_id': notification.content['gcmdeviceid'],
"evid": "%s" % signal.event.uuid,
"device": "%s" % device,
"summary": "%s" % data['eventSummary'].summary,
"status": data['eventSummary'].status,
"count": data['eventSummary'].count,
"severity": data['eventSummary'].severity,
"event_class": "%s" % data['eventSummary'].event_class,
"event_class_key": "%s" % data['eventSummary'].event_class_key,
}
        data = "json=%s" % json.dumps(payload)
        h = httplib.HTTPSConnection('api.coldstart.io')
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        h.request('POST', '/1/zenoss', data, headers)
    
    def updateContent(self, content=None, data=None):
        content['gcmdeviceid'] = data.get('gcmdeviceid')
 
