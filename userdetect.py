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
    try:
        result = dict()
        p = pwd.getpwnam(name)
        result['name'] = p.pw_name
        result['uid'] = p.pw_uid
        result['gid'] = p.pw_gid
        result['home'] = p.pw_dir
        result['shell'] = p.pw_shell
        return result
    except KeyError:
        return None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            user=dict(required=True, type='raw'),
            fallback=dict(required=False, type='str'),
        ),
        supports_check_mode=False,
    )

    users = []
    if isinstance(module.params['user'], (list,)):
        for username in module.params['user']:
            user = detect_user(username)
            if user:
                users.append(user)

        if users:
            module.exit_json(**{'users': users})
        else:
            module.fail_json(**{'msg': 'Users can’t be found.'})

    result = detect_user(module.params['user'])
    if result:
        module.exit_json(**result)
    elif 'fallback' in module.params and module.params['fallback']:
        result = detect_user(module.params['fallback'])
        if result:
            module.exit_json(**result)
        else:
            module.fail_json(**{'msg': 'User can’t be found.'})
    else:
        module.fail_json(**{'msg': 'User can’t be found.'})


if __name__ == '__main__':
    main()
