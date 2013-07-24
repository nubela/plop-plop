import json
from random import choice
import uuid
from bitbucket.bitbucket import Bitbucket

from colorama import init, Fore
from cfg import WORKSPACE_DIR, PLOP_PROJECT_PATH, WATCHER_FILE_PATH, RESOURCES_PATH, ANDROID_SDK_PATH_LIS, ANDROID_PHONEGAP_BIN_PATH, IOS_PHONEGAP_BIN_PATH, BITBUCKET_USERNAME, BITBUCKET_PASSWD, BACKEND_CFG, PLOP_LIBRARIES, DICT_FILE, METEOR_PORT_RANGE
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
    cfg_path = new_cfg_project(project_name)
    plop_path = new_plop_project(project_name)
    common_mobile_folder = new_mobile_proj_path(project_name)
    ios_path = new_ios_project(project_name, common_mobile_folder)
    android_path = new_android_project(project_name, common_mobile_folder)
    put_backend(project_name)
    put_platform(project_name)
    put_git([plop_path, ios_path, android_path, cfg_path])
    put_sync_file(project_name, common_mobile_folder, ios_path, android_path)

    cprint("All done.")

    next_steps = """
Your project is now created at %s.
The SHPAML files in your projects are not yet converted, so pleaes do a ./WATCHER before you begin each sub-project.

Backend: You will need to update brand_cfg.py and then run python configure_brand.py when you are done.
PS: Your next command should be python plop.py add_repo <proj_name>
    """ % (os.path.join(WORKSPACE_DIR, project_name))
    return next_steps


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
            "git push origin master",
        ]
        _run_cmd_lis(cmd_lis)
    cprint("Done.\n")


def _clone_deployment_projects(project_name):
    git_repos = [
        "git@bitbucket.org:unifide/%s-cfg.git" % (project_name),
        "git@bitbucket.org:unifide/%s-plop.git" % (project_name),
        "git@bitbucket.org:kianwei/unifide-platform.git",
        "git@bitbucket.org:kianwei/unifide-backend.git",
    ]
    proj_workspace = _proj_workspace(project_name)
    for repo in git_repos:
        cmd_lines = [
            "cd %s" % (proj_workspace),
            "git clone %s" % (repo),
        ]
        cprint(".. Cloning %s" % (repo))
        _run_cmd_lis(cmd_lines)


def _deploy_ready_cfg(project_name):
    """
    Update backend's project's cfg.py for deployment
    """
    cfg_project_path = _cfg_proj_path(project_name)
    platform_url = "http://unifide.%s.unifide.sg" % (project_name)
    backend_url = "http://backend.%s.unifide.sg" % (project_name)
    plop_url = "http://%s.unifide.sg/" % (project_name)

    #update cfg.js
    js_cfg_file_path = os.path.join(cfg_project_path, "cfg.js")
    all_lines = [
        'BACKEND_URL = "%s/";' % (backend_url),
        'PLATFORM_URL = "%s/";' % (platform_url),
    ]
    f = open(js_cfg_file_path, "w")
    f.write("\n".join(all_lines))
    f.close()

    #update cfg.py
    py_cfg_file_path = os.path.join(cfg_project_path, "cfg.py")
    f = open(py_cfg_file_path, "r")
    lines = f.readlines()
    f.close()
    final_lines = []
    for l in lines:
        l = l.replace("127.0.0.1:3000", platform_url)
        l = l.replace("localhost:3000", platform_url)
        l = l.replace("localhost:5000", backend_url)
        l = l.replace("127.0.0.1:5000", backend_url)
        l = l.replace("127.0.0.1:5001", plop_url)
        l = l.replace("localhost:5001", plop_url)
        l = l.replace("\n", "")
        final_lines += [l]
    f = open(py_cfg_file_path, "w")
    f.write("\n".join(final_lines))
    f.close()


def _deploy_brand_cfg(project_name):
    backend_path = _backend_path(project_name)
    cmd_lis = [
        "cd %s" % (backend_path),
        ". v_env/bin/activate",
        "cd %s" % (os.path.join(backend_path, "src")),
        "python configure_brand.py",
    ]
    _run_cmd_lis(cmd_lis)


