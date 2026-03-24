### tpw08/online.py
import random
from consts import NO_CAR, NOTHING

# Dictionary of Waylo riders in a car or waiting for one.
# This dictionary starts empty since there are no riders
# on the map as a day begins.
#
# Each rider is a dictionary containing:
#   * 'loc':  the rider's current location
#   * 'dest': the rider's desired destination
#   * 'car':  the car assigned to this rider
#   * 'waiting': True if waiting for pickup
RIDERS = {}

# Hails is a schedule of when riders enter the map. Its
# format is: (timestep, loc, dest). The list that
# represents this schedule must be ordered in increasing
# timestep. Each hailing rider is automatically given an
# id, which is the index of that rider in the HAILS list.
# The total number of riders must be less than 26, which
# is a limitation due to how we print the map.
HAILS = []

# Track of the next rider to appear from the hails list
next_rider = 0


def rider_icon(rider_id):
    '''Takes a rider identifier (an int) and returns
       the corresponding rider icon (a letter).'''
    return chr(ord('a') + rider_id)


def rand_locs(city):
    '''Returns a pair of random start and destination locations
       in the given city. It guarantees that the locations
       are within the city and not inside a building.'''
    max_x = city.width + 1
    max_y = city.height + 1

    def rand_loc():
        '''Generates a single random location in the city'''
        # These maximums are weird due to implementation of maze.py
        loc_x = random.randint(0, max_x)
        if loc_x & 1 == 0:
            loc_y = random.randint(0, max_y)
        else:
            # x is odd so force y to be even
            loc_y = random.randint(0, max_y // 2) * 2
        return (loc_x, loc_y)
    
    # Create a random starting location
    start_loc = rand_loc()

    # Create a random destination that isn't the start_loc
    while True:
        dest_loc = rand_loc()
        if dest_loc != start_loc:
            return (start_loc, dest_loc)


def rand_schedule(city):
    '''Saves in HAILS a randomly created hails list.
       It is hardwired with constants that define:
       
       *  what's the first timeslot for a hail
       *  how many hails will be produced
       *  how far apart can hails be

       Feel free to change these ranges.
    '''
    
    assert len(HAILS) == 0, \
           "HAILS should have been cleared in rider_setup"

    # Generate a random starting timeslot
    timeslot = random.randint(1, 3)

    # Generate a random number of hailing riders
    num_riders = random.randint(1, 10)

    # Generate the schedule with a randomly generated
    # distance between hails.
    for _ in range(num_riders):
        # Generate random start and dest locations
        start_loc, dest_loc = rand_locs(city)

        # Add the new hail to the schedule's end
        HAILS.append((
            timeslot,
            start_loc,
            dest_loc
        ))

        # Randomly move the timeslot forward
        timeslot += random.randint(0,7)


def rider_setup(config, city):
    '''Allows the user to select a ride-request stream
    '''
    global next_rider

    # Clear the riders and hails lists and the tracker
    RIDERS.clear()
    HAILS.clear()
    next_rider = 0
    
    # Available configurations, which set the hails list
    if config == '1':
        HAILS.append( ( 1, (3,8), (6,6)) )
    elif config == '2':
        HAILS.append( ( 1, (3,8), (6,6)) )
        HAILS.append( ( 8, (8,7), (2,1)) )
        HAILS.append( (12, (9,2), (0,6)) )
    elif config == 'r':
        # Randomly generate a schedule of rider hails
        rand_schedule(city)
    else:
        print('Invalid choice. Valid responses: 1-2, r')
        return False

    # Validate hail stream
    assert len(HAILS) < 26, 'Too many riders in hail stream'

    if city:
        # Validate starting rider locations
        for rider_id, hail in enumerate(HAILS):
            try:
                city.get_mark(hail[1])
            except AssertionError:
                assert False, \
                    f"Bad loc {hail[1]} for Rider {rider_id}"
            try:
                city.get_mark(hail[2])
            except AssertionError:
                assert False, \
                    f"Bad dest {hail[2]} for Rider {rider_id}"                

    return True


def add_hails(city, timestep, show):
    '''Adds new riders to RIDERS, if any at the given timestep'''
    global next_rider

    # For reasons of rider-icon encoding and limits on
    # simulation time, don't generate more than 26 riders.
    if next_rider > 25:
        return

    # Pull hails from HAILS list for this timestep
    while next_rider < len(HAILS) \
        and timestep == HAILS[next_rider][0]:

        # Create a new rider
        rider = {
            'loc': HAILS[next_rider][1],
            'dest': HAILS[next_rider][2],
            'car': NO_CAR,
            'waiting': True,
        }

        # Add new rider to the dictionary
        RIDERS[next_rider] = rider

        if show > NOTHING:
            # Document the action
            print(f'{timestep}: Rider {rider_icon(next_rider)} hails a car')
        
        # Bump tracker
        next_rider += 1


def main():
    '''Run a simple unit test'''

    # Pick a configuration
    rider_setup('2', None)

    # Show schedule of rider hails
    indent = 2
    for rider_id, hail in enumerate(HAILS):
        print(f'Rider {rider_id} ({rider_icon(rider_id)})')
        print(' ' * indent, 'timestep:', hail[0])
        print(' ' * indent, 'location:', hail[1])
        print(' ' * indent, 'destation:', hail[2])

if __name__ == "__main__":
    main()
