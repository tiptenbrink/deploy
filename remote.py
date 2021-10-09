from fabric import Connection
from pathlib import Path
import sys
import subprocess


def pull_run_remote_trans():
    with Connection(
            host="sd.tipten.nl", user="transnode", port=21678,
            connect_kwargs={
                "key_filename": "./keys/ssh.key",
            },
    ) as c:
        dirpath = Path("deployments/deployment_sd")

        for path in dirpath.rglob("*"):
            # because path is object not string
            path_str = str(path)
            print(path_str)
            c.put(path_str, remote="deployment")
        c.run("./deployment/deploy.sh")


def svn_checkout(github_svn_link, target):
    bash_command = ["svn", "checkout", github_svn_link, target]
    print("Running command: " + " ".join(bash_command))
    try:
        command = subprocess.run(bash_command, check=True, text=True, stdout=subprocess.PIPE, cwd='.')
        print(command.stdout)
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)


def pull_run_remote(host, user, port, key_path, source_dir, target_dir):
    with Connection(
            host=host, user=user, port=port,
            connect_kwargs={"key_filename": key_path},
    ) as c:
        # allow for slash at end of string
        target_dir.rstrip('/')
        dirpath = Path(source_dir)
        c.run("mkdir -p {}".format(target_dir))
        for path in dirpath.rglob("*"):
            # because path is object not string
            path_str = str(path)
            if ".svn" not in path_str:
                print(path_str)
                c.put(path_str, remote=target_dir)
        # SVN does not remember files that are executable in Git
        c.run("chmod +x " + target_dir + "/deploy.sh")
        c.run(target_dir + "/deploy.sh")
