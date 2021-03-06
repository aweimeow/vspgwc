
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import time
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible
from synchronizers.new_base.modelaccessor import *
from xos.logger import Logger, logging

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

logger = Logger(level=logging.INFO)

class SyncVSPGWCTenant(SyncInstanceUsingAnsible):

    provides = [VSPGWCTenant]
    observes = VSPGWCTenant
    requested_interval = 0

    template_name = "vspgwctenant_playbook.yaml"

    service_key_name = "/opt/xos/configurations/mcord/mcord_private_key"

    watches = [ModelLink(ServiceDependency,via='servicedependency'), ModelLink(ServiceMonitoringAgentInfo,via='monitoringagentinfo')]

    def __init__(self, *args, **kwargs):
        super(SyncVSPGWCTenant, self).__init__(*args, **kwargs)

    def get_network_id(self, network_name):
        network = Network.objects.filter(name=network_name).first()

        return network.id

    def get_instance_object(self, instance_id):
        instance = Instance.objects.filter(id=instance_id).first()

        return instance

    def get_information(self, o):
        fields = {}

        collect_network = [
           {'name': 'SPGWC_PRIVATE_IP', 'net_name': 'vspgwc_network'}
        ]

        instance = self.get_instance_object(o.instance_id)

        for data in collect_network:
            network_id = self.get_network_id(data['net_name'])
            port = filter(lambda x: x.network_id == network_id, instance.ports.all())[0]
            fields[data['name']] = port.ip

        return fields

    def get_extra_attributes(self, o):
        fields = self.get_information(o)

        return fields