def _compile_platform(project_name):
    platform_path = _platform_path(project_name)
    cmd_lis = [
        "cd %s" % (platform_path),
        "rm -f app.tgz",
        "rm -rf bundle",
        "mrt bundle app.tgz",
        "tar zxvf app.tgz",
        "cd bundle/server/node_modules",
        "rm -r fibers",
        "npm install fibers@1.0.0",
    ]
    _run_cmd_lis(cmd_lis)


def _update_nginx_for_flask(plop_file_name, plop_name, project_name, staging_plop_cfg_path):
    staging = open(staging_plop_cfg_path, "r")
    staging_material = staging.read()
    staging = staging % {
        "proj_name": plop_name,
        "proj_url": plop_file_name,
        "proj_path": _plop_path(project_name),
    }
    staging.close()
    staging = open(staging_plop_cfg_path, "w")
    staging.write(staging_material)
    staging.close()


def _prep_nginx_config(project_name):
    """
    Preps the config file for backend, plop and platform
    """
    cwd = os.getcwd()
    meteor_cfg_path = os.path.join(RESOURCES_PATH, "NGINX_CONFIG_FOR_METEOR")
    flask_cfg_path = os.path.join(RESOURCES_PATH, "NGINX_CONFIG_FOR_FLASK")
    backend_file_name = "backend.%s.unifide.sg" % (project_name)
    backend_name = "%s-backend" % (project_name)
    platform_file_name = "platform.%s.unifide.sg" % (project_name)
    platform_name = "%s-platform" % (project_name)
    plop_name = "%s-plop" % (project_name)
    plop_file_name = "%s.unifide.sg" % (project_name)
    staging_backend_cfg_path = os.path.join(cwd, backend_file_name)
    staging_plop_cfg_path = os.path.join(cwd, plop_file_name)
    staging_platform_cfg_path = os.path.join(cwd, platform_file_name)
    meteor_port = _get_avail_port()

    #copy cfg to staging
    cmd_lis = [
        "cp %s %s" % (flask_cfg_path, staging_backend_cfg_path),
        "cp %s %s" % (flask_cfg_path, staging_plop_cfg_path),
        "cp %s %s" % (meteor_cfg_path, staging_platform_cfg_path),
    ]
    _run_cmd_lis(cmd_lis)

    #update backend
    _update_nginx_for_flask(backend_file_name, backend_name, project_name, staging_backend_cfg_path)

    #update plop
    _update_nginx_for_flask(plop_file_name, plop_name, project_name, staging_plop_cfg_path)

    #update platform
    staging = open(staging_platform_cfg_path, "r")
    staging_material = staging.read()
    staging = staging % {
        "proj_name": platform_name,
        "port": meteor_port,
        "proj_url": platform_file_name,
    }
    staging.close()
    staging = open(staging_platform_cfg_path, "w")
    staging.write(staging_material)
    staging.close()

    return backend_file_name, plop_file_name, platform_file_name, meteor_port


