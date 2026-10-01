package dockerfile

import rego.v1

df(instructions) := [instructions]

from(values) := {"Cmd": "from", "Flags": [], "Value": values}

test_pinned_base_passes if {
	count(deny) == 0 with input as df([from(["alpine:3.22"])])
}

test_untagged_and_latest_bases_are_denied if {
	deny["FROM alpine has no tag"] with input as df([from(["alpine"])])
	deny["FROM alpine:latest uses latest"] with input as df([from(["alpine:latest"])])
}

test_stage_reference_and_scratch_pass if {
	count(deny) == 0 with input as df([from(["golang:1.26", "AS", "builder"]), from(["builder"]), from(["scratch"])])
}

test_remote_add_needs_checksum if {
	deny["ADD https://example.org/a.jar has no --checksum"] with input as df([{"Cmd": "add", "Flags": [], "Value": ["https://example.org/a.jar", "/opt/"]}])
	count(deny) == 0 with input as df([{"Cmd": "add", "Flags": ["--checksum=sha256:00"], "Value": ["https://example.org/a.jar", "/opt/"]}])
}
