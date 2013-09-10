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


    def update_gcm_settings(self, gcm_api_key=None, gcm_sender_id=None):
        """
        Saves the custom GCM API key etc to local storage. If present we'll use this to send messages
        """
        gcm_details = models.gcm.Gcm(gcm_api_key, gcm_sender_id)
        dmdRoot = _dmdRoot(self.context)
        setattr(dmdRoot, 'rhybudd_gcm', gcm_details)

        return DirectResponse.succeed()
        #if not account.api_access_key or not account.subdomain:
        #    return DirectResponse.succeed()
#
#        services_router = ServicesRouter(self.context, self.request)
#        result = services_router.get_services(wants_messages)
#
#        if result.data['success']:
#            result.data['msg'] = "PagerDuty services retrieved successfully."
#            api_services = result.data['data']
#            log.info("Successfully fetched %d PagerDuty generic API services.", len(api_services))
#
#        return result
