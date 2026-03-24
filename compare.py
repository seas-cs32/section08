### tpw08/compare.py
import random
from city import CitySqGrid
from consts import NOTHING
from offline import car_setup
from online import rider_setup
import simulate
from tabulate import tabulate

# Infrequently turned simulation knobs
RND_SEED = 42
TRIALS = 1000

def run_trials(our_city, car_layout, timesteps):
    '''Given a city, car layout, and timesteps, simulate
       lots of trials with randomly generated rider
       hails for each trial. This function returns the 
       averages of the statistics we measure. '''
    # Collect statistics
    stats = []

    # Make sure that the trials always start with the same
    # random seed.
    random.seed(RND_SEED)

    # Run the simulations and collect the list of results
    for trial in range(TRIALS):
        # Set car locations for start of day (computed offline)
        success = car_setup(car_layout, our_city)
        assert success, 'This should never fail'

        # Reset the city
        our_city.reset()
        simulate.update_map(our_city)

        # When running lots of simulations, we use the random
        # hail stream. Reset it for the next simulation.
        success = rider_setup('r', our_city)
        assert success, 'Random rider_setup failed'
        
        # Run simulation
        results = simulate.simulate(our_city, timesteps,
                                    delay=0.0, show=NOTHING)

        stats.append(results)

    # Compute the desired statistics for these trials. Currently,
    # this is just an arithmetic average.
    mins_waiting = 0
    mins_idle = 0
    miles_driven = 0

    for elem in stats:
        mins_waiting += elem[0]
        mins_idle += elem[1]
        miles_driven += elem[2]

    return (mins_waiting / TRIALS,
            mins_idle / TRIALS,
            miles_driven / TRIALS)


def main():
    # Build a city
    our_city = CitySqGrid(6)

    # Grab two offline car setups from the user separated by a comma
    while True:
        car_layout = input(
            'Which two car layouts would you like to compare? ')
        
        try:
            # Separate and strip off whitespace
            layout1, layout2 = car_layout.split(',')
            layout1, layout2 = layout1.strip(), layout2.strip()

            # Verify that they're valid setups
            success = car_setup(layout1, our_city)
            success = success and car_setup(layout2, our_city)
            if success:
                break
            else:
                print('Please try again...')
        except ValueError:
            print('Invalid input. Should be of the form "int, int"')

    # Grab desired timesteps in each simulation
    while True:
        try:
            ans = input('How long would you like each simulation to run? ')
            timesteps = int(ans)
            if timesteps <= 0:
                raise ValueError
            break
        except ValueError:
            print('Must be a positive integer. Try again...')

    # Setup for tabulate output
    headers = ['Statistic (avg/day)', f'Car Layout {layout1}', f'Car Layout {layout2}']
    data = [
        ['Total mins waiting'],
        ['Total mins idle'],
        ['Total miles driven'],
    ]

    # Run the simulations for each layout
    for layout in [layout1, layout2]:
        # Print car layout so user knows what we did
        print(f'### Car Layout {layout} ###')
        our_city.reset()
        car_setup(layout, our_city)
        rider_setup('r', our_city)
        simulate.update_map(our_city)
        print(our_city)

        # Run trials for this layout
        results = run_trials(our_city, layout, timesteps)

        # Add these results to the data list
        data[0].append(results[0])
        data[1].append(results[1])
        data[2].append(results[2])

    # Print the results of the comparison
    print(tabulate(data, headers=headers, tablefmt="grid"))

if __name__ == '__main__':
    main()
