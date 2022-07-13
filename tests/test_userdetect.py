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


def mock_userdetect(params, side_effect):
    with mock.patch("userdetect.AnsibleModule") as AnsibleModule:
        with mock.patch("userdetect.pwd.getpwnam") as getpwnam:
            module = AnsibleModule.return_value
            module.params = params
            module.check_mode = False
            getpwnam.side_effect = side_effect
            userdetect.main()
            args, kwargs = module.exit_json.call_args
            return kwargs


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

    def test_single_user_existent(self):
        kwargs = mock_userdetect(
            {'user': 'root'},
            [create_struct_passwd('root', 2, 3, '/root', '/bin/sh')]
        )
        self.assertEqual(kwargs['mode'], 'single')
        self.assertEqual(kwargs['fallback'], False)
        self.assertEqual(kwargs['exists'], True)
        self.assertEqual(kwargs['username'], 'root')
        self.assertEqual(kwargs['uid'], 2)
        self.assertEqual(kwargs['gid'], 3)
        self.assertEqual(kwargs['home'], '/root')
        self.assertEqual(kwargs['shell'], '/bin/sh')

    def test_single_user_non_existent(self):
        kwargs = mock_userdetect({'user': 'root'}, KeyError())
        self.assertEqual(kwargs['mode'], 'single')
        self.assertEqual(kwargs['exists'], False)
        self.assertEqual(kwargs['username'], 'root')
        self.assertNotIn('uid', kwargs)
        self.assertNotIn('gid', kwargs)
        self.assertNotIn('home', kwargs)
        self.assertNotIn('shell', kwargs)

    def test_single_fallback_existent(self):
        kwargs = mock_userdetect(
            {'user': 'jf', 'fallback': 'root'},
            [
                KeyError(),
                create_struct_passwd('root', 2, 3, '/root', '/bin/sh'),
            ]
        )
        self.assertEqual(kwargs['mode'], 'single')
        self.assertEqual(kwargs['fallback'], True)
        self.assertEqual(kwargs['exists'], True)
        self.assertEqual(kwargs['username'], 'root')
        self.assertEqual(kwargs['uid'], 2)
        self.assertEqual(kwargs['gid'], 3)
        self.assertEqual(kwargs['home'], '/root')
        self.assertEqual(kwargs['shell'], '/bin/sh')

    def test_single_fallback_non_existent(self):
        kwargs = mock_userdetect(
            {'user': 'jf', 'fallback': 'root'},
            [
                KeyError(),
                KeyError(),
            ]
        )
        self.assertEqual(kwargs['mode'], 'single')
        self.assertEqual(kwargs['exists'], False)
        self.assertEqual(kwargs['username'], 'root')
        self.assertNotIn('uid', kwargs)
        self.assertNotIn('gid', kwargs)
        self.assertNotIn('home', kwargs)
        self.assertNotIn('shell', kwargs)

    def test_multi_existent(self):
        kwargs = mock_userdetect(
            {'user': 'jf,root'},
            [
                create_struct_passwd('jf', 1000, 1000, '/home/jf',
                                     '/bin/sh'),
                create_struct_passwd('root', 2, 3, '/root', '/bin/sh'),
            ]
        )
        self.assertEqual(kwargs['mode'], 'multi')
        self.assertEqual(len(kwargs['all']), 2)
        self.assertEqual(len(kwargs['existent']), 2)
        self.assertEqual(len(kwargs['non_existent']), 0)
        self.assertEqual(kwargs['all'][0]['username'], 'jf')
        self.assertEqual(kwargs['all'][1]['username'], 'root')

    def test_multi_existent_non_existent(self):
        kwargs = mock_userdetect(
            {'user': 'jf,root'},
            [
                create_struct_passwd('jf', 1000, 1000, '/home/jf',
                                     '/bin/sh'),
                KeyError(),
            ]
        )
        self.assertEqual(kwargs['mode'], 'multi')
        self.assertEqual(len(kwargs['all']), 2)
        self.assertEqual(len(kwargs['existent']), 1)
        self.assertEqual(len(kwargs['non_existent']), 1)
        self.assertEqual(kwargs['existent'][0]['username'], 'jf')
        self.assertEqual(kwargs['non_existent'][0]['username'], 'root')

    def test_multi_non_existent(self):
        kwargs = mock_userdetect(
            {'user': 'jf,root'},
            [
                KeyError(),
                KeyError(),
            ]
        )
        self.assertEqual(kwargs['mode'], 'multi')
        self.assertEqual(len(kwargs['all']), 2)
        self.assertEqual(len(kwargs['existent']), 0)
        self.assertEqual(len(kwargs['non_existent']), 2)
        self.assertEqual(kwargs['non_existent'][0]['username'], 'jf')
        self.assertEqual(kwargs['non_existent'][1]['username'], 'root')
