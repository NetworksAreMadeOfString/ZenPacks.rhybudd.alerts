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

class Gcm(object):
    """
    GCM transactions require a GCM API Key and for certain things a sender id.
    """
    def __init__(self, gcm_api_key, gcm_sender_id):
        self.gcm_api_key = gcm_api_key
        self.gcm_sender_id = gcm_sender_id

    def __json__(self):
        return json.dumps(self, cls=serialization.JSONEncoder)
