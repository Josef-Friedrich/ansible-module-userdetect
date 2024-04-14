ansible-module-userdetect
=========================

:: 

    > USERDETECT    (/etc/ansible/library/userdetect.py)

            Detect the existence of user(s) on UNIX operation systems.
            This module only reports about the existence of users. It
            doesn’t change any data. Use the register key to catch the
            returned informatins about the users.

    OPTIONS (= is mandatory):

    - fallback
            User to look for if the main user can’t be detected.
            default: null

    - user
            The name of the user or a list of users. Users can be
            specified as a comma separted list (user1,user2) or as a YAML
            list.
            default: null

    AUTHOR: Josef Friedrich (@Josef-Friedrich)

    METADATA:
      metadata_version: '0.1'
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
    - all
            A list of all users containing a dictionary with the keys
            “username”, “exists”, “uid”, “gid”, “home”, “shell”.
            returned: In multi mode
            type: list

    - existent
            A list of all existing users containing a dictionary with the
            keys “username”, “exists”, “uid”, “gid”, “home”, “shell”.
            returned: In multi mode
            type: list

    - exists
            Indicates if the user exists
            returned: always
            sample: true
            type: boolean

    - fallback
            Indicates if the user is a the fallback user or not.
            returned: If the user exists
            sample: true
            type: boolean

    - gid
            The group ID
            returned: If the user exists
            sample: 1000
            type: integer

    - home
            The path of the home folder
            returned: If the user exists
            sample: /home/jf
            type: string

    - non_existent
            A list of all non existing users containing a dictionary with
            the keys “username”, “exists”, “uid”, “gid”, “home”, “shell”.
            returned: In multi mode
            type: list

    - shell
            The absoltue path of the shell the user uses.
            returned: If the user exists
            sample: /bin/bash
            type: string

    - uid
            The user ID
            returned: If the user exists
            sample: 1000
            type: integer

    - username
            The name of the user
            returned: always
            sample: root
            type: string

Development
===========

Test functionality
------------------

::

   /usr/local/src/ansible/hacking/test-module -m userdetect.py -a

Test documentation
------------------

::

   source /usr/local/src/ansible/hacking/env-setup
   /usr/local/src/ansible/test/sanity/validate-modules/validate-modules --arg-spec --warnings userdetect.py

Generate documentation
----------------------

::

   ansible-doc -M . userdetect
