# Rules for every Dockerfile under infra/ (POL-0095).
package dockerfile

import rego.v1

stage_names contains lower(name) if {
	some instruction in input[_]
	instruction.Cmd == "from"
	count(instruction.Value) == 3
	name := instruction.Value[2]
}

deny contains msg if {
	some instruction in input[_]
	instruction.Cmd == "from"
	image := instruction.Value[0]
	image != "scratch"
	not lower(image) in stage_names
	not startswith(image, "$")
	not contains(image, ":")
	not contains(image, "@")
	msg := sprintf("FROM %s has no tag", [image])
}

deny contains msg if {
	some instruction in input[_]
	instruction.Cmd == "from"
	endswith(instruction.Value[0], ":latest")
	msg := sprintf("FROM %s uses latest", [instruction.Value[0]])
}

deny contains msg if {
	some instruction in input[_]
	instruction.Cmd == "add"
	some source in array.slice(instruction.Value, 0, count(instruction.Value) - 1)
	regex.match(`^https?://`, source)
	not checksum_flag(instruction)
	msg := sprintf("ADD %s has no --checksum", [source])
}

checksum_flag(instruction) if {
	some flag in instruction.Flags
	startswith(flag, "--checksum=")
}