@manager.command
def deploy(project_name):
    """
    (This command should be executed in the production machine)
    Deploys a project that is already pushed to bitbucket onto a production machine.
    """
    cprint("Deploying..")

    cprint(".. Cloning projects")
    _clone_deployment_projects(project_name)

    #create virtualenv
    cprint(".. Creating and installing requirements for virtualenv (Backend)")
    backend_path = _backend_path(project_name)
    src_path = os.path.join(backend_path, "src")
    _put_venv(backend_path)
    _pip_install(backend_path)

    cprint(".. Creating and installing requirements for virtualenv (Platform)")
    plop_path = _plop_path(project_name)
    _put_venv(plop_path)
    _pip_install(plop_path)

    cprint(".. Linking libraries from plop")
    _link_plop_libs(plop_path)
    _link_plop_libs(src_path)

    cprint(".. Linking cfg for backend/platform")
    _link_backend_cfg(src_path, project_name)
    _link_backend_cfg(plop_path, project_name)

    cprint(".. Updating projects' config")
    _deploy_ready_cfg(project_name)

    cprint(".. Configuring brand config")
    _deploy_brand_cfg(project_name)

    cprint(".. Compiling Platform into NodeJS app")
    _compile_platform(project_name)

    #nginx setup
    cprint(".. Preparing nginx site config")
    backend_filename, plop_filename, platform_filename, meteor_port_no = _prep_nginx_config(project_name)

    cprint(".. Copying and enabling site config")
    cmd_lis = [
        "cd %s" % (os.getcwd()),
        "sudo cp %s /etc/nginx/sites-available/" % (plop_filename),
        "sudo cp %s /etc/nginx/sites-available" % (backend_filename),
        "sudo cp %s /etc/nginx/sites-available" % (platform_filename),
        "cd /etc/nginx/sites-enabled",
        "sudo ln -s /etc/nginx/sites-available/%s" % (plop_filename),
        "sudo ln -s /etc/nginx/sites-available/%s" % (backend_filename),
        "sudo ln -s /etc/nginx/sites-available/%s" % (platform_filename),
    ]
    _run_cmd_lis(cmd_lis)

    cprint(".. Launching NodeJS app and FCGI apps")

    cprint(".. Reloading nginx")

    return """
Done! Please set your DNS.
    """

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


def _link_plop_libs(proj_path):
    for lib in PLOP_LIBRARIES:
        base_package_path = os.path.join(PLOP_PROJECT_PATH, lib)
        to_del = os.path.join(proj_path, lib)
        ln_cmd_lis = [
            "cd %s" % (proj_path),
            "rm -f %s" % (to_del),
            "ln -s %s" % (base_package_path)
        ]
        _run_cmd_lis(ln_cmd_lis)


def _plop_path(project_name):
    return os.path.join(_proj_workspace(project_name), "%s-plop" % (project_name))


def _put_venv(proj_path):
    venv_lis = [
        "cd %s" % (proj_path),
        "virtualenv v_env"
    ]
    _run_cmd_lis(venv_lis)


def _pip_install(proj_path):
    pip_install_cmd_lis = [
        "cd %s" % (proj_path),
        ". v_env/bin/activate",
        "pip install -r REQUIREMENTS",
    ]
    _run_cmd_lis(pip_install_cmd_lis)


def new_plop_project(project_name):
    cprint("Working on plop..")

    #create folder
    proj_path = _plop_path(project_name)
    cmd_lis = [
        "cd %s" % (RESOURCES_PATH),
        "cp -R %s %s" % ("plop_proj", proj_path),
    ]
    _run_cmd_lis(cmd_lis)

    #create virtualenv
    cprint(".. Creating virtualenv")
    _put_venv(proj_path)

    #pip install requirements
    cprint(".. (pip) Installing requirements")
    _pip_install(proj_path)

    #link base
    _link_plop_libs(proj_path)
    _link_backend_cfg(proj_path, project_name)

    #add watcher
    _put_plop_watcher(proj_path)
    cprint("Done.\n")
    return proj_path


def new_android_project(project_name, www_folder):
    cprint("Working on Android project..")
    export_cmd = ":".join(["export PATH=${PATH}:"] + ANDROID_SDK_PATH_LIS)
    proj_path = os.path.join(_proj_workspace(project_name), "%s-android" % (project_name))
    commands = [
        export_cmd,
        "cd %s" % (ANDROID_PHONEGAP_BIN_PATH),
        "./create %s %s %s" % (
            proj_path, "com.unifide.%s" % (project_name), project_name),
        "cd %s" % (RESOURCES_PATH),
        "cp %s %s" % ("gitignore_for_mobile", os.path.join(proj_path, ".gitignore")),
    ]
    str_of_cmds = " && ".join(commands)
    os.system(str_of_cmds)

    #replace www
    cprint(".. Replacing www")
    www_folder_path = os.path.join(proj_path, "assets", "www")
    cmd_lis = [
        "rm -rf %s" % (www_folder_path),
        "cd %s" % (proj_path),
        "ln -s %s" % (www_folder),
    ]
    _run_cmd_lis(cmd_lis)

    #put watcher
    cprint(".. Adding Watcher")
    path_to_watch = os.path.join(_proj_workspace(project_name), "%s-www" % (project_name))
    _put_generic_watcher(proj_path, path_to_watch)

    cprint("Done.\n")
    return proj_path


