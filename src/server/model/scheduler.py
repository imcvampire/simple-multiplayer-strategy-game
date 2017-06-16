from threading import Timer
from resource import RESOURCES
from interval import VALUE


def check_data(teams, fields, castles, init=False):
    """Create new Timer, start it and check all server's data
    :param teams: array of team
    :param fields: array of field
    :param castles: array of castle
    :param init: whether is init or not
    :return timer: a new timer
    """
    timer = Timer(1.0, check_data, [
        teams,
        fields,
        castles,
    ])

    timer.start()

    # We dont need run this block if this is init function
    if not init:
        for field in fields:
            for resource in RESOURCES[:2]:
                teams_have_resource = field.reduce_time(resource)

                for solver in teams_have_resource:
                    teams[solver].add_resource(resource, VALUE[resource])

        for castle in castles:
            resource = RESOURCES[3]

            if castle.reduce_gold_delay():
                teams[castle.owner_id].add_resource(resource, VALUE[resource])


    # Send data to client

    return timer
