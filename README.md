```
> USERDETECT    (userdetect.py)

        Detect the existence of user(s) on UNIX operation systems.

OPTIONS (= is mandatory):

- fallback
        User to look for if the main user can’t be detected.
        [Default: (null)]

- user
        The name of the user or a list of users
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
```
