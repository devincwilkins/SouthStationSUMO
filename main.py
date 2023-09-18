from __future__ import absolute_import
from __future__ import print_function

from simulation import Simulation
from generator import TrafficGenerator
from utils import import_test_configuration, set_sumo, set_test_path
import pandas as pd

if __name__ == "__main__":
    config = import_test_configuration(config_file='settings/settings.ini')
    print(config)
    sumo_cmd = set_sumo(config['gui'], config['sumocfg_file_name'], config['timestep'])

    TrafficGen = TrafficGenerator(
        config['start_time'], 
        config['end_time'], 
    )
        
    Simulation = Simulation(
        TrafficGen,
        sumo_cmd,
        config['start_time'], 
        config['end_time'], 
        config['loading_duration'],
        config['timestep']
        config['schedule_file_name']
    )

    print('\n----- Begin Simulation Episode')
    # run the simulation
    simulation_time, avg_waiting, trackassigneds, donothings, output = Simulation.run(config['episode_seed'])
    print("\n [STAT] Simulation time:", simulation_time, 's',
          "\n Total assignments and dispatches:", sum(trackassigneds), 
          "\n Trains assigned to each platform:", trackassigneds)
    print('\n----- End Simulation Episode')
    output.to_csv('outputs/simulation_output.csv')
    print('Outputs Saved')
