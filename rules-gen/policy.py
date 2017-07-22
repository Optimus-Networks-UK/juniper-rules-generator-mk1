

def gen_policy(rule_id, from_zone, to_zone, source_group_name, dest_group_name, application_set_name, policy_name):


	### First check if any of the zones are "any" and if so, generate a global policy.

	if from_zone == "any":
		gen_policy_global(rule_id, from_zone, to_zone, source_group_name, dest_group_name, application_set_name, policy_name)
		return

	elif to_zone == "any":
		gen_policy_global(rule_id, from_zone, to_zone, source_group_name, dest_group_name, application_set_name, policy_name)
		return

	config1 = "set security policies from-zone " 
	config1_2 = " to-zone "
	### from-zone
	### to-zone

	config2 = " policy "
	### policy-name
	config3 = " "

	policy_line = config1  + from_zone + config1_2 + to_zone + config2 + policy_name

	policy_line_source = policy_line + " match source-address " + source_group_name
	policy_line_dest = policy_line + " match destination-address " + dest_group_name
	policy_line_app = policy_line + " match application " + application_set_name
	policy_line_action = policy_line + " then permit"
	### Gen Policy

	### Print policy on screen

	print policy_line_source
	print policy_line_dest
	print policy_line_app
	print policy_line_action

def gen_policy_global(rule_id, from_zone, to_zone, source_group_name, dest_group_name, application_set_name, policy_name):

	config1 = "set security policies global policy " 
	config1_1 = " from-zone "
	config1_2 = " to-zone "
	match = " match "
	### from-zone
	### to-zone

	config2 = " policy "
	### policy-name
	config3 = " "

	policy_line = config1  + policy_name + match + config1_1 + from_zone + config1_2 + to_zone

	policy_line_source = policy_line + " source-address " + source_group_name
	policy_line_dest = policy_line + " destination-address " + dest_group_name
	policy_line_app = policy_line + " application " + application_set_name
	policy_line_action = config1  + policy_name + " then permit"
	### Gen Policy

	### Print policy on screen

	print policy_line_source
	print policy_line_dest
	print policy_line_app
	print policy_line_action

	





