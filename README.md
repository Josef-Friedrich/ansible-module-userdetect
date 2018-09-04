[![Build Status](https://travis-ci.org/Josef-Friedrich/ansible-module-userdetect.svg?branch=master)](https://travis-ci.org/Josef-Friedrich/ansible-module-userdetect)

```
> USERDETECT    (userdetect.py)

        Detect the existence of user(s) on UNIX operation systems.
        This module only reports about the existence of users. It
        doesn’t change any data. Use the register key to catch the
        returned informatins about the users.

OPTIONS (= is mandatory):

- fallback
        User to look for if the main user can’t be detected.
        [Default: (null)]

- user
        The name of the user or a list of users. Users can be
        specified as a comma separted list (user1,user2) or as a YAML
        list.
        [Default: (null)]


AUTHOR: Josef Friedrich (@Josef-Friedrich)
        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:
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

RETURN VALUES:


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
fallback:
    description: Indicates if the user is a the fallback user or not.
    returned: If the user exists
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
```

# Development

## Test functionality

```
/usr/local/src/ansible/hacking/test-module -m userdetect.py -a
```

## Test documentation

```
source /usr/local/src/ansible/hacking/env-setup
/usr/local/src/ansible/test/sanity/validate-modules/validate-modules --arg-spec --warnings userdetect.py
```

## Generate documentation

```
ansible-doc -M . userdetect
```
