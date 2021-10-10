# tideploy: remote deployment simplified

`tideploy` is a simple tool to simplify remote deployment using SSH. While it has been specifically designed for deploying Docker containers, it can be easily configured for other deployment pipelines.

`tideploy` is a Python CLI script that depends on [Fabric](https://www.fabfile.org/), a library for executing shell commands remotely over SSH.

### What `tideploy` can do

`tideploy` performs the following steps:

1. Connects to a remote host via SSH
2. Transfers files to a remote host
3. Runs a script contained in the files called `deploy.sh`

These are all very simple, but due to the versatile nature of steps 2 and 3 you can perform nearly any task. An example deployment can be found in `/example_deployments`. There, the deploy script as well as a docker-compose file and .env file are transferred, after which Docker Compose is executed from the script.

### Installation and basic usage

```shell
pip install tideploy
```

`tideploy` is a CLI script that requires a number of arguments to function. To easily employ `tideploy` in a virtualenv, [Poetry](https://python-poetry.org) is recommended. Once installed, you can view the `tideploy` help by running:

```shell
poetry run tideploy --help
```

`tideploy` does not support password-authenticated SSH connections for security reasons. Use an SSH keyfile instead. If the keyfile is protected by a passphrase, you will be prompted to enter it.

By default, `tideploy` will look for a `/deployment` folder in the working directory and transfer its contents to a `/deployment` folder in the remote server's home directory. Subsequently, the `deploy.sh` script (which is assumed to be part of the files that are transferred) is executed.

The 'hostname' and 'user' arguments are required.

```shell
tideploy -n bar.com -u foo
```
will connect to user foo at host bar.com, with the SSH key located at `./keys/ssh.key`.

### Usage guide

```
usage: tideploy [-h] [-y YAML] -n HOST -u USER [-p PORT] [-k KEY] [-svn SVN_URL] [-s SOURCE] 
[-t TARGET]

Deploy app remotely using Python Fabric.

Examples:
tideploy -n bar.com -u foo -s bar_deployment -t bar_target
tideploy --yaml deployments/foo_deployment.yml
tideploy -n bar.com -u foo -svn https://github.com/foo/bar/trunk/baz

optional arguments:
  -h, --help            show this help message and exit
  -y YAML, --yaml YAML  YAML configuration file location. Optional and can be used only 
  instead of CLI arguments. (default: ./deployments/deployment.yml)

arguments:
  -n HOST, --host HOST  Remote server hostname
  -u USER, --user USER  Remote server user
  -p PORT, --port PORT  Remote SSH port (default: 22)
  -k KEY, --key KEY     SSH key location for remote access (default: ./keys/ssh.key)
  -svn SVN_URL, --svn-url SVN_URL
                        If files are not stored locally, you can use an SVN (Subversion) 
                        URL to check out a specific directory that will be transferred. 
                        Specify the local download location using the --source argument. 
                        SVN must be installed for this to work.
  -s SOURCE, --source SOURCE
                        Directory (relative to the script or absolute path) that contains 
                        the deployment files (.env, docker-compose.yml and tideploy.sh). 
                        'tideploy.sh' is required! Every file in the directory (including 
                        in subdirectories) will be
                        transferred. Note that this is the directory download destination 
                        for SVN checkout if an SVN link was provided for '--svn-url'. 
                        (default: ./deployments/deployment)
  -t TARGET, --target TARGET
                        Target directory in the remote server where all files from the 
                        subdirectory will be loaded into. This must be an absolute path or 
                        relative to the target server home directory. (default: ./deployment)
```

#### YAML configuration file

If you do not want to specify all arguments from the command line, you can supply it with a YAML file instead by denoting the file name after the `--yaml` flag. All other flags are then ignored and only the YAML file is read. See the `example_deployments/deploynent.yml` file for the syntax.

#### SVN link

If you want to be sure you are sending the most recent deployment files or you do not want to download them first, you can use a SVN (Subversion) link to check them out locally before sending them. Use the `--svn-url` option. You can check out a single directory from all GitHub repositories this way ([GitHub Docs](https://docs.github.com/en/github/importing-your-projects-to-github/working-with-subversion-on-github/support-for-subversion-clients)). 

For example, if you want to transfer the contents of the `/baz` directory from the HEAD branch of the `foo/bar` GitHub repository, you can use `https://github.com/foo/bar/trunk/baz`. If you want it from some other branch, replace `trunk` with `branches/<branch>`.

### Supported platforms

`tideploy` depends on Fabric, which itself depends on [Paramiko](https://www.paramiko.org/installing.html), which relies on a number of non-pure Python packages (bcrypt, cryptography and PyNaCl, the latter of which relies on cffi). This requirement means only platforms for which these packages have binary releases are supported, but that should include almost all.

`tideploy` is primarily targeted at Linux → Linux deployment pipelines. Windows and macOS are untested. 