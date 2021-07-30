#!/usr/bin/env python3

""" Fundamentals """

from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import prompt, Separator
import json
import yaml
import os
from shutil import copyfile

print()
print("WP local environment for Better Collective based on VVV")
print("Always refer to the official VVV documentation, default-config.yml, and BC documentation.")
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
	print("{0} does not exist. {0} will be created from {1} and used in this util.".format(config, config_sample))
	print()
	copyfile(config_sample, config)

# Read vvv yaml config
with open(config, 'r') as stream:
    try:
        documents = yaml.safe_load(stream);
    except yaml.YAMLError as exc:
        print(exc)

""" Functionality """

# TODO 
# 
# mention ssh-agent configuration
# github config - before and after setup - different from existing or new 
# important paths within VVV: e.g., webroot that git initialised paths
# NEW SITE - copy gitignore file 
# 
# Inspiration from bccw? 
""" 
1) Run '$ vagrant up' and make sure to provision.
2) Replace the files from the existing Wordpress application with the files in ./wordpress/, except ./wordpress/phpmyadmin directory.
3) Login to phpMyAdmin at http://dasd/phpmyadmin, on database 'wordpress', with username 'wordpress' and password 'wordpress', and import your existing database. Make sure your wp-config.php matches these database credentials.
4) Enjoy developing with your files at ./wordpress/ shared with vm folder /var/www/html, with local access at http://dasd.
"""

def bcvvv_list_sites():
	print(yaml.dump(documents["sites"], allow_unicode=True, default_flow_style=False))
	print()

def bcvvv_edit_sites():
	print()
	print("This feature has not been added. Refer to {} and VVV for further changes.".format(config))
	print()

def bcvvv_setup_new_site():

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
			'message': 'What PHP version do you want (e.g. php56, php70, php71, php73)',
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

	new_site_obj = { new_site_answers['new_site_title']: {'skip_provisioning': False, 'description': new_site_answers['new_site_desc'], 'repo': 'https://github.com/Varying-Vagrant-Vagrants/custom-site-template.git', 'nginx_upstream': new_site_answers['new_site_php_version'], 'hosts': [new_site_answers['new_site_domain']], 'custom': {'wpconfig_constants': {'WP_VERSION': 4.7, 'WP_DEBUG': True, 'WP_DEBUG_LOG': True, 'WP_DISABLE_FATAL_ERROR_HANDLER': True}}} }

	print("Creating new site with the following config:")
	print("")
	print(yaml.dump(new_site_obj, allow_unicode=True, default_flow_style=False))

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
		        yaml.safe_dump(documents, stream)
		    except yaml.YAMLError as exc:
		        print(exc)

		print("Config has been appended to {}. Now applying changes.".format(config))
		print()
		
		# Apply changes
		bcvvv_apply_changes()

		# Copy custom gitignore 

		print("Copying ./gitignore-sample to ./www/{}".format(new_site_answers['new_site_title']))
		copyfile("./gitignore-sample", "./www/{}".format(new_site_answers['new_site_title']))

		# print information about ssh agent, github and git integration and docs
		print("Next steps:")
		print("Setup Github, forward ssh key, and update {}".format(config))
	else:
		bcvvv_exit() 

	# TODO and notes
	# generate YAML and insert into config
	# copy gitignore sample to the root folder 
	# 'folders': {'public_html/': {'git': {'repo': 'git@github.com:BetterCollective/wordpress-guidedupari-com.git', 'branch': 'staging', 'overwrite_on_clone': True, 'pull': True}}},

def bcvvv_setup_existing_site():
	pass

def bcvvv_apply_changes():
	# This is a temporary fix to a bug that has been known in VVV for a long time.
	os.system('vagrant ssh -c "rm -f /usr/local/bin/wp"; vagrant reload --provision;')

def bcvvv_exit():
	exit()

def bcvvv_docs():
	print()
	print("documentation referals:")
	print("* VVV documenation can be found at https://varyingvagrantvagrants.org")
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
            'List sites',
            'Edit sites',
            'Setup new site',
            'Setup existing site',
            'Apply config changes',
            'Exit',
            Separator(),
            'Find documentation',
            'Contact DevOps for support'
        ]
    }
]

answers = prompt(questions)

if answers["primary"] == 'List sites':
	bcvvv_list_sites()
	answers = prompt(questions)
elif answers["primary"] == 'Edit sites':
	bcvvv_edit_sites()
	answers = prompt(questions)
elif answers["primary"] == 'Setup new site':
	bcvvv_setup_new_site()
	answers = prompt(questions)
elif answers["primary"] == 'Setup existing site':
	bcvvv_setup_existing_site()
	answers = prompt(questions)
elif answers["primary"] == 'Apply config changes':
	bcvvv_apply_changes()
elif answers["primary"] == 'Exit':
	bcvvv_exit()
elif answers["primary"] == 'Find documentation':
	bcvvv_docs()
	answers = prompt(questions)
elif answers["primary"] == 'Contact DevOps for support':
	bcvvv_contact()
	answers = prompt(questions)