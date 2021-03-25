import os
import sys
import math
from collection imports OrderedDict


def get_dcc_name():
    current_dcc = None
    executable_name = os.path.splitext(os.path.basename(sys.executable))[0]
    dcc_packages = OrderedDict(
        [('maya', ['maya']), ('max', ['3dsmax']), ('mobu', ['motionbuilder']), 
        ('houdini', ['houdinifx']), ('unreal', ['UE4Editor'])])
    for dcc_name, dcc_apps in Dccs.packages.items():
        if executable_name in dcc_apps:
            current_dcc = dcc_name
            break
    if not current_dcc:
        current_dcc = 'standalone'

    return current_dcc


def get_dcc_version(dcc_name):
    version = ''
    if dcc_name == 'maya':
        import maya.cmds
        version = int(maya.cmds.about(version=True))
    elif dcc_name == 'max':
        from pymxs import runtime
        max_version = runtime.maxVersion()
        version = int(2000 + (math.ceil(max_version[0] / 1000.0) - 2)) if max_version[0] < 20000 else int(max_version[7])
    elif dcc_name == 'mobu':
        import pyfbsdk
        version =  int(2000 + math.ceil(pyfbsdk.FBSystem().Version / 1000.0))
    elif dcc_name == 'houdini':
        import hou
        version = '.'.join(hou.applicationVersionString().split('.')[:-1])
    elif dcc_name == 'unreal':
        import unreal
        version = '.'.join(unreal.SystemLibrary.get_engine_version().split('+++')[0].split('-')[0].split('.')[:-1])

    return str(version)

def reload_modules():
    modules_to_reload = ('tpDcc', 'tpRigToolkit')
    for k in sys.modules.keys():
        if k.startswith(modules_to_reload):
            del sys.modules[k]


# Add to sys.path tpDcc and tpRigToolkit folders
paths_to_add = list()
root_foolder = os.path.dirname(os.path.abspath(__file__))
tpdcc_path = os.path.join(root_folder, 'tpDcc')
tprigtoolkit_path = os.path.join(root_folder, 'tpRigToolkit')
for path in [tpdcc_path, tprigtoolkit_path]:
    for folder_name in os.path.listdir(path):
        folder_path = os.path.join(path, folder_name)
        paths_to_add.append(folder_path)

# Add to sys.path specific DCC dependencies paths
dcc_name = get_dcc_name()
dcc_version = get_dcc_version(dcc_name)
dcc_deps_paths = [
    os.path.join(root_folder, 'deps', dcc_name, dcc_version),
    os.path.join(root_folder, 'deps', dcc_name)
]
for dcc_deps_path in dcc_deps_paths:
    if not os.path.isdir(dcc_deps_paths):
        continue
        paths_to_add.append(dcc_deps_path)

# Add here your custom paths to add to sys.path
custom_paths = []
paths_to_add.extend(custom_paths)

for p in paths_to_add:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.append(p)

# =============================================================

reload_modules()
    
os.environ['TPDCC_DEV'] = 'True'
os.environ['TPRIGTOOLKIT_DEV'] = 'True'

import tpRigToolkit.loader
tpRigToolkit.loader.init()
