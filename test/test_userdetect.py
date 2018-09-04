# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division)
from ansible.compat.tests import unittest
import userdetect
import six
import collections
if six.PY3:
    from unittest import mock
else:
    import mock


__metaclass__ = type


StructPasswd = collections.namedtuple(
    'struct_passwd',
    ['pw_name', 'pw_passwd', 'pw_uid', 'pw_gid', 'pw_gecos', 'pw_dir',
     'pw_shell']
)

def create_struct_passwd(name, uid, gid, home, shell):
    return StructPasswd(name, 'x', uid, gid, 'gecos', home, shell)


class TestFunction(unittest.TestCase):

    @mock.patch("userdetect.AnsibleModule")
    def test_argument_spec(self, AnsibleModule):
        module = AnsibleModule.return_value
        module.params = {
            'user': 'root',
        }
        module.check_mode = False
        userdetect.main()

        expected = dict(
            user=dict(required=True, type='raw'),
            fallback=dict(required=False, type='str'),
        )

        assert(mock.call(argument_spec=expected,
               supports_check_mode=False) == AnsibleModule.call_args)


    @mock.patch("userdetect.AnsibleModule")
    @mock.patch("userdetect.pwd.getpwnam")
    def test_single_user_existent(self, getpwnam, AnsibleModule):
        module = AnsibleModule.return_value
        module.params = {
            'user': 'root',
        }
        module.check_mode = False
        getpwnam.return_value = create_struct_passwd('root', 2, 3, '/root', '/bin/sh')
        userdetect.main()

        args, kwargs = module.exit_json.call_args
        self.assertEqual(kwargs['mode'], 'single')
        self.assertEqual(kwargs['exists'], True)
        self.assertEqual(kwargs['username'], 'root')
        self.assertEqual(kwargs['uid'], 2)
        self.assertEqual(kwargs['gid'], 3)
        self.assertEqual(kwargs['home'], '/root')
        self.assertEqual(kwargs['shell'], '/bin/sh')

    @mock.patch("userdetect.AnsibleModule")
    @mock.patch("userdetect.pwd.getpwnam")
    def test_single_user_non_existent(self, getpwnam, AnsibleModule):
        module = AnsibleModule.return_value
        module.params = {
            'user': 'root',
        }
        module.check_mode = False
        getpwnam.side_effect = KeyError()
        userdetect.main()

        args, kwargs = module.exit_json.call_args
        self.assertEqual(kwargs['mode'], 'single')
        self.assertEqual(kwargs['exists'], False)
        self.assertEqual(kwargs['username'], 'root')
        self.assertNotIn('uid', kwargs)
        self.assertNotIn('gid', kwargs)
        self.assertNotIn('home', kwargs)
        self.assertNotIn('shell', kwargs)
