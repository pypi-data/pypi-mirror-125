from pgnosql.user import GlobalUser
from pgnosql.models import KV


class SPACE_ROLES:
    ADMIN_ROLES = ["Owner", "Admin"]


def has_enabled_permissions(space, permissions):
    enabled_permissions = space.get("enabled_actions", [])
    return len(set(permissions).intersection(enabled_permissions)) > 0


def get_spaces(user_id, roles=None, permissions=[]):
    if not user_id:
        return []
    user = GlobalUser(user_id).get()
    if not user:
        return []
    all_spaces = user.get("spaces", [])

    if roles is not None or len(permissions) > 0:
        spaces = []
        if roles is None:
            roles = []
        for space in all_spaces:
            has_permissions = has_enabled_permissions(space, permissions)
            if space.get("role") in roles or has_permissions:
                spaces.append(space.get("service"))

        return spaces
    else:
        return [space.get("service") for space in all_spaces]


def get_channel(user_id):
    user = GlobalUser(user_id).get()
    if user is not None:
        return user.get("user", {}).get("channel", None)
    return None


def get_relationship(practitioner_id, client_id):
    key = "relationship:{}/{}".format(practitioner_id, client_id)
    return KV.get(key)
