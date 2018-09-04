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
    Detect the existence of user(s) on UNIX operation systems.
description:
    - Detect the existence of user(s) on UNIX operation systems.

author: "Josef Friedrich (@Josef-Friedrich)"
options:
    user:
        description:
            - The name of the user or a list of users

    fallback:
        description:
            - User to look for if the main user can’t be detected.
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

- name: Detect users as a comma separated list
  userdetect: user=jf,root
  register: user
"""

RETURN = '''
username:
    description: The name of the user
    returned: always
    type: string
    sample: root
exists:
    description: Indicates if the user exists
    returned: always
    type: boolean
    sample: True
uid:
    description: The user ID
    returned: If the user exists
    type: integer
    sample: 1000
gid:
    description: The group ID
    returned: If the user exists
    type: integer
    sample: 1000
home:
    description: The path of the home folder
    returned: If the user exists
    type: string
    sample: /home/jf
shell:
    description: The absoltue path of the shell the user uses.
    returned: If the user exists
    type: string
    sample: /bin/bash

all:
    description: |
        A list of all users containing a dictionary with the keys “username”,
        “exists”, “uid”, “gid”, “home”, “shell”.
    returned: In multi mode
    type: list
existent:
    description: |
        A list of all existing users containing a dictionary with the keys
        “username”, “exists”, “uid”, “gid”, “home”, “shell”.
    returned: In multi mode
    type: list
non_existent:
    description: |
        A list of all non existing users containing a dictionary with the
        keys “username”, “exists”, “uid”, “gid”, “home”, “shell”.
    returned: In multi mode
    type: list
'''


def detect_user(name):
    result = dict()
    result['username'] = name
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

    existent = []
    non_existent = []
    all = []

    userlist = None
    if isinstance(module.params['user'], (list,)):
        userlist = module.params['user']
    elif ',' in module.params['user']:
        userlist = module.params['user'].split(',')

    if userlist:
        for username in userlist:
            user = detect_user(username)
            if user['exists']:
                existent.append(user)
            else:
                non_existent.append(user)
            all.append(user)
        module.exit_json(mode='multi', existent=existent,
                         non_existent=non_existent,
                         all=non_existent)

    result = detect_user(module.params['user'])
    result['mode'] = 'single'

    if not result['exists'] and 'fallback' in module.params and \
       module.params['fallback']:
        result = detect_user(module.params['fallback'])

    module.exit_json(**result)


if __name__ == '__main__':
    main()
