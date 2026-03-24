### tpw08/offline.py
from consts import NO_DEST, NO_RIDER

# CARS is a dictionary of Waylo cars. Each car is
# a dictionary containing:
#   * 'loc':   the car's current location. The car's starting
#              location is computed offline.
#   * 'dest':  the car's current destination, which is NO_DEST
#              when it is awaiting a rider assignment, the
#              rider's location when it is headed to a pick-up,
#              or the rider's destination when it is
#              transporting a rider.
#   * 'rider': the car's rider, which is NO_RIDER when the car
#              is awaiting a rider assignment or a rider's ID
#              when it has been assigned a rider.
CARS = {}

def car_setup(config, city):
    '''Allows the user to select an initial configuration
       of cars for a given city. Returns True if setup
       succeeds and False otherwise.
    '''

    # Make sure that CARS is an empty dictionary
    CARS.clear()

    # Available configurations
    if config == '1':
        CARS['1'] = {'loc': (2,2), 'dest': NO_DEST, 'rider': NO_RIDER}
        CARS['2'] = {'loc': (4,4), 'dest': NO_DEST, 'rider': NO_RIDER}
    elif config == '2':
        CARS['1'] = {'loc': (2,2), 'dest': NO_DEST, 'rider': NO_RIDER}
        CARS['2'] = {'loc': (10,10), 'dest': NO_DEST, 'rider': NO_RIDER}
    elif config == '3':
        CARS['1'] = {'loc': (2,5), 'dest': NO_DEST, 'rider': NO_RIDER}
        CARS['2'] = {'loc': (2,4), 'dest': NO_DEST, 'rider': NO_RIDER}
    elif config == '4':
        CARS['1'] = {'loc': (2,2), 'dest': NO_DEST, 'rider': NO_RIDER}
        CARS['2'] = {'loc': (10,10), 'dest': NO_DEST, 'rider': NO_RIDER}
        CARS['3'] = {'loc': (6,6), 'dest': NO_DEST, 'rider': NO_RIDER}
    else:
        print('Invalid choice. Valid responses: 1-4')
        return False

    # Validate starting configuration for Waylo cars
    assert len(CARS) < 10, f'Too many cars in selected configuration'

    if city:
        # Validate starting car locations
        for car_id, car in CARS.items():
            try:
                city.get_mark(car['loc'])
            except AssertionError:
                assert False, \
                    f"Bad loc {car['loc']} for Car {car_id}"

    return True


def main():
    '''Run a simple unit test'''

    # Pick a configuration
    car_setup('2', None)

    # Fake an assignment to Car 1. I cheat on the rider object, which
    # should be a dictionary.
    CARS['1']['dest'] = (4,4)
    CARS['1']['rider'] = 'b'

    # Print out the CARS data structure
    for car in CARS:
        print(f'Car {car} is at {CARS[car]['loc']}')

        # Add current destination to v
        v = '  heading '
        if CARS[car]['dest'] == NO_DEST:
            assert CARS[car]['rider'] == NO_RIDER
            v += 'nowhere and awaiting a rider assignment'
        else:
            v += f'to {CARS[car]['dest']} for Rider {CARS[car]['rider']}'
        
        print(v)

if __name__ == "__main__":
    main()