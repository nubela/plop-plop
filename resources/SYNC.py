import os


def _run_cmd_lis(cmd_lis):
    full_cmd = " && ".join(cmd_lis)
    os.system(full_cmd)

def sync():
    cmds_lis = [
        "rm -rf %(android_www_path)s",
        "rm -rf %(ios_www_path)s",
        "cp -R %(www_path)s %(android_www_path)s",
        "cp -R %(www_path)s %(ios_www_path)s",
    ]
    _run_cmd_lis(cmds_lis)

if __name__ == "__main__":
    sync()