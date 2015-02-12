# Copyright 2012 OpenStack Foundation
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

import uuid

from tempest_lib import exceptions as lib_exc

from tempest.api.volume import base
from tempest import exceptions
from tempest import test


class VolumeTypesNegativeV2Test(base.BaseVolumeAdminTest):
    _interface = 'json'

    @test.attr(type='gate')
    def test_create_with_nonexistent_volume_type(self):
        # Should not be able to create volume with nonexistent volume_type.
        self.name_field = self.special_fields['name_field']
        params = {self.name_field: str(uuid.uuid4()),
                  'volume_type': str(uuid.uuid4())}
        self.assertRaises(lib_exc.NotFound,
                          self.volumes_client.create_volume, size=1,
                          **params)

    @test.attr(type='gate')
    def test_create_with_empty_name(self):
        # Should not be able to create volume type with an empty name.
        self.assertRaises(exceptions.BadRequest,
                          self.volume_types_client.create_volume_type, '')

    @test.attr(type='gate')
    def test_get_nonexistent_type_id(self):
        # Should not be able to get volume type with nonexistent type id.
        self.assertRaises(lib_exc.NotFound,
                          self.volume_types_client.get_volume_type,
                          str(uuid.uuid4()))

    @test.attr(type='gate')
    def test_delete_nonexistent_type_id(self):
        # Should not be able to delete volume type with nonexistent type id.
        self.assertRaises(lib_exc.NotFound,
                          self.volume_types_client.delete_volume_type,
                          str(uuid.uuid4()))


class VolumeTypesNegativeV1Test(VolumeTypesNegativeV2Test):
    _api_version = 1