def new_ios_project(project_name, www_folder):
    cprint("Working on iOS project..")
    proj_path = os.path.join(_proj_workspace(project_name), "%s-ios" % (project_name))
    commands = [
        "cd %s" % (IOS_PHONEGAP_BIN_PATH),
        "./create %s %s %s" % (
            proj_path, "com.unifide.%s" % (project_name), project_name)
    ]
    str_of_cmds = " && ".join(commands)
    os.system(str_of_cmds)

    #replace www
    cprint(".. Replacing www")
    www_folder_path = os.path.join(proj_path, "www")
    cmd_lis = [
        "rm -rf %s" % (www_folder_path),
        "cd %s" % (proj_path),
        "ln -s %s" % (www_folder),
        "cd %s" % (RESOURCES_PATH),
        "cp %s %s" % ("gitignore_for_mobile", os.path.join(proj_path, ".gitignore")),
    ]
    _run_cmd_lis(cmd_lis)

    #put watcher
    cprint(".. Adding Watcher")
    path_to_watch = os.path.join(_proj_workspace(project_name), "%s-www" % (project_name))
    _put_generic_watcher(proj_path, path_to_watch)
    cprint("Done.\n")
    return proj_path


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


def _cfg_proj_path(project_name):
    cfg_project_path = os.path.join(_proj_workspace(project_name), "%s-cfg" % (project_name))
    return cfg_project_path


def new_cfg_project(project_name):
    """
    Recursively copies the cfg project from resources to the project workspace
    """
    cprint("Working on CFG project..")
    cfg_project_path = _cfg_proj_path(project_name)
    cmd_lis = [
        "cd %s" % (RESOURCES_PATH),
        "cp -R %s %s" % ("cfg_proj", cfg_project_path),
    ]
    _run_cmd_lis(cmd_lis)
    cprint("Done.\n")
    return cfg_project_path


def _setup_backend_cfg(project_name):
    """
    Localise the config files for backend by generating some localised fields for it
    """
    lines = []

    #secret key -> SECRET_KEY = "b4ef3a73-5d52-11e2-9b58-14109feb3038"
    secret_key = _generate_uuid()
    lines += ["SECRET_KEY = '%s'" % (secret_key)]

    #mongo uri -> MONGO_URI = 'mongodb://localhost/unifide'
    lines += ["MONGO_URI = 'mongodb://localhost/%s'" % (project_name)]

    #mongodb -> MONGO_DB = "dada"
    lines += ["MONGO_DB = '%s'" % (project_name)]

    cfg_project_path = _cfg_proj_path(project_name)
    backend_cfg_file = os.path.join(cfg_project_path, "cfg.py")
    f = open(backend_cfg_file, "a")
    for l in lines:
        f.write("%s\n" % (l))
    f.close()


def _generate_uuid():
    return str(uuid.uuid1())


def _link_backend_cfg(backend_path, project_name):
    cfg_project_path = _cfg_proj_path(project_name)
    for cfg in BACKEND_CFG:
        cmd_lis = [
            "cd %s" % (backend_path),
            "rm -f %s" % (cfg),
            "ln -s %s" % (os.path.join(cfg_project_path, cfg)),
        ]
        _run_cmd_lis(cmd_lis)
    _setup_backend_cfg(project_name)


def _backend_path(project_name):
    return os.path.join(_proj_workspace(project_name), "unifide-backend")


def put_backend(project_name):
    """
    Clones a brand new unifide backend project
    """
    project_path = _backend_path(project_name)
    src_path = os.path.join(_proj_workspace(project_name), "unifide-backend", "src")

    cprint("Cloning backend project..")
    #clone git repository
    cmd_lis = [
        "cd %s" % (_proj_workspace(project_name)),
        "git clone git@bitbucket.org:kianwei/unifide-backend.git",
    ]
    _run_cmd_lis(cmd_lis)

    #link cfg
    _link_backend_cfg(src_path, project_name)

    #create virtualenv
    cprint(".. Creating virtualenv")
    _put_venv(project_path)

    #pip install requirements
    cprint(".. (pip) Installing requirements")
    _pip_install(project_path)

    cprint(".. Linking plop libraries")
    _link_plop_libs(src_path)

    new_folder(os.path.join(project_path, "resources"))

    cprint("Done.\n")
    return project_path


