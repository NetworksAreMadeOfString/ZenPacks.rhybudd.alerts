###########################################################################
#
# This program is part of Rhybudd
# http://blog.NetworksAreMadeOfString.co.uk/Rhybudd/
# Copyright (C) 2013 Gareth Llewellyn
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>
###########################################################################

import models.gcm
import models.regid

from Products.ZenUtils.Ext import DirectRouter, DirectResponse

import json
import logging

def _dmdRoot(dmdContext):
    return dmdContext.getObjByPath("/zport/dmd/")

def _success(model_obj, msg=None):
    obj_data = json.loads(json.dumps(model_obj, cls=models.serialization.JSONEncoder))
    return DirectResponse.succeed(msg=msg, data=obj_data)


class RhybuddGCMRouter(DirectRouter):
    def __init__(self, context, request=None):
        super(RhybuddGCMRouter, self).__init__(context, request)

    def get_gcm_settings(self):
        """
        Retrieves the gcm pair from /zport/dmd/rhybudd_gcm.
        """
        dmdRoot = _dmdRoot(self.context)
        gcm_details = getattr(dmdRoot, 'rhybudd_gcm', models.gcm.Gcm(None, None))
        return _success(gcm_details)

    def get_gcm_regids(self):
        """
        Retrieves the various regids from /zport/dmd/rhybudd_regids.
        """
        dmdRoot = _dmdRoot(self.context)
        regids = getattr(dmdRoot, 'rhybudd_regids', [])
        return _success(regids)

    def ping(self):
        """
        Used by the android app to confirm we are installed
        """
        #I really should get this working
        #resources = pkg_resources.require(__name__)
        #ver = 0
        #if not resources:
        #    ver = 0
        #else:
        #    ver = resources[0].version

	dmdRoot = _dmdRoot(self.context)
        regids = getattr(dmdRoot, 'rhybudd_regids', [])
        pong = {"pong":True, "version": 1, "reg":regids }

        return _success(pong)


    def update_gcm_regid(self, gcm_reg_id=None, device_id=None):
        """
        Adds or updates the GCM registration id for the specificed device
        """

        this_reg_details = models.regid.RegID(gcm_reg_id, device_id)
        dmdRoot = _dmdRoot(self.context)
        regids = getattr(dmdRoot, 'rhybudd_regids', [])
        #regids = []
        i = 0
        newDevice = True
        for regDetails in regids:        
         if regDetails.device_id == device_id:
          newDevice = False
          break
         else:
          i += 1

        if newDevice == True:
         regids.append(this_reg_details)
        else:
         regids[i] = this_reg_details

        setattr(dmdRoot, 'rhybudd_regids', regids)
        return DirectResponse.succeed()

    def remove_gcm_regid(self, device_id=None):
        """
        Removes the GCM registration id for the specificed device
        """

        dmdRoot = _dmdRoot(self.context)
        regids = getattr(dmdRoot, 'rhybudd_regids', [])
        #regids = []
        i = 0
        found = False
	this_reg_details = models.regid.RegID("None","None")
        for regDetails in regids:
         if regDetails.device_id == device_id:
          found = True
          this_reg_details = regDetails	  
          break
         else:
          i += 1

        if found == True:
         regids.remove(this_reg_details)
         
        setattr(dmdRoot, 'rhybudd_regids', regids)
        return DirectResponse.succeed()

    def update_gcm_settings(self, gcm_api_key=None, gcm_sender_id=None):
        """
        Saves the custom GCM API key etc to local storage. If present we'll use this to send messages
        """
        gcm_details = models.gcm.Gcm(gcm_api_key, gcm_sender_id)
        dmdRoot = _dmdRoot(self.context)
        setattr(dmdRoot, 'rhybudd_gcm', gcm_details)

        return DirectResponse.succeed()
