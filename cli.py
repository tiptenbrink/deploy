from remote import pull_run_remote, svn_checkout
import argparse
import yaml


def cli(argv):
    yaml_default = "./deployments/deployment.yml"
    yaml_help = "YAML configuration file location. Optional and can be used only instead of CLI arguments. " \
                "(default: {})".format(yaml_default)

    host_nm = 'host'
    user_nm = 'user'
    port_nm = 'port'
    key_nm = 'key'
    svn_nm = 'svn-url'
    source_nm = 'source'
    target_nm = 'target'

    # Optionally, a YAML configuration file can be supplied (by default it is assumed to be 'deployment.yml' in the
    # directory of the script file. If '-y' or '--yaml' is supplied, it will ignore all other arguments.
    if '-y' in argv or '--yaml' in argv:
        print("Parsing using YAML config... Leave out -y/--yaml to use CLI arguments.")
        parser = argparse.ArgumentParser()
        parser.add_argument('-y', '--yaml', required=True, nargs='?', const=yaml_default, help=yaml_help,
                            type=argparse.FileType('r'))
        args = parser.parse_args(argv)

        config = yaml.safe_load(args.yaml)

    # Otherwise, it will parse all arguments from the CLI. At least, 'host' and 'user' must be supplied.
    else:
        parser = argparse.ArgumentParser(description="Deploy app remotely.")

        parser.add_argument('-y', '--yaml', default=yaml_default, help=yaml_help)
        group = parser.add_argument_group("arguments")

        group.add_argument('-n', '--{}'.format(host_nm), required=True, help="Remote server hostname")

        group.add_argument('-u', '--{}'.format(user_nm), required=True, help="Remote server user")
        ssh_default = 22

        group.add_argument('-p', '--{}'.format(port_nm), default=ssh_default, type=int,
                           help="Remote SSH port (default: {})".format(ssh_default))
        key_default = "./keys/ssh.key"

        group.add_argument('-k', '--{}'.format(key_nm), default=key_default,
                           help="SSH key location for remote access (default: {})".format(key_default))

        group.add_argument('-svn', '--{}'.format(svn_nm), help="If files are not stored locally, you can use an SVN "
                                                               "(Subversion) URL to check out a specific directory "
                                                               "that will be transferred. Specify the local download "
                                                               "location using the --{} argument. SVN must be "
                                                               "installed for this to work.".format(source_nm))
        default_source = "./deployments/deployment"
        group.add_argument('-s', '--{}'.format(source_nm), default=default_source,
                           help="Directory (relative to the script or absolute path) that contains the deployment "
                                "files (.env, docker-compose.yml and deploy.sh). 'deploy.sh' is  required! Every file "
                                "in the directory (including in subdirectories) will be transferred. Note that this "
                                "is the directory download destination for SVN checkout if an SVN link was provided "
                                "for '--{svn}'. (default: {deflt})".format(svn=svn_nm, deflt=default_source))
        default_target = "./deployment"

        group.add_argument('-t', '--{}'.format(target_nm), default=default_target,
                           help="Target directory in the remote server where all files from the subdirectory will be "
                                "loaded into. This must be an absolute path or relative to the target server home "
                                "directory. (default: {})".format(default_target))

        config = vars(parser.parse_args(argv))

    if config[svn_nm] is not None:
        print("--{} detected, checking out using SVN...".format(svn_nm))
        svn_checkout(config[svn_nm], config[source_nm])

    print("{} {} {} {} {} {}".format(config[host_nm], config[user_nm], config[port_nm], config[key_nm],
                                     config[source_nm], config[target_nm]))

    # pull_run_remote(config[host_nm], config[user_nm], config[port_nm], config[key_nm], config[source_nm],
    #                 config[target_nm])
