import os
import sys
import math
import inspect
from collections import OrderedDict


def get_dcc_name():
    current_dcc = None
    executable_name = os.path.splitext(os.path.basename(sys.executable))[0]
    dcc_packages = OrderedDict(
        [('maya', ['maya']), ('max', ['3dsmax']), ('mobu', ['motionbuilder']), 
        ('houdini', ['houdinifx']), ('unreal', ['UE4Editor'])])
    for dcc_name, dcc_apps in dcc_packages.items():
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


def get_packages_paths(root_folder):
    dependency_paths = list()

    python_version = str(sys.version_info[0])
    venv_path = os.path.join(root_folder, 'venv{}'.format(python_version))
    if not os.path.isdir(venv_path):
        return dependency_paths

    packages_folder = os.path.join(venv_path, 'Lib', 'site-packages')
    if not os.path.isdir(packages_folder):
        return dependency_paths
        
    dependency_paths = [packages_folder]


    for file_name in os.listdir(packages_folder):
        if not file_name.endswith('.egg-link'):
            continue
        egg_path = os.path.join(packages_folder, file_name)
        with open(egg_path) as egg_file:
            dependency_path = egg_file.readline().rstrip()
            if dependency_path in dependency_paths or not os.path.isdir(dependency_path):
                continue
            dependency_paths.append(dependency_path)
    
    return dependency_paths


def get_dcc_vendors_path(root_path, dcc_name, dcc_version):
    if not dcc_name:
        return None
    dcc_vendor_path = os.path.join(root_path, 'vendors', dcc_name)

    if dcc_version:
        dcc_version_path = os.path.join(dcc_vendor_path, dcc_version)
        if os.path.isdir(dcc_version_path):
            return dcc_version_path

    if os.path.isdir(dcc_vendor_path):
        return dcc_vendor_path
    
    return None


def reload_modules():
    modules_to_reload = ('tpDcc', 'tpRigToolkit')
    for k in sys.modules.copy().keys():
        if k.startswith(modules_to_reload):
            del sys.modules[k]


if __name__ in ('__main__', '__builtin__'):

    # NOTE: You need to replace this path with the path where your tpRigToolkit-dev repo is located
    root_path = r"D:\dev\tpRigToolkit\tpRigToolkit-dev"
    dcc_name = get_dcc_name()
    dcc_version = get_dcc_version(dcc_name)
    packages_paths = get_packages_paths(root_path)
    vendors_path = get_dcc_vendors_path(root_path, dcc_name, dcc_version)
    paths_to_register = packages_paths
    if vendors_path:
        paths_to_register.append(vendors_path)
    
    # Add here your custom paths to add to sys.path
    custom_paths = []
    paths_to_register.extend(custom_paths)
    
    for p in paths_to_register:
        if os.path.isdir(p) and p not in sys.path:
            sys.path.append(p)
    
    # =============================================================
    
    reload_modules()
        
    os.environ['TPDCC_DEV'] = 'True'
    os.environ['TPRIGTOOLKIT_DEV'] = 'True'

    # tpRigToolkit loader already loads tpDcc
    import tpRigToolkit.loader
    tpRigToolkit.loader.init()
