#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Josef Friedrich <josef@friedrich.rocks>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.


ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
---
module: userdetect
author: "Josef Friedrich (@Josef-Friedrich)"

short_description: Detect if a user exists on a UNIX operations system.
description:
  - Detect if a user exists on a UNIX operations system.
options:
  path:
    user:
      - The name to the user.
    required: true

"""

EXAMPLES = """

"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


# import module snippets
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            user=dict(required=True),
        ),
        supports_check_mode=False,
    )


if __name__ == '__main__':
    main()
