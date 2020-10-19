from pyramid.view import view_config


@view_config(route_name="ymd-pattern", renderer="json")
@view_config(route_name="ymd-kvpattern", renderer="json")
@view_config(route_name="user_profile", renderer="json")
@view_config(route_name="user_profile-subfolder1", renderer="json")
@view_config(route_name="user_profile-subfolder2", renderer="json")
def ymd_pattern(request):
    return {
        "matchdict": request.matchdict,
        "route_name": request.matched_route.name,
    }
