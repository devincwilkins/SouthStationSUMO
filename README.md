# South Station SUMO Simulation

## Inputting Schedules (/schedules/*)

## Adjusting Settings (/settings/settings.ini)
gui = (True/False) | Whether you want SUMO to visualize the simulation, runs faster if False
start_time = (Integer value) | Desired start time-of-day of simulation in seconds
end_time = (Integer value) | Desired end time-of-day of simulation in seconds
loading_duration = (Integer value) | Minimum time trains spend at platform for loading/unloading of passengers in seconds
timestep = (Integer value) | How much time to elapse in the simulation at each step in seconds, reccommended value is 10

sumocfg_file_name = (.cfg filename) | Which simulation architecture to use from scene folder
schedule_file_name = (.csv filename) | Which schedule file to use from schedules folder

## Route and Vehicle Information (generator.py)
This file generates a list of scheduled trains as input to this situation. Here you can:

-Edit characteristics of trains such as carriage length and acceleration
-Edit characteristics of routes through the interlocking, specifically the sequence of track segments that define them.


## Architecture of Simulation (/scene/*)
This folder contains all the xml structures that define the South Station model within SUMO, such as links, switches, speed limits. These are best edited within the NetEdit application. 