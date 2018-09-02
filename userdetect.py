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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

# import module snippets
from ansible.module_utils.basic import AnsibleModule
import pwd

ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: userdetect
short_description: |
    Detect the existence of an user on UNIX operations system.
description:
    - Detect the existence of an user on UNIX operations system.

author: "Josef Friedrich (@Josef-Friedrich)"
options:
    user:
        description:
            - The name to the user.

    fallback:
        description:
            - User to look for if the main user can’t be detected.
        default: root
'''


EXAMPLES = """

"""


def detect_user(name):
        result = dict()
        p = pwd.getpwnam(name)
        result['name'] = p.pw_name
        result['uid'] = p.pw_uid
        result['gid'] = p.pw_gid
        result['home'] = p.pw_dir
        result['shell'] = p.pw_shell
        return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            user=dict(required=True),
            fallback=dict(required=False, default='root'),
        ),
        supports_check_mode=False,
    )


    try:
        result = detect_user(module.params['user'])
        module.exit_json(**result)
    except KeyError:
        try:
            result = detect_user(module.params['fallback'])
            module.exit_json(**result)
        except KeyError:
            module.fail_json(**{'msg': 'User can’t be found.'})



if __name__ == '__main__':
    main()
