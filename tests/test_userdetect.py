from __future__ import annotations

from typing import NamedTuple, Union
from unittest import mock

import userdetect
from userdetect import ModuleParams

__metaclass__ = type


class StructPasswd(NamedTuple):
    pw_name: str
    pw_passwd: str
    pw_uid: int
    pw_gid: int
    pw_gecos: str
    pw_dir: str
    pw_shell: str


def create_struct_passwd(
    name: str, uid: int, gid: int, home: str, shell: str
) -> StructPasswd:
    return StructPasswd(name, "x", uid, gid, "gecos", home, shell)


SideEffect = Union[StructPasswd, KeyError]


def mock_userdetect(
    params: ModuleParams, side_effect: Union[SideEffect, list[SideEffect]]
):
    with mock.patch("userdetect.AnsibleModule") as AnsibleModule:
        with mock.patch("userdetect.pwd.getpwnam") as getpwnam:
            module = AnsibleModule.return_value
            module.params = params
            module.check_mode = False
            getpwnam.side_effect = side_effect
            userdetect.main()
            _, kwargs = module.exit_json.call_args
            return kwargs


class TestFunction:
    @mock.patch("userdetect.AnsibleModule")
    def test_argument_spec(self, AnsibleModule: mock.MagicMock):
        module = AnsibleModule.return_value
        module.params = {
            "user": "root",
        }
        module.check_mode = False
        userdetect.main()

        expected = dict(
            user=dict(required=True, type="raw"),
            fallback=dict(required=False, type="str"),
        )

        assert (
            mock.call(argument_spec=expected, supports_check_mode=False)
            == AnsibleModule.call_args
        )

    def test_single_user_existent(self) -> None:
        kwargs = mock_userdetect(
            {"user": "root"}, [create_struct_passwd("root", 2, 3, "/root", "/bin/sh")]
        )
        assert kwargs["mode"] == "single"
        assert not kwargs["fallback"]
        assert kwargs["exists"]
        assert kwargs["username"] == "root"
        assert kwargs["uid"] == 2
        assert kwargs["gid"] == 3
        assert kwargs["home"] == "/root"
        assert kwargs["shell"] == "/bin/sh"

    def test_single_user_non_existent(self) -> None:
        kwargs = mock_userdetect({"user": "root"}, KeyError())
        assert kwargs["mode"] == "single"
        assert not kwargs["exists"]
        assert kwargs["username"] == "root"
        assert "uid" not in kwargs
        assert "gid" not in kwargs
        assert "home" not in kwargs
        assert "shell" not in kwargs

    def test_single_fallback_existent(self) -> None:
        kwargs = mock_userdetect(
            {"user": "jf", "fallback": "root"},
            [
                KeyError(),
                create_struct_passwd("root", 2, 3, "/root", "/bin/sh"),
            ],
        )
        assert kwargs["mode"] == "single"
        assert kwargs["fallback"]
        assert kwargs["exists"]
        assert kwargs["username"] == "root"
        assert kwargs["uid"] == 2
        assert kwargs["gid"] == 3
        assert kwargs["home"] == "/root"
        assert kwargs["shell"] == "/bin/sh"

    def test_single_fallback_non_existent(self) -> None:
        kwargs = mock_userdetect(
            {"user": "jf", "fallback": "root"},
            [
                KeyError(),
                KeyError(),
            ],
        )
        assert kwargs["mode"] == "single"
        assert not kwargs["exists"]
        assert kwargs["username"] == "root"
        assert "uid" not in kwargs
        assert "gid" not in kwargs
        assert "home" not in kwargs
        assert "shell" not in kwargs

    def test_multi_existent(self) -> None:
        kwargs = mock_userdetect(
            {"user": "jf,root"},
            [
                create_struct_passwd("jf", 1000, 1000, "/home/jf", "/bin/sh"),
                create_struct_passwd("root", 2, 3, "/root", "/bin/sh"),
            ],
        )
        assert kwargs["mode"] == "multi"
        assert len(kwargs["all"]) == 2
        assert len(kwargs["existent"]) == 2
        assert len(kwargs["non_existent"]) == 0
        assert kwargs["all"][0]["username"] == "jf"
        assert kwargs["all"][1]["username"] == "root"

    def test_multi_existent_non_existent(self) -> None:
        kwargs = mock_userdetect(
            {"user": "jf,root"},
            [
                create_struct_passwd("jf", 1000, 1000, "/home/jf", "/bin/sh"),
                KeyError(),
            ],
        )
        assert kwargs["mode"] == "multi"
        assert len(kwargs["all"]) == 2
        assert len(kwargs["existent"]) == 1
        assert len(kwargs["non_existent"]) == 1
        assert kwargs["existent"][0]["username"] == "jf"
        assert kwargs["non_existent"][0]["username"] == "root"

    def test_multi_non_existent(self) -> None:
        kwargs = mock_userdetect(
            {"user": "jf,root"},
            [
                KeyError(),
                KeyError(),
            ],
        )
        assert kwargs["mode"] == "multi"
        assert len(kwargs["all"]) == 2
        assert len(kwargs["existent"]) == 0
        assert len(kwargs["non_existent"]) == 2
        assert kwargs["non_existent"][0]["username"] == "jf"
        assert kwargs["non_existent"][1]["username"] == "root"
