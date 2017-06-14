from threading import Timer
from resource import RESOURCES
from interval import VALUE


def check_data(teams, fields, castles, init=False):
    timer = Timer(1.0, check_data, [
        teams,
        fields,
        castles,
    ])

    timer.start()

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
