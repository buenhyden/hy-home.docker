# Rules for every Compose leaf under infra/ (POL-0095). Each deny names the
# service and the rule; the allowlists are the only sanctioned exceptions.
package compose

import rego.v1

# cAdvisor reads host cgroups and devices; no other service may be privileged.
privileged_allowed := {"cadvisor"}

secret_key(key) if regex.match(`(?i)(PASSWORD|PASSWD|SECRET|TOKEN|API_KEY|PRIVATE_KEY)`, key)

# A value that cannot be a credential: empty, interpolated, a secret path, a
# flag or a URL.
reference(value) if value == ""

reference(value) if startswith(value, "$")

reference(value) if contains(value, "/run/secrets/")

reference(value) if lower(value) in {"true", "false", "yes", "no", "0", "1"}

reference(value) if contains(value, "://")

# Keys that name where a secret comes from rather than holding it.
indirect(key) if endswith(key, "_FILE")

indirect(key) if endswith(key, "_CMD")

env_pairs(env) := {[k, sprintf("%v", [v])] | some k, v in env} if is_object(env)

env_pairs(env) := {[k, v] |
	some item in env
	[k, v] := split_env(item)
} if is_array(env)

split_env(item) := [parts[0], concat("=", array.slice(parts, 1, count(parts)))] if {
	parts := split(item, "=")
	count(parts) > 1
}

deny contains msg if {
	some name, svc in input.services
	svc.privileged == true
	not name in privileged_allowed
	msg := sprintf("service %s: privileged is not allowed", [name])
}

deny contains msg if {
	some name, svc in input.services
	not svc.profiles
	msg := sprintf("service %s: declares no profile (POL-0078)", [name])
}

deny contains msg if {
	some name, svc in input.services
	image := svc.image
	not startswith(image, "$")
	endswith(image, ":latest")
	msg := sprintf("service %s: image %s uses latest", [name, image])
}

deny contains msg if {
	some name, svc in input.services
	image := svc.image
	not startswith(image, "$")
	not contains(image, ":")
	not contains(image, "@")
	msg := sprintf("service %s: image %s has no tag", [name, image])
}

deny contains msg if {
	some name, svc in input.services
	some [key, value] in env_pairs(object.get(svc, "environment", {}))
	secret_key(key)
	not indirect(key)
	not reference(value)
	msg := sprintf("service %s: %s carries a literal value; use a Docker secret", [name, key])
}

# A host publication must name the address it binds (SPEC-0188, a deny once
# the source passed): loopback for a
# host-local port, the host LAN address for one the k3d cluster reaches. The
# raw string is read before interpolation, so `${VAR:-address}` counts as an
# address when its default is not a wildcard.
wildcard_addresses := {"", "0.0.0.0", "::", "[::]"}

wildcard_host(host) if host in wildcard_addresses

wildcard_host(host) if {
	startswith(host, "${")
	not contains(host, ":-")
}

wildcard_host(host) if {
	startswith(host, "${")
	trim_suffix(split(host, ":-")[1], "}") in wildcard_addresses
}

# `${...}` and `[...]` may hold colons, so they are masked before counting the
# `host:container` or `address:host:container` fields.
wide_port(port) if {
	is_string(port)
	fields := split(regex.replace(regex.replace(port, `\$\{[^}]*\}`, "V"), `\[[^\]]*\]`, "B"), ":")
	count(fields) == 2
}

wide_port(port) if {
	is_string(port)
	fields := split(regex.replace(regex.replace(port, `\$\{[^}]*\}`, "V"), `\[[^\]]*\]`, "B"), ":")
	count(fields) > 2
	host := regex.find_n(`^(\$\{[^}]*\}|\[[^\]]*\]|[^:]*)`, port, 1)[0]
	wildcard_host(host)
}

wide_port(port) if {
	is_object(port)
	port.published
	wildcard_host(object.get(port, "host_ip", ""))
}

port_label(port) := port if is_string(port)

port_label(port) := sprintf("%v", [port]) if not is_string(port)

deny contains msg if {
	some name, svc in input.services
	some port in object.get(svc, "ports", [])
	wide_port(port)
	msg := sprintf("service %s: port %s is published on all interfaces", [name, port_label(port)])
}
