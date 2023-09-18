import configparser
from sumolib import checkBinary
import os
import sys

def import_test_configuration(config_file):
    """
    Read the config file regarding the testing and import its content
    """
    content = configparser.ConfigParser()
    content.read(config_file)
    config = {'gui': content['simulation'].getboolean('gui'), 
              'max_steps': content['simulation'].getint('max_steps'),
              'n_trains_generated': content['simulation'].getint('n_trains_generated'),
              'episode_seed': content['simulation'].getint('episode_seed'),
              'start_time': content['simulation'].getint('start_time'), 
              'end_time':content['simulation'].getint('end_time'),
              'loading_duration': content['simulation'].getint('loading_duration'),
              'timestep': content['simulation'].getint('timestep'),
              'sumocfg_file_name': content['dir']['sumocfg_file_name'],
              'schedule_file_name': content['dir']['schedule_file_name']}
    return config


def set_sumo(gui, sumocfg_file_name, timestep):
    """
    Configure various parameters of SUMO
    """
    # we need to import python modules from the $SUMO_HOME/tools directory
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # setting the cmd mode or the visual mode    
    if not gui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
 
    # setting the cmd command to run sumo at simulation time
    sumo_cmd = [sumoBinary, "-c", os.path.join('scene', sumocfg_file_name),
                "--no-step-log", "true", "--waiting-time-memory", str(timestep)]

    return sumo_cmd


def set_train_path(models_path_name):
    """
    Create a new model path with an incremental integer, also considering previously created model paths
    """
    models_path = os.path.join(os.getcwd(), models_path_name, '')
    os.makedirs(os.path.dirname(models_path), exist_ok=True)

    dir_content = os.listdir(models_path)
    new_version = ''
    if dir_content:
        previous_versions = [int(name.split("_")[1]) for name in dir_content]
        new_version = str(max(previous_versions) + 1)
    else:
        new_version = '1'

    data_path = os.path.join(models_path, 'model_'+new_version, '')
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    return data_path, new_version


def set_test_path(models_path_name):
    """
    Returns a model path
    """
    model_folder_path = os.path.join(os.getcwd(), models_path_name + '/')

    if os.path.isdir(model_folder_path):
        return model_folder_path
    else: 
        sys.exit('The model number specified does not exist in the models folder')
