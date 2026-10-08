package compose

import rego.v1

base := {"profiles": ["x"], "image": "busybox:1.37"}

svc(extra) := {"services": {"s": object.union(base, extra)}}

test_clean_service_passes if {
	count(deny) == 0 with input as svc({})
}

test_privileged_is_denied if {
	deny["service s: privileged is not allowed"] with input as svc({"privileged": true})
}

test_cadvisor_may_be_privileged if {
	count(deny) == 0 with input as {"services": {"cadvisor": object.union(base, {"privileged": true})}}
}

test_missing_profile_is_denied if {
	deny["service s: declares no profile (POL-0078)"] with input as {"services": {"s": {"image": "busybox:1.37"}}}
}

test_latest_and_untagged_images_are_denied if {
	deny["service s: image busybox:latest uses latest"] with input as svc({"image": "busybox:latest"})
	deny["service s: image busybox has no tag"] with input as svc({"image": "busybox"})
}

test_literal_secret_is_denied_in_both_env_forms if {
	deny["service s: DB_PASSWORD carries a literal value; use a Docker secret"] with input as svc({"environment": {"DB_PASSWORD": "hunter2hunter2"}})
	deny["service s: API_TOKEN carries a literal value; use a Docker secret"] with input as svc({"environment": ["API_TOKEN=abc=def"]})
}

test_secret_references_pass if {
	count(deny) == 0 with input as svc({"environment": {
		"DB_PASSWORD": "${DB_PASSWORD}",
		"DB_PASSWORD_FILE": "/run/secrets/db",
		"JWT_SECRET_CMD": "cat /run/secrets/jwt",
		"AUTH_TOKEN_URL": "https://auth.example/token",
		"ENABLE_PASSWORD_AUTH": "false",
	}})
}

test_credentials_inside_urls_are_denied_under_any_key if {
	deny["service s: DATABASE_URL carries a credential in a URL; use a Docker secret"] with input as svc({"environment": {"DATABASE_URL": "postgres://app:hunter2@db:5432/app"}})
	deny["service s: BROKER_URL carries a credential in a URL; use a Docker secret"] with input as svc({"environment": ["BROKER_URL=redis://:s3cret@valkey:6379/0"]})
	deny["service s: HOOK carries a credential in a URL; use a Docker secret"] with input as svc({"environment": {"HOOK": "https://hooks.example/notify?token=abc123"}})
	deny["service s: FEED carries a credential in a URL; use a Docker secret"] with input as svc({"environment": {"FEED": "https://api.example/v1?q=x&API_KEY=k9"}})
	deny["service s: AUTH_TOKEN_URL carries a credential in a URL; use a Docker secret"] with input as svc({"environment": {"AUTH_TOKEN_URL": "https://u:p@auth.example/token"}})
}

test_urls_without_their_own_credential_pass if {
	count(deny) == 0 with input as svc({"environment": {
		"DATABASE_URL": "postgres://app:${DB_PASSWORD}@db:5432/app",
		"BROKER_URL": "redis://:${VALKEY_PASSWORD}@valkey:6379/0",
		"ISSUER_URL": "https://keycloak.${DEFAULT_URL}/realms/r",
		"USER_ONLY_URL": "postgres://app@db:5432/app",
		"HOOK": "https://hooks.example/notify?token=${HOOK_TOKEN}",
		"SEARCH_URL": "https://api.example/v1?q=keyword&page=2",
		"SECRET_PATH": "/run/secrets/db",
		"DSN_FILE": "/run/secrets/dsn",
	}})
}

test_wide_port_is_denied_and_loopback_is_not if {
	count(deny) == 1 with input as svc({"ports": ["8080:80"]})
	count(deny) == 0 with input as svc({"ports": ["127.0.0.1:8080:80", "80"]})
}

test_host_port_variables_without_an_address_are_denied if {
	count(deny) == 1 with input as svc({"ports": ["${X_HOST_PORT:-8080}:${X_PORT:-80}"]})
	count(deny) == 1 with input as svc({"ports": ["${X_HOST_PORT:-8443}:8443/tcp"]})
}

test_a_named_host_address_is_scoped if {
	count(deny) == 0 with input as svc({"ports": [
		"192.168.0.13:80:80",
		"${HOST_LAN_BIND_IP:-192.168.0.13}:${X_HOST_PORT:-443}:${X_PORT:-443}",
		"127.0.0.1:${X_HOST_PORT:-8080}:80",
		"[::1]:8080:80",
	]})
}

test_wildcard_and_unset_addresses_are_denied if {
	count(deny) == 1 with input as svc({"ports": ["0.0.0.0:8080:80"]})
	count(deny) == 1 with input as svc({"ports": ["[::]:8080:80"]})
	count(deny) == 1 with input as svc({"ports": ["${BIND_IP}:8080:80"]})
	count(deny) == 1 with input as svc({"ports": ["${BIND_IP:-0.0.0.0}:8080:80"]})
}

test_long_syntax_needs_a_host_ip if {
	count(deny) == 1 with input as svc({"ports": [{"target": 80, "published": 8080}]})
	count(deny) == 1 with input as svc({"ports": [{"target": 80, "published": 8080, "host_ip": "0.0.0.0"}]})
	count(deny) == 0 with input as svc({"ports": [{"target": 80, "published": 8080, "host_ip": "127.0.0.1"}]})
	count(deny) == 0 with input as svc({"ports": [{"target": 80}]})
}
