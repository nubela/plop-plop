from bitbucket.bitbucket import Bitbucket

from colorama import init, Fore
from cfg import WORKSPACE_DIR, PLOP_PROJECT_PATH, WATCHER_FILE_PATH, RESOURCES_PATH, ANDROID_SDK_PATH_LIS, ANDROID_PHONEGAP_BIN_PATH, IOS_PHONEGAP_BIN_PATH, BITBUCKET_USERNAME, BITBUCKET_PASSWD
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
    common_mobile_folder = new_mobile_proj_path(project_name)
    ios_path = new_ios_project(project_name, common_mobile_folder)
    android_path = new_android_project(project_name, common_mobile_folder)
    cfg_path = new_cfg_project(project_name)
    put_backend(project_name)
    put_platform(project_name)
    put_git([plop_path, ios_path, android_path, cfg_path])
    cprint("All done.")


@manager.command
def rm_repo(project_name):
    """
    Shortcut to delete bitbucket repositories for the projects.
    """
    cprint("Deleting repositories..")
    repositories_to_del = [
        "%s-ios" % (project_name),
        "%s-android" % (project_name),
        "%s-plop" % (project_name),
        "%s-cfg" % (project_name),
    ]
    bb = Bitbucket(BITBUCKET_USERNAME, BITBUCKET_PASSWD)
    for r in repositories_to_del:
        cprint(".. Working on %s" % (r))
        bb.repository.delete(r)
        cprint(".. Repository deleted")
    cprint("All done.")


@manager.command
def add_repo(project_name):
    """
    Create bitbucket repositories for the projects, and then adds them to the bitbucket
    """
    cprint("Creating repositories..")
    #create em repositories
    repositories_to_create = [
        "%s-ios" % (project_name),
        "%s-android" % (project_name),
        "%s-plop" % (project_name),
        "%s-cfg" % (project_name),
    ]
    bb = Bitbucket(BITBUCKET_USERNAME, BITBUCKET_PASSWD)
    for r in repositories_to_create:
        cprint(".. Working on %s" % (r))
        bb.repository.create(r, private=True)
        cprint(".. Repository created")

    #add remote to the various project folders
    proj_folders = map(lambda x: (x, os.path.join(WORKSPACE_DIR, project_name, x)), repositories_to_create)
    for p_name, pf in proj_folders:
        cmds = [
            "cd %s" % (pf),
            "git remote add origin https://unifide@bitbucket.org/unifide/%s.git" % (p_name),
        ]
        full_cmd = " && ".join(cmds)
        cprint(".. Adding remote to %s project" % (p_name))
        os.system(full_cmd)

    cprint("All done.")


@manager.command
def push(project_name):
    """
    Pushes projects to their relevant repositories.
    """
    cprint("Pushing..")
    proj_ws = _proj_workspace(project_name)
    folders_to_push = [
        os.path.join(proj_ws, "%s-ios" % (project_name)),
        os.path.join(proj_ws, "%s-android" % (project_name)),
        os.path.join(proj_ws, "%s-plop" % (project_name)),
        os.path.join(proj_ws, "%s-cfg" % (project_name)),
    ]
    for f in folders_to_push:
        cprint(".. Pushing in %s" % (f))
        cmd_lis = [
            "cd %s" % (f),
            "git push",
        ]
        _run_cmd_lis(cmd_lis)
    cprint("Done.\n")


@manager.command
def deploy(project_name):
    """
    """
    pass

#-- helper methods --#

def new_mobile_proj_path(project_name):
    cprint("Creating a bridging www folder for Phonegap..")

    cfg_project_path = os.path.join(_proj_workspace(project_name), "%s-www" % (project_name))
    cmd_lis = [
        "cd %s" % (RESOURCES_PATH),
        "cp -R %s %s" % ("www", cfg_project_path),
    ]
    _run_cmd_lis(cmd_lis)

    cprint("Done.\n")
    return cfg_project_path


