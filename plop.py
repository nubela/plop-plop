from distutils.file_util import copy_file

from colorama import init, Fore
from cfg import WORKSPACE_DIR, REQUIREMENTS, PLOP_PROJECT_PATH, WATCHER_FILE_PATH, PROJ_FILES, RESOURCES_PATH, ANDROID_SDK_PATH_LIS, ANDROID_PHONEGAP_BIN_PATH, IOS_PHONEGAP_BIN_PATH
import os
from manager import Manager


manager = Manager()


@manager.command
def new(project_name):
    """
    Generates a new plop project (website), an iOS Phonegap project, and an Android project.
    """
    if proj_exists(project_name):
        cprint("Project already exists.")

    cprint("Creating project..")
    plop_path = new_plop_project(project_name)
    ios_path = new_ios_project(project_name)
    android_path = new_android_project(project_name)
    # put_git([plop_path, ios_path, android_path])
    cprint("All done.")


@manager.command
def create_repository(project_name):
    """
    Create bitbucket repositories for the projects.
    """
    pass


@manager.command
def push(project_name):
    """
    Pushes projects to their relevant repositories.
    """
    return "pushed"


@manager.command
def deploy(project_name):
    """
    """
    pass

#-- helper methods --#

def new_folder(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def _put_plop_requirements(proj_path):
    req_file = os.path.join(proj_path, "REQUIREMENTS")
    f = open(req_file, "w+")
    requirements_str = "\n".join(REQUIREMENTS)
    f.write(requirements_str)
    f.close()


def _put_watcher(project_path):
    watcher_file = os.path.join(project_path, "WATCHER.sh")
    path_to_watch = os.path.join(project_path, "web")
    f = open(watcher_file, "w+")
    s = "\n".join([
        "#!/bin/bash",
        "python %s %s" % (WATCHER_FILE_PATH, path_to_watch),
    ])
    f.write(s)
    f.close()


def _put_plop_files(project_path):
    #cp web folder to project path
    mv_cmd = 'cd %s && cp -R %s %s' % (RESOURCES_PATH, "web", project_path)
    os.system(mv_cmd)
    for cfg_file in PROJ_FILES: copy_file(cfg_file, project_path)

    #link base
    base_package_path = os.path.join(PLOP_PROJECT_PATH, "base")
    ln_cmd = 'cd %s && ln -s %s' % (project_path, base_package_path)
    os.system(ln_cmd)

    #add watcher
    _put_watcher(project_path)

    #update cfg.py
    pass


def new_plop_project(project_name):
    cprint("Working on plop..")

    #create folder
    folder_name = "%s-plop" % (project_name)
    cprint(".. Creating folder at %s" % (folder_name))
    proj_path = os.path.join(WORKSPACE_DIR, folder_name)
    new_folder(proj_path)

    #create virtualenv
    cprint(".. Creating virtualenv")
    v_cmd = 'cd %s && virtualenv v_env' % (proj_path)
    os.system(v_cmd)

    #create REQUIREMENTS file
    cprint(".. Creating REQUIREMENTS file")
    _put_plop_requirements(proj_path)

    #pip install requirements
    cprint(".. (pip) Installing requirements")
    install_cmds = [
        "cd %s" % (proj_path),
        "source v_env/bin/activate",
        "pip install -r REQUIREMENTS",
    ]
    install_cmd = " && ".join(install_cmds)
    os.system(install_cmd)

    #put files
    cprint(".. Putting files into the project folder")
    _put_plop_files(proj_path)
    cprint("Done.\n")
    return proj_path


def new_android_project(project_name):
    cprint("Working on Android project..")
    export_cmd = ":".join(["export PATH=${PATH}:"] + ANDROID_SDK_PATH_LIS)
    path_to_new_project = os.path.join(WORKSPACE_DIR, "%s-android" % (project_name))
    commands = [
        export_cmd,
        "cd %s" % (ANDROID_PHONEGAP_BIN_PATH),
        "./create %s %s %s" % (
            path_to_new_project, "com.unifide.%s" % (project_name), project_name)
    ]
    str_of_cmds = " && ".join(commands)
    os.system(str_of_cmds)
    cprint("Done.\n")
    return path_to_new_project


def new_ios_project(project_name):
    cprint("Working on iOS project..")
    path_to_new_project = os.path.join(WORKSPACE_DIR, "%s-ios" % (project_name))
    commands = [
        "cd %s" % (IOS_PHONEGAP_BIN_PATH),
        "./create %s %s %s" % (
            path_to_new_project, "com.unifide.%s" % (project_name), project_name)
    ]
    str_of_cmds = " && ".join(commands)
    os.system(str_of_cmds)
    cprint("Done.\n")
    return path_to_new_project


def proj_exists(project_name):
    folder_name = "%s-plop" % (project_name)
    proj_path = os.path.join(WORKSPACE_DIR, folder_name)
    return os.path.exists(proj_path)


def cprint(text):
    print("%s%s%s" % (Fore.RED, text, Fore.RESET))


def put_git(path_lis):
    #put gitignore

    #git init
    pass

#-- main --#

if __name__ == '__main__':
    init()
    manager.main()