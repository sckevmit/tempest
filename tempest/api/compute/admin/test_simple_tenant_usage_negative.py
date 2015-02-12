# Copyright 2013 NEC Corporation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import datetime
from tempest_lib import exceptions as lib_exc

from tempest.api.compute import base
from tempest import exceptions
from tempest import test


class TenantUsagesNegativeTestJSON(base.BaseV2ComputeAdminTest):

    @classmethod
    def resource_setup(cls):
        super(TenantUsagesNegativeTestJSON, cls).resource_setup()
        cls.adm_client = cls.os_adm.tenant_usages_client
        cls.client = cls.os.tenant_usages_client
        cls.identity_client = cls._get_identity_admin_client()
        now = datetime.datetime.now()
        cls.start = cls._parse_strtime(now - datetime.timedelta(days=1))
        cls.end = cls._parse_strtime(now + datetime.timedelta(days=1))

    @classmethod
    def _parse_strtime(cls, at):
        # Returns formatted datetime
        return at.strftime('%Y-%m-%dT%H:%M:%S.%f')

    @test.attr(type=['negative', 'gate'])
    def test_get_usage_tenant_with_empty_tenant_id(self):
        # Get usage for a specific tenant empty
        params = {'start': self.start,
                  'end': self.end}
        self.assertRaises(lib_exc.NotFound,
                          self.adm_client.get_tenant_usage,
                          '', params)

    @test.attr(type=['negative', 'gate'])
    def test_get_usage_tenant_with_invalid_date(self):
        # Get usage for tenant with invalid date
        params = {'start': self.end,
                  'end': self.start}
        self.assertRaises(exceptions.BadRequest,
                          self.adm_client.get_tenant_usage,
                          self.client.tenant_id, params)

    @test.attr(type=['negative', 'gate'])
    def test_list_usage_all_tenants_with_non_admin_user(self):
        # Get usage for all tenants with non admin user
        params = {'start': self.start,
                  'end': self.end,
                  'detailed': int(bool(True))}
        self.assertRaises(exceptions.Unauthorized,
                          self.client.list_tenant_usages, params)