def _platform_path(project_name):
    return os.path.join(_proj_workspace(project_name), "unifide-platform")


def put_platform(project_name):
    cprint("Cloning platform project..")
    #clone git repository
    cmd_lis = [
        "cd %s" % (_proj_workspace(project_name)),
        "git clone git@bitbucket.org:kianwei/unifide-platform.git",
    ]
    _run_cmd_lis(cmd_lis)

    #link cfg
    cprint(".. Linking cfg")
    platform_path = _platform_path(project_name)
    platform_cfg_folder_path = os.path.join(platform_path, "lib")
    cfg_project_path = _cfg_proj_path(project_name)
    cmd_lis = [
        "cd %s" % (platform_cfg_folder_path),
        "rm -f %s" % (os.path.join(platform_cfg_folder_path, "cfg.js")),
        "ln -s %s" % (os.path.join(cfg_project_path, "cfg.js")),
    ]
    _run_cmd_lis(cmd_lis)

    #setup RunMeteor file
    cprint(".. Setting up RunMeteor")
    str = "PORT=3000 MONGO_URL=mongodb://localhost:27017/%s ROOT_URL=. meteor run" % (project_name)
    run_meteor_file_path = os.path.join(platform_path, "RunMeteor")
    run_meteor_file = open(run_meteor_file_path, "w")
    run_meteor_file.write(str)
    run_meteor_file.close()
    cmd_lis = [
        "cd %s" % (platform_path),
        "chmod +x %s" % (run_meteor_file_path),
    ]
    _run_cmd_lis(cmd_lis)

    cprint("Done.\n")
    return platform_path


def _proj_workspace(project_name):
    p = os.path.join(WORKSPACE_DIR, project_name)
    if not os.path.exists(p):
        cprint(".. Creating project workspace at %s" % (p))
        new_folder(p)
        cprint(".. Done creating workspace.")
    return p


def put_sync_file(project_name, common_mobile_folder, ios_path, android_path):
    sync_file_path = os.path.join(RESOURCES_PATH, "SYNC.py")
    f = open(sync_file_path, 'r')
    sync_file_content = f.read()
    f.close()
    ios_www_path = os.path.join(ios_path, "www")
    android_www_path = os.path.join(android_path, "assets", "www")

    sync_file_content = sync_file_content % {
        "android_www_path": android_www_path,
        "ios_www_path": ios_www_path,
        "www_path": common_mobile_folder,
    }

    cprint("Writing SYNC file..")
    new_sync_file_path = os.path.join(_proj_workspace(project_name), "SYNC.py")
    new_f = open(new_sync_file_path, "w")
    new_f.write(sync_file_content)
    new_f.close()
    cprint("Done.")
    return new_sync_file_path


def _get_avail_port():
    used_ports = _get("meteor_used_ports")
    if used_ports is None: used_ports = []

    avail_ports = filter(lambda x: x not in used_ports, METEOR_PORT_RANGE)
    chosen_port = choice(avail_ports)
    used_ports += [chosen_port]
    _set("meteor_used_ports", used_ports)

    return chosen_port


def _release_port(port_no):
    used_ports = _get("meteor_used_ports")
    used_ports = filter(lambda x: x != port_no, used_ports)
    _set("meteor_used_ports", used_ports)


def _get(key):
    f = open(DICT_FILE, "w+")
    stuff = f.read()
    try:
        d = json.loads(stuff)
    except:
        d = {}
    f.close()
    return d[key] if key in d else None


def _set(key, value):
    f = open(DICT_FILE, "w+")
    stuff = f.read()
    try:
        d = json.loads(stuff)
    except:
        d = {}
    f.close()

    d[key] = value
    f = open(DICT_FILE, "w+")
    f.write(json.dumps(d))
    f.close()


#-- main --#

if __name__ == '__main__':
    init()
    manager.main()