def new_folder(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def _put_generic_watcher(project_path, path_to_watch):
    watcher_file_path = os.path.join(project_path, "WATCHER.sh")
    f = open(watcher_file_path, "w+")
    s = "\n".join([
        "#!/bin/bash",
        "python %s %s" % (WATCHER_FILE_PATH, path_to_watch),
    ])
    f.write(s)
    os.system("chmod +x %s" % (watcher_file_path))
    f.close()


def _put_plop_watcher(project_path):
    path_to_watch = os.path.join(project_path, "web")
    _put_generic_watcher(project_path, path_to_watch)


def new_plop_project(project_name):
    cprint("Working on plop..")

    #create folder
    proj_path = os.path.join(_proj_workspace(project_name), "%s-plop" % (project_name))
    cmd_lis = [
        "cd %s" % (RESOURCES_PATH),
        "cp -R %s %s" % ("plop_proj", proj_path),
    ]
    _run_cmd_lis(cmd_lis)

    #create virtualenv
    cprint(".. Creating virtualenv")
    venv_lis = [
        "cd %s" % (proj_path),
        "virtualenv v_env"
    ]
    _run_cmd_lis(venv_lis)

    #pip install requirements
    cprint(".. (pip) Installing requirements")
    pip_install_cmd_lis = [
        "cd %s" % (proj_path),
        "source v_env/bin/activate",
        "pip install -r REQUIREMENTS",
    ]
    _run_cmd_lis(pip_install_cmd_lis)

    #link base
    base_package_path = os.path.join(PLOP_PROJECT_PATH, "base")
    ln_cmd_lis = [
        "cd %s" % (proj_path),
        "ln -s %s" % (base_package_path)
    ]
    _run_cmd_lis(ln_cmd_lis)

    #add watcher
    _put_plop_watcher(proj_path)
    cprint("Done.\n")
    return proj_path


def new_android_project(project_name, www_folder):
    cprint("Working on Android project..")
    export_cmd = ":".join(["export PATH=${PATH}:"] + ANDROID_SDK_PATH_LIS)
    path_to_new_project = os.path.join(_proj_workspace(project_name), "%s-android" % (project_name))
    commands = [
        export_cmd,
        "cd %s" % (ANDROID_PHONEGAP_BIN_PATH),
        "./create %s %s %s" % (
            path_to_new_project, "com.unifide.%s" % (project_name), project_name)
    ]
    str_of_cmds = " && ".join(commands)
    os.system(str_of_cmds)

    #replace www
    cprint(".. Replacing www")
    www_folder_path = os.path.join(path_to_new_project, "www")
    cmd_lis = [
        "rm -rf %s" % (www_folder_path),
        "cd %s" % (RESOURCES_PATH),
        "cp -R %s %s" % ("www", path_to_new_project),
    ]
    _run_cmd_lis(cmd_lis)

    #put watcher
    cprint(".. Adding Watcher")
    path_to_watch = os.path.join(_proj_workspace(project_name), "%s-www" % (project_name))
    _put_generic_watcher(path_to_new_project, path_to_watch)

    cprint("Done.\n")
    return path_to_new_project


def new_ios_project(project_name, www_folder):
    cprint("Working on iOS project..")
    path_to_new_project = os.path.join(_proj_workspace(project_name), "%s-ios" % (project_name))
    commands = [
        "cd %s" % (IOS_PHONEGAP_BIN_PATH),
        "./create %s %s %s" % (
            path_to_new_project, "com.unifide.%s" % (project_name), project_name)
    ]
    str_of_cmds = " && ".join(commands)
    os.system(str_of_cmds)

    #replace www
    cprint(".. Replacing www")
    www_folder_path = os.path.join(path_to_new_project, "assets", "www")
    cmd_lis = [
        "rm -rf %s" % (www_folder_path),
        "cd %s" % (RESOURCES_PATH),
        "cp -R %s %s" % ("www", os.path.join(path_to_new_project, "assets")),
    ]
    _run_cmd_lis(cmd_lis)

    #put watcher
    cprint(".. Adding Watcher")
    path_to_watch = os.path.join(_proj_workspace(project_name), "%s-www" % (project_name))
    _put_generic_watcher(path_to_new_project, path_to_watch)
    cprint("Done.\n")
    return path_to_new_project


def proj_exists(project_name):
    folder_name = "%s" % (project_name)
    proj_path = os.path.join(WORKSPACE_DIR, folder_name)
    return os.path.exists(proj_path)


def cprint(text):
    print("%s%s%s" % (Fore.RED, text, Fore.RESET))


def put_git(path_lis):
    for path in path_lis:
        cmd_lis = [
            "cd %s" % (path),
            "git init",
        ]
        cprint(".. Initialising git on %s" % (path))
        _run_cmd_lis(cmd_lis)


def _run_cmd_lis(cmd_lis):
    full_cmd = " && ".join(cmd_lis)
    os.system(full_cmd)


def new_cfg_project(project_name):
    """
    Recursively copies the cfg project from resources to the project workspace
    """
    cprint("Working on CFG project..")
    cfg_project_path = os.path.join(_proj_workspace(project_name), "%s-cfg" % (project_name))
    cmd_lis = [
        "cd %s" % (RESOURCES_PATH),
        "cp -R %s %s" % ("cfg_proj", cfg_project_path),
    ]
    _run_cmd_lis(cmd_lis)
    cprint("Done.\n")
    return cfg_project_path


def put_backend(project_name):
    """
    Clones a brand new unifide backend project
    """
    cprint("Cloning backend project..")
    #clone git repository
    cmd_lis = [
        "cd %s" % (_proj_workspace(project_name)),
        "git clone git@bitbucket.org:kianwei/unifide-backend.git",
    ]
    _run_cmd_lis(cmd_lis)

    #link cfg
    pass

    cprint("Done.\n")
    return os.path.join(_proj_workspace(project_name), "unifide-backend")


def put_platform(project_name):
    cprint("Cloning platform project..")
    #clone git repository
    cmd_lis = [
        "cd %s" % (_proj_workspace(project_name)),
        "git clone git@bitbucket.org:kianwei/unifide-platform.git",
    ]
    _run_cmd_lis(cmd_lis)

    #link cfg
    pass

    #setup RunMeteor file
    pass

    cprint("Done.\n")
    return os.path.join(_proj_workspace(project_name), "unifide-backend")


def _proj_workspace(project_name):
    p = os.path.join(WORKSPACE_DIR, project_name)
    if not os.path.exists(p):
        cprint(".. Creating project workspace at %s" % (p))
        new_folder(p)
        cprint(".. Done creating workspace.")
    return p

#-- main --#

if __name__ == '__main__':
    init()
    manager.main()