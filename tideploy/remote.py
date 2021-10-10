from fabric import Connection
import paramiko.ssh_exception
from pathlib import Path
import sys
import subprocess
from getpass import getpass


def svn_checkout(github_svn_link, target):
    bash_command = ["svn", "checkout", github_svn_link, target]
    print("Running command: " + " ".join(bash_command))
    try:
        command = subprocess.run(bash_command, check=True, text=True, stdout=subprocess.PIPE, cwd='.')
        print(command.stdout)
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)


def make_connection(host, user, port, key_path, source_dir, target_dir):
    try:
        print("Establishing SSH connection with SSH key from {}...".format(key_path))
        with Connection(
                host=host, user=user, port=port,
                connect_kwargs={"key_filename": key_path},
        ) as c:
            pull_run_remote(c, source_dir, target_dir)
    except FileNotFoundError as e:
        print(e)
        print("Your key file is missing or wrong path given to '--key' argument / YAML field.")
    except paramiko.ssh_exception.PasswordRequiredException:
        # Ask for passphrase to decrypt private key file
        passphrase = getpass("SSH key is encrypted. Enter passphrase:\n")
        attempts = 0
        # While loop for multiple password attempts
        while True:
            try:
                with Connection(
                        host=host, user=user, port=port,
                        connect_kwargs={"key_filename": key_path, "passphrase": passphrase},
                ) as c:
                    pull_run_remote(c, source_dir, target_dir)
                    break
            except paramiko.ssh_exception.SSHException as e:
                attempts += 1
                if str(e) == "Invalid key":
                    attempts_string = "{} attempt{} remaining.".format(3-attempts, "s" if attempts < 2 else "") if \
                        attempts != 0 else ""
                    print("Incorrect password, please try again. Program will exit after 3 incorrect attempts. " +
                          attempts_string)

                    passphrase = getpass("SSH key is encrypted. Enter passphrase:\n")
                else:
                    raise

            if attempts >= 2:
                print("Incorrect password. Exiting program...")
                break


def pull_run_remote(c, source_dir, target_dir):
    c.run('echo "Entered ${HOME} directory of remote host..."')
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

