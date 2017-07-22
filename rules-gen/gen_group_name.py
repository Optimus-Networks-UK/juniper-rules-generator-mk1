
### Generate source and destination group names
from random import choice
from string import ascii_uppercase, ascii_lowercase


def src_group(dest_host, source_host):

	### Check if dest host contains "any"

	## Check for presence of "Any", if so then do the source group alternate generation
	if dest_host == "any":
		trimmed = src_group_alternate(source_host)
		return trimmed
	elif dest_host == "Any":
		source_group_name = "any"
		## now exit
		trimmed = src_group_alternate(source_host)
		return trimmed
		
	elif dest_host == "ANY":
		source_group_name = "any"
		## now exit
		trimmed = src_group_alternate(source_host)
		return trimmed
			

	### standard name based on destination

	trimmed = finish_trim(dest_host)
	trimmed = trimmed + "_access"
	trimmed = trim_mess(trimmed)


	return trimmed

def src_group_alternate(source_host):

	trimmed = finish_trim(source_host)
	trimmed = trimmed + "_access_src"
	trimmed = trim_mess(trimmed)

	return trimmed

def dst_group_alternate(source_host):

	trimmed = finish_trim(source_host)
	trimmed = trimmed + "_access_dst"
	trimmed = trim_mess(trimmed)

	return trimmed

def app_group_alternate(source_host):

	trimmed = finish_trim(source_host)
	trimmed = trimmed + "_apps"
	trimmed = trim_mess(trimmed)

	return trimmed

def policy_name_alternate(source_host):

	trimmed = finish_trim(source_host)
	trimmed = trimmed + "_policy"
	trimmed = trim_mess(trimmed)

	return trimmed


def dst_group(dest_host):


	
	trimmed = finish_trim(dest_host)
	trimmed = trimmed + "_servers"
	trimmed = trim_mess(trimmed)


	return trimmed


def app_set(dest_host, source_host):

### Check for presence of "Any", if so then do the source group alternate generation

	#trimmed = name_logic(dest_host, source_host)

	if dest_host == "any":
		trimmed = app_group_alternate(source_host)
		return trimmed + "_" + gen_random_string()
	elif dest_host == "Any":
		source_group_name = "any"
		## now exit
		trimmed = app_group_alternate(source_host)
		return trimmed + "_" + gen_random_string()
		
	elif dest_host == "ANY":
		source_group_name = "any"
		## now exit
		trimmed = app_group_alternate(source_host)
		return trimmed + "_" + gen_random_string()

	trimmed = finish_trim(dest_host)

	trimmed = trimmed + "_apps"
	trimmed = trim_mess(trimmed)

	return trimmed

def policy_name(dest_host, source_host):

	## Check for presence of "Any", if so then do the source group alternate generation
	if dest_host == "any":
		trimmed = policy_name_alternate(source_host)
		return trimmed + "_" + gen_random_string()
	elif dest_host == "Any":
		source_group_name = "any"
		## now exit
		trimmed = policy_name_alternate(source_host)
		return trimmed + "_" + gen_random_string()
		
	elif dest_host == "ANY":
		source_group_name = "any"
		## now exit
		trimmed = policy_name_alternate(source_host)
		return trimmed + "_" + gen_random_string()

	trimmed = finish_trim(dest_host)

	trimmed = trimmed + "_policy"
	trimmed = trim_mess(trimmed)


	return trimmed


def finish_trim(trimmed):

	### Trim size to 8 char

	trimmed = trimmed[:8]

	### remove spaces

	trimmed = trimmed.replace(" ", "")

	### remove messy gubbins

	trimmed = trimmed.replace("-_", "_")
	trimmed = trimmed.replace("_-", "_")

	return trimmed

def trim_mess(trimmed):

	### Remove numeric digits from string

	trimmed = ''.join([i for i in trimmed if not i.isdigit()])

		### remove messy gubbins

	trimmed = trimmed.replace("-_", "_")
	trimmed = trimmed.replace("_-", "_")



	return trimmed


def gen_random_string():
	random_string = (''.join(choice(ascii_lowercase) for i in range(3)))
	return random_string