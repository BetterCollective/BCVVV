#!/usr/bin/env python3

""" Fundamentals """

from __future__ import print_function, unicode_literals
from PyInquirer import prompt, Separator
from shutil import copyfile
import json
import os
import yaml
import sys 

print()
print("BCVVV: fork of VVV")
print("------------------")
print()
print("Local development environment and guideline for Wordpress at Better Collective")
print("- Always refer to the official VVV documentation, ./config/default-config.yml, and DevOps documentation.")
print()
print("Be aware that 'existing site' refer to a site that is already hosted on Plesk that you want to develop on, and 'new site' refer to a site that is NOT already Plesk, however, that you want to add.")
print()
print("This util is not meant as a configuration manager, but as a guideline and a place to get started.")
print()

# Create vvv yaml config if does not exist
config_sample = "./config/default-config.yml"
config = "./config/config.yml"

file_exists = os.path.isfile(config) 

if file_exists:
	print("{0} already exists and will be used in this util.".format(config))
	print()
	pass
else:
	copyfile(config_sample, config)
	print("{0} does not exist. {0} has been created from {1} and will be used in this util.".format(config, config_sample))
	print()

# yaml quote representer
def quoted_presenter(dumper, data):
	if type(data) == str:
		if ' ' in data:
			return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
		else:
			return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')
	else:
		return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')

#yaml.add_representer(str, quoted_presenter) only for strings with spaces due to the representer function
yaml.add_representer(str, quoted_presenter)

# yaml indentation fix 
class IndentDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)

# Read vvv yaml config
with open(config, 'r') as stream:
    try:
        documents = yaml.safe_load(stream);
    except yaml.YAMLError as exc:
        print(exc)

""" Functionality """

