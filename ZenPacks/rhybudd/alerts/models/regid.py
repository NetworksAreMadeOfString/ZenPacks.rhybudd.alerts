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

import serialization
import json

class RegID(object):
    """
    GCM communications require a GCM RegID and Rhybudd uses a device ID to dedupe
    """
    def __init__(self, gcm_reg_id, device_id):
        self.gcm_reg_id = gcm_reg_id
        self.device_id = device_id

    def __json__(self):
        return json.dumps(self, cls=serialization.JSONEncoder)
