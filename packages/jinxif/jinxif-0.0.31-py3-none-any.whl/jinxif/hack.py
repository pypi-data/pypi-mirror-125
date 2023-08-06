####
# title: configuration.py
#
# language: Python3.8
# date: 2021-10-27
# license: GPL>=v3
# author: Jenny, bue
#
# description:
#   enabele local config py file for lab specific
#   marker standard, naeming convention, and slurmbatch function. 
#####

# libarary
import os
import shutil

# global var
s_path_module = os.path.abspath(os.path.dirname(__file__))
s_path_module = re.sub(r'jinxif$','jinxif/', s_path_module)

# functions
def link_local_config():
    '''
    '''
    # get paths
    s_path_local = os.path.expanduser('~/.jinxif/')
    s_pathfile_configuration_module = f'{s_path_module}/configuration.py'
    s_pathfile_config_module = f'{s_path_module}/config.py'
    s_pathfile_config_local = os.path.expanduser(f'{s_path_local}/config.py')

    # generate local jinxif config file
    if os.path.isfile(s_pathfile_config_local):
        print(f'Warning @ jinxif.configuration.link_local_config : {s_pathfile_config_local} file already exist. No new config.py file was generated!')
    else:
        os.makedirs(s_path_config, exist_ok=True)
        shutil.copy(s_pathfile_configuration_library, s_pathfile_config_local)
        print(f'Okay @ jinxif.configuration.link_local_config : {s_pathfile_config_local} file generated.\nplease edit the config.py file to your needs!')

    # link local config file
    if os.path.isfile(s_pathfile_config_module) and not os.path.link(s_pathfile_config_module):
            sys.exit(f'Error @ jinxif.configuration.link_local_config : pre-historic jinxif config.py file detected! please:\npip uninstall jinxif\npip install jinxif\nthen re-run link_local_config. thank you!')
    if os.path.isfile(s_pathfile_config_module):
        print(f'Warning @ jinxif.configuration.link_local_config : at\n{s_pathfile_config_module} link to local conf.py file\n{os.path.realpath(s_pathfile_config_local)} already exist. no new link generated!')
    else:
        s_pwd = os.getcwd()
        os.chdir(s_path_module)
        os.symlink(s_pathfile_config_local, 'config.py')
        os.chdir(s_pwd)
        print(f'Okay @ jinxif.configuration.link_local_config : at\n{s_pathfile_config_module} link to local conf.py file\n{os.path.realpath(s_pathfile_config_local)} generated.')