def bcvvv_setup_new_site():

	# Existing site message
	print()
	print("You have chosen to setup a new site.")
	print()

	# PyInquirer questions
	new_site_questions = [
		{
			'type': 'input',
			'name': 'new_site_domain',
			'message': 'What\'s the domain name',
		},
		{
			'type': 'input',
			'name': 'new_site_php_version',
			'message': 'What PHP version do you want (php56, php70, php71, php72, php73, php74)',
			#'validate': lambda val: val == 'Doe' or 'is your last name Doe?'
		},
		{
			'type': 'input',
			'name': 'new_site_title',
			'message': 'What\'s the Wordpress title'
			#'validate': PhoneNumberValidator
		},
		{
			'type': 'input',
			'name': 'new_site_desc',
			'message': 'What\'s the Wordpress description',
		},
		{
			'type': 'input',
			'name': 'new_site_wp_version',
			'message': 'What\'s the Wordpress version',
			#'validate': lambda val: val == 'Doe' or 'is your last name Doe?'
		}
	]

	new_site_answers = prompt(new_site_questions)

	# remove spaces from title
	new_site_title_no_spaces = "".join(new_site_answers['new_site_title'].split())

	new_site_obj = {
		new_site_title_no_spaces: {
			'skip_provisioning': False,
			'description': new_site_answers['new_site_desc'],
			'repo': 'https://github.com/Varying-Vagrant-Vagrants/custom-site-template.git',
			'nginx_upstream': new_site_answers['new_site_php_version'],
			'hosts': [
				new_site_answers['new_site_domain'],
				'{}.test'.format(new_site_answers['new_site_domain']),
			],
			'custom': {
				'wpconfig_constants': {
				'WP_VERSION': new_site_answers['new_site_wp_version'],
				'WP_DEBUG': True,
				'WP_DEBUG_LOG': True,
				'WP_DISABLE_FATAL_ERROR_HANDLER': True
				}
			}
		}
	}

	print("Creating new site with the following config:")
	print("")
	print(yaml.dump(new_site_obj, Dumper=IndentDumper, allow_unicode=True, default_flow_style=False, sort_keys=False))

	y_or_no = [
	    {
	        'type': 'confirm',
	        'message': 'Do you want to continue?',
	        'name': 'continue',
	        'default': False,
	    }
	]

	y_or_no_answer = prompt(y_or_no)

	if y_or_no_answer["continue"] is True:
		documents["sites"].update(new_site_obj)

		# Write vvv yaml config
		with open(config, 'w') as stream:
		    try:
		        yaml.dump(documents, stream, Dumper=IndentDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
		    except yaml.YAMLError as exc:
		        print(exc)

		print("Config has been appended to {}".format(config))
		print()
		
		y_or_no = [
		    {
		        'type': 'confirm',
		        'message': 'Do you want to add more sites before provisioning?',
		        'name': 'continue',
		        'default': False,
		    }
		]

		y_or_no_answer = prompt(y_or_no)

		if y_or_no_answer["continue"] is True:
			bcvvv_exit()
			bcvvv_setup_new_site()
		else:
			pass

		# Apply changes
		print("Applying changes")
		bcvvv_apply_changes()

		# Copy custom gitignore 
		print()
		print("Copying ./bc-gitignore-sample to ./www/{}/public_html/.gitignore".format(new_site_title_no_spaces))
		dir_exists = os.path.isdir("./www/{}/public_html/".format(new_site_title_no_spaces))
		
		if dir_exists is True:
			copyfile("./bc-gitignore-sample", "./www/{}/public_html/.gitignore".format(new_site_title_no_spaces))
		else:
			print("./www/{}/public_html/ does not exist and gitignore can't be created. Please copy/paste the contents of ./bc-gitignore-sample the ./gitignore manually.".format(new_site_title_no_spaces))

		# print information about ssh agent, github and git integration and docs
		print()
		print("Further instructions:")
		print("1) Setup git repository in Git")
		print("2) Ensure you have proper access to the repository")
		print("3) Forward local SSH key with ssh-agent")
		print("4) Update {} with git config (refer to VVV documentation and ./config/default-config.yml)".format(config))
		print("5) Apply config changes with ./bcvvv.py or vagrant cli")
		print()
	else:
		bcvvv_exit() 

def bcvvv_setup_existing_site():

	# Existing site message
	print()
	print("You have chosen to setup an existing site.")
	print()
	print("Please ensure the following prerequisities has been satisifed:")
	print("1) The site is already in a Git repository, e.g., wordpress-example-com")
	print("2) You have proper access to the repository")
	print("3) Your SSH key has been forwarded with ssh-agent or similar")
	print()

	y_or_no = [
	    {
	        'type': 'confirm',
	        'message': 'Do you want to continue?',
	        'name': 'continue',
	        'default': False,
	    }
	]

	y_or_no_answer = prompt(y_or_no)

	if y_or_no_answer["continue"] is True:
		pass
	else:
		bcvvv_exit() 

	# PyInquirer questions
	existing_site_questions = [
		{
			'type': 'input',
			'name': 'existing_site_domain',
			'message': 'What\'s the domain name',
		},
		{
			'type': 'input',
			'name': 'existing_site_php_version',
			'message': 'What PHP version do you want (php56, php70, php71, php72, php73, php74)',
			#'validate': lambda val: val == 'Doe' or 'is your last name Doe?'
		},
		{
			'type': 'input',
			'name': 'existing_site_title',
			'message': 'What\'s the Wordpress title'
			#'validate': PhoneNumberValidator
		},
		{
			'type': 'input',
			'name': 'existing_site_desc',
			'message': 'What\'s the Wordpress description',
		},
		{
			'type': 'input',
			'name': 'existing_site_wp_version',
			'message': 'What\'s the Wordpress version',
			#'validate': lambda val: val == 'Doe' or 'is your last name Doe?'
		},
		{
			'type': 'input',
			'name': 'existing_git_repo',
			'message': 'What\'s the Git repository (format: git@github.com:BetterCollective/wordpress-example-com.git)',
			#'validate': lambda val: val == 'Doe' or 'is your last name Doe?'
		}
	]

	existing_site_answers = prompt(existing_site_questions)

	# remove spaces from title
	existing_site_title_no_spaces = "".join(existing_site_answers['existing_site_title'].split())

	existing_site_obj = {
		existing_site_title_no_spaces: {
			'skip_provisioning': False,
			'description': existing_site_answers['existing_site_desc'],
			'repo': 'https://github.com/Varying-Vagrant-Vagrants/custom-site-template.git',
			'nginx_upstream': existing_site_answers['existing_site_php_version'],
			'hosts': [
				existing_site_answers['existing_site_domain'],
				'{}.test'.format(existing_site_answers['existing_site_domain']),
			],
			'folders': {
				'public_html/': {
					'git': {
						'repo': existing_site_answers['existing_git_repo'],
						'branch': 'staging',
						'overwrite_on_clone': True,
						'pull': True
					}
				}
			},
			'custom': {
				'wpconfig_constants': {
				'WP_VERSION': existing_site_answers['existing_site_wp_version'],
				'WP_DEBUG': True,
				'WP_DEBUG_LOG': True,
				'WP_DISABLE_FATAL_ERROR_HANDLER': True
				}
			}
		}
	}

	print("Creating existing site with the following config:")
	print("")
	print(yaml.dump(existing_site_obj, Dumper=IndentDumper, allow_unicode=True, default_flow_style=False, sort_keys=False))

	y_or_no = [
	    {
	        'type': 'confirm',
	        'message': 'Do you want to continue?',
	        'name': 'continue',
	        'default': False,
	    }
	]

	y_or_no_answer = prompt(y_or_no)

	if y_or_no_answer["continue"] is True:
		documents["sites"].update(existing_site_obj)

		# Write vvv yaml config
		with open(config, 'w') as stream:
		    try:
		        yaml.dump(documents, stream, Dumper=IndentDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
		    except yaml.YAMLError as exc:
		        print(exc)

		print("Config has been appended to {}".format(config))
		print()
		
		y_or_no = [
		    {
		        'type': 'confirm',
		        'message': 'Do you want to add more sites before provisioning?',
		        'name': 'continue',
		        'default': False,
		    }
		]

		y_or_no_answer = prompt(y_or_no)

		if y_or_no_answer["continue"] is True:
			bcvvv_exit()
			bcvvv_setup_existing_site()
		else:
			pass

		# Apply changes
		print("Applying changes")
		bcvvv_apply_changes()

		# print information about ssh agent, github and git integration and docs
		print()
		print("Further instructions:")
		print("1) Download webroot with FTP from Plesk and place in webroot ./www/{}/public_html/".format(existing_site_title_no_spaces))
		print("2) Download SQL dump and import for database (PhpMyAdmin: http://vvv.test/database-admin/)")
		print("3) Ensure the database parameters in ./www/{}/public_html/wp-config.php has been changed to VVV credentials".format(existing_site_title_no_spaces))
		print("4) Apply config changes with ./bcvvv.py or vagrant cli. This will sync and overwrite files from Git into webroot again. This can be done manually with git cli in ./www/{}/public_html/".format(existing_site_title_no_spaces))
		print("5) Develop and utilise git commands at ./www/{}/public_html/".format(existing_site_title_no_spaces))
		print()	
	else:
		bcvvv_exit() 

def bcvvv_list_sites():
	print(yaml.dump(documents["sites"], Dumper=IndentDumper, allow_unicode=True, default_flow_style=False, sort_keys=False))
	print()

def bcvvv_edit_sites():
	print()
	print("This feature has not been added. Refer to {} and VVV for further changes.".format(config))
	print()

def bcvvv_apply_changes():
	# This is a temporary fix to a bug that has been known in VVV for a long time.
	os.system('vagrant halt; vagrant up --provision')

def bcvvv_exit():
	sys.exit()

def bcvvv_docs():
	print()
	print("documentation referals:")
	print("* VVV documenation (https://varyingvagrantvagrants.org)")
	print("* DevOps documentation at GitHub (dev-ops repository)")
	print("* DevOps documentation at BookStack")
	print("* Contact DevOps to be refered to wider Wordpress and Plesk documenation specific to BC")
	print()

def bcvvv_contact():
	print()
	print("Contact DevOps at devops@bettercollective.com")
	print()


""" Initial questions """

# PyInquirer questions
questions = [
    {
        'type': 'list',
        'name': 'primary',
        'message': 'What do you want to do',
        'choices': [
            'Setup new site',
            'Setup existing site',
            'List sites',
            'Edit sites (feature not added)',
            'Apply config changes',
            'Exit',
            Separator(),
            'Find documentation',
            'Contact DevOps for support'
        ]
    }
]

answers = prompt(questions)

if answers["primary"] == 'Setup new site':
	bcvvv_setup_new_site()
elif answers["primary"] == 'Setup existing site':
	bcvvv_setup_existing_site()
elif answers["primary"] == 'List sites':
	bcvvv_list_sites()
elif answers["primary"] == 'Edit sites (feature not added yet)':
	bcvvv_edit_sites()
elif answers["primary"] == 'Apply config changes':
	bcvvv_apply_changes()
elif answers["primary"] == 'Exit':
	bcvvv_exit()
elif answers["primary"] == 'Find documentation':
	bcvvv_docs()
elif answers["primary"] == 'Contact DevOps for support':
	bcvvv_contact()
