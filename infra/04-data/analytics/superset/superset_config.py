"""hy-home Superset configuration (mounted at /app/pythonpath).

Secrets come from Docker secret files, never the environment or a URI:
the signing key, the metadata database password and the Keycloak client
secret. Keycloak is reached through Traefik (`keycloak.${DEFAULT_URL}` is a
Traefik alias on edge_net), so the local root CA is added to the CA bundle.
"""

import os
import pathlib

import certifi
from flask_appbuilder.security.manager import AUTH_OAUTH
from sqlalchemy.engine import URL

SECRETS = pathlib.Path("/run/secrets")


def _file(path: pathlib.Path) -> str:
    if not path.is_file():
        raise RuntimeError(f"superset: {path} is missing or not a file")
    return path.read_text(encoding="utf-8")


def _secret(name: str) -> str:
    value = _file(SECRETS / name).strip()
    if not value or "\n" in value:
        raise RuntimeError(f"superset: secret {name} must be one non-empty line")
    return value


def _env(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise RuntimeError(f"superset: {name} is not set")
    return value


SECRET_KEY = _secret("superset_secret_key")

# Built in memory: the migration engine (Alembic) reads only the URI, so the
# password has to be in it; URL.create escapes it, and nothing puts it in the
# environment or argv.
SQLALCHEMY_DATABASE_URI = URL.create(
    "postgresql+psycopg2",
    username=_env("SUPERSET_DB_USER"),
    password=_secret("superset_db_password"),
    host=_env("SUPERSET_DB_HOST"),
    port=int(_env("SUPERSET_DB_PORT")),
    database=_env("SUPERSET_DB_NAME"),
).render_as_string(hide_password=False)
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

# Public CAs plus the local root CA, for the Keycloak discovery and token calls.
# Every CLI run imports this file too, so replace the bundle atomically.
_bundle = pathlib.Path("/tmp/superset-ca-bundle.pem")
_staged = _bundle.with_name(f"{_bundle.name}.{os.getpid()}")
_staged.write_text(
    _file(pathlib.Path(certifi.where()))
    + "\n"
    + _file(pathlib.Path("/etc/ssl/certs/hy-home-rootCA.pem")),
    encoding="utf-8",
)
os.replace(_staged, _bundle)
os.environ["REQUESTS_CA_BUNDLE"] = os.environ["SSL_CERT_FILE"] = str(_bundle)

_realm = "https://keycloak.{}/realms/hy-home.realm".format(_env("DEFAULT_URL"))
AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [
    {
        "name": "keycloak",
        "icon": "fa-key",
        "token_key": "access_token",
        "remote_app": {
            "client_id": _env("SUPERSET_OIDC_CLIENT_ID"),
            "client_secret": _secret("superset_oidc_client_secret"),
            "server_metadata_url": f"{_realm}/.well-known/openid-configuration",
            "api_base_url": f"{_realm}/protocol/",
            "client_kwargs": {"scope": "openid email profile", "code_challenge_method": "S256"},
        },
    }
]
# First login creates a Gamma user (no data access); an Admin grants roles.
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"

# Behind Traefik: trust its X-Forwarded-* so callbacks use https and the host.
ENABLE_PROXY_FIX = True
PREFERRED_URL_SCHEME = "https"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"
