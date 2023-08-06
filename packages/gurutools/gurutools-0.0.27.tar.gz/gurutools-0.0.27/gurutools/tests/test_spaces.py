from django.test import TestCase
from gurutools.spaces import get_spaces, has_enabled_permissions
from pgnosql.user import GlobalUser
from unittest import mock


def mock_space(id, role, enabled_actions):
    return {"service": id, "role": role, "enabled_actions": enabled_actions}


class SpacesTestCase(TestCase):
    def __set_userdata(self, id, data):
        return GlobalUser(id).set(data)

    def setUp(self):
        pass

    def test_has_permissions(self):
        space = {"enabled_actions": ["foo", "bar", "baz"]}
        self.assertFalse(has_enabled_permissions(space, []))

        self.assertTrue(has_enabled_permissions(space, ["bar"]))

    @mock.patch.object(GlobalUser, "get")
    def test_get_spaces(self, mock_user):
        mock_user.return_value = {
            "spaces": [
                mock_space("1", "Owner", ["foo"]),
                mock_space("2", "Member", []),
                mock_space("3", "Member", ["bar"]),
            ]
        }
        space_ids = get_spaces("1")
        self.assertEqual(space_ids, ["1", "2", "3"])

        space_ids = get_spaces("1", roles=["Owner"])
        self.assertEqual(space_ids, ["1"])

        space_ids = get_spaces("1", permissions=["foo"])
        self.assertEqual(space_ids, ["1"])

        space_ids = get_spaces("1", permissions=["bar"])
        self.assertEqual(space_ids, ["3"])

        space_ids = get_spaces("1", permissions=["foo", "bar"])
        self.assertEqual(space_ids, ["1", "3"])

        # permissions _or_ roles
        space_ids = get_spaces("1", permissions=["foo", "bar"], roles=["Owner"])
        self.assertEqual(space_ids, ["1", "3"])

        # permissions _or_ roles
        space_ids = get_spaces("1", permissions=["foo", "bar"], roles=["Member"])
        self.assertEqual(space_ids, ["1", "2", "3"])
