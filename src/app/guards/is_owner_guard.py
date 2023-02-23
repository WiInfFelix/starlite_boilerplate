from starlite import ASGIConnection, BaseRouteHandler


def is_owner_guard(connection: ASGIConnection, _: BaseRouteHandler):
    return connection.user.id == connection.path_params["user_id"]
