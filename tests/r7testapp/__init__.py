from pyramid.config import Configurator


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("home", "/")

    config.include("pyramid_route_7")
    config.add_route_7_pattern("d4", r"\d\d\d\d")
    config.add_route_7_pattern("d2", r"\d\d")
    config.add_route_7_kvpattern("year", r"\d\d\d\d")
    config.add_route_7_kvpattern("month", r"\d\d")
    config.add_route_7_kvpattern("day", r"\d\d")
    config.add_route_7("ymd-kvpattern", "/ymd-kvpattern/{@year}/{@month}/{@day}")
    config.add_route_7("ymd-pattern", "/ymd-pattern/{year|d4}/{month|d2}/{day|d2}")

    config.add_route_7_kvpattern("user_id", r"\d\d\d")
    config.add_route_7("user_profile", "/path/to/user/{@user_id}")
    config.add_route_7(
        "user_profile-subfolder1", "/path/to/user/{@user_id}/subfolder-one"
    )
    config.add_route_7(
        "user_profile-subfolder2", "/path/to/user/{@user_id}/subfolder-two"
    )
    config.add_route_7("user_profile-alt", "/path/to/user-alt/{@user_id}", jsonify=True)

    config.scan()
    return config.make_wsgi_app()
