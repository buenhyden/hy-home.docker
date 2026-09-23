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

test_wide_port_warns_and_loopback_does_not if {
	count(warn) == 1 with input as svc({"ports": ["8080:80"]})
	count(warn) == 0 with input as svc({"ports": ["127.0.0.1:8080:80", "80"]})
}
