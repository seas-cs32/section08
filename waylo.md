### Introduction to the Waylo Lab

A ride-hailing service built on driverless vehicles depends not only on an autonomous driving technology that can safely navigate our roadways but also on an algorithm that provisions the right-sized fleet and positions these cars to quickly meet dynamically changing demand. This algorithm is an excellent example of _offline-online processing_, and your challenge for the day is to design and implement a portion of the online algorithms of a simple ride-hailing service using driverless cars.

Our company is called _Waylo_, and its service runs in a city in the southwestern United States with a Mahattan-like grid of streets. The company bought the **offline** portion of the provisioning algorithm, which sets the number of driverless cars available for the day and where these cars start across the city. These decisions are based on historical trends, maintenance schedules, the day's road closures, and any currently running corporate promotions. Unfortunately, the portion of the **online** algorithm that assigns cars to hailing riders was poorly done, and the company has asked you to reimplement it.

Open the "Section Week #8" assignment on Gradescope, which contains questions you'll answer as you work through these steps.

Make sure you've previously grabbed the `chap11` files via `python3 grab32.py chap11`.

----

### Step 1: Try the simulator

You've been given a simulator with which you will be able to test different rider assignment algorithms. To get a feel for how it works, run the simulator by typing `python3 simulate.py` at the Terminal prompt.

1.  When it asks what car layout to use, try a number between 1 and 4. These numbers correspond to different starting configurations of cars at the beginning of the day.

2.  When it asks what hail stream to use, try a number between 1 and 2. The hail stream describes how riders arrive, where they hailed from, and where they want to go.

3. When it asks how long (in timesteps) the simulation should run, choose a value between 15-40. Car setup 1 and hail stream 1 is a simple scenario that completes in less than 15 timesteps. The car setups with rider setup 2 typically complete in less than 40 timesteps.

4. After the first map is printed, resize your Terminal window so that it can display the entire map. This will create the best viewing experience. The simulator uses ASCII character art in the following ways:

    * Waylo cars are printed as numbers.
    * Waiting riders are printed as little letters.
    * Riders in a moving Waylo car are printed as capital letters.
    * Squares containing cars and/or riders (i.e., a square where we have to print more than a single digit or letter) are printed as a `*`.

    When you're ready to see this in action, start the simulation (by "pressing the return key to start...")

5. Make sure that you and your partner understand what the simulator is showing you. If you want the simulation to run faster or slower, you can decrease or increase the `DELAY` in `consts.py`.

6. Run the simulation with a couple of different car layouts and hail streams. You can also try a random hail stream by typing `r` when the simulator asks which hail stream to use.

----

### Step 2: Learn about the simulator's organization

There are five main files associated with this simulator:

*   `consts.py` and `city.py`: The first file defines a few useful constants and the second implements the city grid. You will NOT need to change or even look at these two files (unless you want to adjust the `DELAY` in `consts.py`).

*   `offline.py`: This module creates an empty dictionary called `CARS` within which we keep track of deployed Waylo cars. Cars are named with a number from 1-9, which are also the keys to the `CARS` dictionary. Each car is described by three values:

    * `'loc'`: This car's current location on the map. Map locations are tuples of the form `(x,y)`, where `(0,0)` is the lower left-hand corner of the map.
    * `'dest'`: This car's intended destination (as a map location). It will be `NO_DEST` when the car is awaiting an assignment. It will be the waiting rider's location when a car is headed to a pick-up. Once the car picks up its rider, this value becomes the rider's destination. It returns to `NO_DEST` when the rider is dropped off.
    * `'rider'`: The rider identifier assigned to this car. It will be `NO_RIDER` when the car is awaiting an assignment and after a rider is dropped off at their destination.

    The function `car_setup` allows you to run the simulation with a number of different starting configurations (i.e., where the Waylo cars start their day). Feel free to create additional configurations, but what's already defined is all you need for this lab.

    The `main` function runs a simple unit test on this module. You don't need it.

*   `online.py`: This module creates an empty dictionary called `RIDERS` within which we keep track of current active Waylo users (i.e., those individuals currently waiting for or riding in a Waylo car). Riders are numbered, but these numbers become letters of the alphabet when riders are printed on the city map (see the function `rider_icon`). Each rider is described by four values:

    * `'loc'`: This rider's current location on the map.
    * `'dest'`: This rider's intended destination on the map.
    * `'car'`: The car identifier assigned to this rider. It will be `NO_CAR` until this assignment is made.
    * `'waiting'`: A Boolean that is `True` if the rider is waiting to be picked up.

    The simulator generates rider hails in one of two ways, as seen in the function `rider_setup`:
    
    1.  From a list of tuples defining the timestep at which this rider hails a Waylo car, where they want to be picked up, and where they want to be dropped off. These tuples must be in timestep order.
    2.  A randomly generated hail stream (with help from `rand_schedule` and `rand_locs`).
    
    You might choose to create new configurations in `rider_setup`, but you don't have to touch the functions `add_hails`, `rand_schedule`, or `rand_locs`. 
    
    Like `offline.py`, the `main` function runs a simple unit test on this module. You'll only need it if you decide to create a new rider configuration and you want to see that you did it correctly.

    > **Answer on Gradescope:** Given an active Waylo car named `car` and a Waylo rider named `rider`, how would you calculate (in Python) the distance between the car and the rider? Remember that `car` and `rider` are both represented as dictionaries.

