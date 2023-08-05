import os
import socket
import requests as req
from .env import Env, expandvars
from .auth.keycloak import Keycloak


def load_configs(app_role):
    env = Env()

    app_role = env("CONFIGS_ROLE_NAME", default=app_role)
    configs_protocol = env("CONFIGS_PROTOCOL", default="https")
    configs_host = env("CONFIGS_HOST", default="configs.avd.al")
    configs_client = env("CONFIGS_CLIENT_ID", default="")
    configs_secret = env("CONFIGS_CLIENT_SECRET", default="")

    iam_host = env("IAM_HOST", default="iam.avd.al")
    iam_realm = env("IAM_REALM", default="groot")

    if not configs_client:
        print("CONFIGS_CLIENT_ID not set. Skipping remote configs")
        return

    keycloak = Keycloak(iam_host, iam_realm, configs_client, configs_secret)
    token, error = keycloak.access_token()

    if not token:
        print("failed to get a token due to", error)
        return

    def load_role(role):
        print(f"loading role: {role}")
        role_uri = f"{configs_protocol}://{configs_host}/api/v1/roles/{role}/configs"

        res = req.get(role_uri, headers={
            "Authorization": f"Bearer {token}",
        })

        if not res.ok:
            print(f"configs service returned an error: [{res.content}]")
            return

        for k, v in res.json().items():
            if k not in os.environ:
                os.environ[k] = expandvars(str(v))

        print(f"loaded role: {role}")

    load_role(app_role)
    load_role("common")
    load_role(socket.gethostname().lower())
