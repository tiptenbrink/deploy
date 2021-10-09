```shell
ssh-copy-id -i ssh.key 
ssh -i ssh.key 
```

```shell
poetry run python __main__.py --host sd.tipten.nl --user transnode --port  --key './keys/ssh.key' --source deployments/deployment_sd --target deployment
```

```shell
poetry run python __main__.py --yaml deployments/deploy_auth.yml
```