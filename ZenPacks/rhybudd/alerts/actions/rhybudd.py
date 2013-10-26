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
from ZenPacks.rhybudd.alerts.libs.gcm_server import GCMSERVER
from ZenPacks.rhybudd.alerts.models.gcm import Gcm

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

#    def executeBatch(self, notification, signal, targets):
#	log.debug("Executing %s action for targets: %s", self.name, targets)
#
#	self.setupAction(notification.dmd)
#
#        data = _signalToContextDict(signal, self.options.get('zopeurl'), notification, self.guidManager)


    def execute(self, notification, signal):
        self.setupAction(notification.dmd)
        
        data = _signalToContextDict(signal, self.options.get('zopeurl'), notification, self.guidManager)

        #if notification.content['gcmdeviceid'] == "AABBCCDDEEFF00112233":
        #    raise ActionExecutionException("Cannot send a Rhybudd GCM message with the default GCM Key")
        
	#if signal.clear and data['clearEventSummary'].uuid:
	#    log.info('------------------------------------ This is a clear message')
        #else:
        #    log.info('------------------------------------ This is an alert')

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

	#------------------------------------
	#The CURL Way of doing things
        #curlCall = "curl -H \"Content-Type: application/json\" -X POST -d '{\"gcm_id\": \"%s\",\"evid\": \"%s\",\"device\": \"%s\",\"summary\": \"%s\",\"status\": \"%s\",\"count\": \"%s\",\"severity\": \"%s\",\"event_class\": \"%s\",\"event_class_key\": \"%s\"}' http://api.coldstart.io/1/zenoss.php" % (notification.content['gcmdeviceid'], signal.event.uuid,device,data['eventSummary'].summary,data['eventSummary'].status,data['eventSummary'].count,data['eventSummary'].severity,data['eventSummary'].event_class,data['eventSummary'].event_class_key)
        #call(curlCall, shell=True)

	#------------------------------------
	#The URL Lib way of doing things

	prodstate = ""
	try:
		prodstate = "%s" % data.prodstate  		
	except Exception:
		prodstate = "" 
  		pass

        payload = {
        'filter_key': notification.content['gcmdeviceid'],
"evid": "%s" % signal.event.uuid,
"device": "%s" % device,
"summary": "%s" % data['eventSummary'].summary,
"status": data['eventSummary'].status,
"count": data['eventSummary'].count,
"severity": data['eventSummary'].severity,
"event_class": "%s" % data['eventSummary'].event_class,
"event_class_key": "%s" % data['eventSummary'].event_class_key,

"prodstate": "%s" % prodstate,
"firsttime": "%s" % data['eventSummary'].first_seen_time,
#"componenttext": "%s" % data['eventSummary'].component.text,
"ownerid": "%s" % data['eventSummary'].current_user_name
}

	gcm_details = getattr(self.dmd, 'rhybudd_gcm', Gcm("", ""))
	log.info("%s",gcm_details.gcm_api_key)
	stored_regids = getattr(self.dmd, 'rhybudd_regids', [])
	reg_ids = []

	for regDetails in stored_regids:
          #log.info('Found a GCM ID: %s',regDetails.gcm_reg_id)
	  reg_ids.append(regDetails.gcm_reg_id)

	if gcm_details.gcm_api_key == "":
		#------------------------------------
		#No GCM Key specified so we'll proxy through ColdStart.io so as to not expose our GCM API Key
		log.info('------------------------------------ Sending a coldstart GCM Request')
        	
		coldstart_payload = {'payload': payload, 'regids': reg_ids} 
		data = "json=%s" % json.dumps(coldstart_payload)
		
        	h = httplib.HTTPSConnection('api.coldstart.io')
        	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        	h.request('POST', '/1/zenoss', data, headers)
    
	else:
		#------------------------------------
		# Direct to GCM
		log.info('------------------------------------ Sending a direct GCM Request')
		gcm = GCMSERVER(gcm_details.gcm_api_key)
		#reg_ids = ['APA91bEPJ_Pf7k5KgpZxbNBpq9snGjYyQn6Q21w_JYl-_4FADgNH54kzcQxGb6Wjb1PkWGiEaVQE0MXhMw7q-jTOvDN_smiaSa96F9sEOLd1xYt4yd7PiYVCYsVULiFoN_isvz1AcN-HXjZVfipBLBIzN5ohqN_MM2tpmBj9JFpdwjFgM6ZNhPU']
		response = gcm.json_request(registration_ids=reg_ids, data=payload, collapse_key=signal.event.uuid, time_to_live=0)
		log.info("%s",json.dumps(response))
		log.info('------------------------------------ Sent a direct GCM Request')	

    def updateContent(self, content=None, data=None):
        content['gcmdeviceid'] = data.get('gcmdeviceid') 