*   `simulate.py`: This is the script you'll hand to the Python interpreter to run the Waylo simulator. We briefly describe its contents from the bottom up.

    The `main` function permits a user to use one car layout with one hail stream. You indicate how many timesteps you'd like in a day, and the simulator prints out what happens at each timestep. At the end of the day, a few statistics are printed about the Waylo operation:

    * Total miles driven by all Waylo cars that day.
    * Total minutes spent by the hailing riders while waiting to be picked up.
    * Total minutes spent by all Waylo cars idling (i.e., waiting to be assigned a rider).

    `simulate` is the workhorse routine. It contains a loop over the timesteps, and for each loop iteration, it performs the following actions in the order below:

    1. `make_assignments`, which attempts to make a good assignment of hailing riders to empty cars. This is the routine that you'll rewrite. It currently uses a very dumb algorithm. Once you've decided to assign a rider to a car, you call the helper routine `assign` to update the car and rider data structures.

    2. `move_cars`, which moves the cars with active destinations towards their destinations. You don't have to understand how this routine does its work.

    3. `add_hails`, which is imported from the `online` module. This routine simulates a rider requesting a Waylo car in the current timestep. You don't have to understand the logic in this routine. You simply need to know that a rider hails a car in one timestep and the earliest they can be assigned to a car is the next timestep.

    4. Next, the loop body updates the simulation statistics based on the actions in this timestep.

    5. `update_map` and possibly show the current map of cars and riders. Running `simulate.py` will show the map on each timestep.
----

### Step 3: Re-implement the online component

As we mentioned in Step 2, the current algorithm for `make_assignments` in `simulate.py` doesn't assign cars to riders in a thoughtful way. To see why, run the simulation a few more times. Try different car layouts (1-4) and the random hail stream (`r`) for ~80 timesteps. Read through the code in `make_assignments`.

> **Answer on Gradescope:** How is `make_assignments` currently assigning cars to riders? Why is it not a smart algorithm?

Think about how you can make it better (i.e., how you might better assign waiting riders to idle Waylo cars so that _the total rider wait time_ is minimized). 

Starting with a simple improvement, write a new version of `make_assignments`. Keep the old version so that you can switch between them (i.e., comment out the existing `make_assignments` and write a new one).

Test it using the simulation.

When your first simple improvement works, try adding another improvement.

When you are satisfied that your new version of `make_assignments` reduces total rider wait time:

> **Answer on Gradescope:** Describe the improvements you made to `make_assignments`. Why do you expect your new algorithm to perform better than the original dumb algorithm?

> **Answer on Gradescope:** What simulation parameters (car layout(s) and hail stream(s)) demonstrated that your new algorithm performs better than the original dumb algorithm?

> **Answer on Gradescope:** Were there any simulation parameters that did not yield improvements over the original dumb algorithm? Why do you think the results did not improve?

>**Upload** your final version of `simulate.py` to the last question Gradescope.

>**Submit** the assignment on Gradescope.

----

### Step 4: What are you learning about scheduling?

Let's spend a few minutes thinking about other metrics of interest. For example, the simulator keeps track of the total miles driven and total minutes spent idle in a day by Waylo cars.  Minutes waiting is a metric of interest to both the company and its riders. These two other metrics are something the company cares about (but not the riders).

For example, car configuration 1 uses two Waylo cars while configuration 4 uses three Waylo cars. With more cars, the wait times for customers are generally decreased, but the amount of idle time goes up. You can see this by running `python3 compare.py`. (You may need to install the `tabluate` module by running `pip install tabulate`). At the first prompt, type `1,4`, which says that you want to compare car configuration 1 (two Waylo cars) against configuration 4 (three Waylo cars). When asked how long to run an individual simulation, say `50` timesteps.

What is the right balance between (expensive) idle Waylo cars and waiting rider frustration? How might you use these scripts to figure out the answer to this question? 

> **Talk to your partner and tablemates about this question.** You do not need to answer this question on Gradescope.

Version 20260324
