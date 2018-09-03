# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division)
from ansible.compat.tests import unittest
import userdetect
import six
if six.PY3:
    from unittest import mock
else:
    import mock


__metaclass__ = type


class TestFunction(unittest.TestCase):

    @mock.patch("userdetect.AnsibleModule")
    def test_mock(self, AnsibleModule):
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


    # @mock.patch("userdetect.AnsibleModule")
    # def test_delete(self, AnsibleModule):
    #     module = AnsibleModule.return_value
    #     module.params = {
    #         'state': 'absent',
    #         'path': '/tmp',
    #         'mark': 'tmp',
    #         'sdirs': sdirs
    #     }
    #     module.check_mode = False
    #     shellmarks.main()
    #
    #     args = module.exit_json.call_args
    #     self.assertEqual(mock.call(changed=False, msg='tmp : /tmp'), args)
