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
            - The name of the user or a list of users

    fallback:
        description:
            - User to look for if the main user can’t be detected.
        default: root
'''

EXAMPLES = """

- name: Detect user “jf”
  userdetect: user=jf
  register: user

- name: Detect fallback user “root”.
  userdetect: user=lol
              fallback=root
  register: user

- name: Detect users as a list
  userdetect:
    user:
      - jf
      - root
  register: user

"""


EXAMPLES = '''
- name: Ensure foo is installed
  modulename:
    name: foo
    state: present
'''

def detect_user(name):
    result = dict()
    result['name'] = name
    result['exists'] = False

    try:
        p = pwd.getpwnam(name)
        result['exists'] = True
        result['uid'] = p.pw_uid
        result['gid'] = p.pw_gid
        result['home'] = p.pw_dir
        result['shell'] = p.pw_shell
    except KeyError:
        pass

    return result


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
            users.append(user)
        module.exit_json(**{'users': users})

    result = detect_user(module.params['user'])

    if not result['exists'] and 'fallback' in module.params and \
       module.params['fallback']:
        result = detect_user(module.params['fallback'])

    module.exit_json(**result)


if __name__ == '__main__':
    main()
