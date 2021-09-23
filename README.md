# BCVVV ( Varying Vagrant Vagrants for Better Collective )

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/206b06167aaf48aab24422cd417e8afa)](https://www.codacy.com/gh/Varying-Vagrant-Vagrants/VVV?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Varying-Vagrant-Vagrants/VVV&amp;utm_campaign=Badge_Grade) [![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/varying-vagrant-vagrants/vvv.svg)](http://isitmaintained.com/project/varying-vagrant-vagrants/vvv "Average time to resolve an issue") [![Percentage of issues still open](http://isitmaintained.com/badge/open/varying-vagrant-vagrants/vvv.svg)](http://isitmaintained.com/project/varying-vagrant-vagrants/vvv "Percentage of issues still open")

BCVVV is a fork of VVV. We strive to stick as much as possible to the origin repository, but setup a guideline for configuration and development.

Local development environment and guideline for Wordpress at Better Collective.

Always refer to the official VVV documentation, ./config/default-config.yml, and DevOps documentation.

Be aware that 'existing site' refer to a site that is already hosted on Plesk that you want to develop on, and 'new site' refer to a site that is NOT already Plesk, however, that you want to add.

This util is not meant as a configuration manager, but as a guideline and a place to get started.

## Prerequisities

- VirtualBox
- Vagrant
- Python 3

## How To Use

To use it, download and install [Vagrant](https://www.vagrantup.com) and [VirtualBox](https://www.virtualbox.org/). Then, clone this repository and run:

```shell
vagrant plugin install --local
vagrant up --provision
```

Install requirements:
```shell
pip3 install -r ./requirements.txt
```

Run `bcvvv.py`, read notes, and follow instructions carefully:
```shell
./bcvvv.py
```

## Good to know

### .gitignore specific to BC for each new site

This repository contains a file in the root folder called `gitignore-sample` that will be copied into each sites webroot when a new site is added with the `bcvvv.py` script. In case you want to configure sites manually, you can copy the contents of this into a file called `.gitignore` to achieve the same configuration on initiating a new site migration in Plesk. 

### default-config.yml

This repository contains a file in `./config/` called `default-config.yml` that contains an example of a configured site. This has commented lines that can be useful. Refer to this file for further configuration of sites, but stick to the official VVV documentation. 

### .test domain

For each site created, both new and existing, `.test` tld will be appended automatically as an optional domain name. An example could be `guidedupari.com.test`.

### nginx versus apache

A discrepancy that we have to be aware of in this local development environment and our Plesk farm, is that our Plesk farm uses Apache for all sites, and the local development environment uses Nginx. This can create discrepancy in regards of custom Apache configuration particularly for `.htaccess` that will not be applied for sites developed in this environment. The nginx configuration is configured for Wordpress to a high degree, and it should not be a problem. If you are suspicious that problems occur due to the discprenancy of nginx versus apache please contact DevOps.

## Other

When it's done, visit [http://vvv.test](http://vvv.test).

The online documentation contains more detailed [installation instructions](https://varyingvagrantvagrants.org/docs/en-US/installation/).

Original VVV readme has been preserved below.

# VVV ( Varying Vagrant Vagrants )

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/206b06167aaf48aab24422cd417e8afa)](https://www.codacy.com/gh/Varying-Vagrant-Vagrants/VVV?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Varying-Vagrant-Vagrants/VVV&amp;utm_campaign=Badge_Grade) [![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/varying-vagrant-vagrants/vvv.svg)](http://isitmaintained.com/project/varying-vagrant-vagrants/vvv "Average time to resolve an issue") [![Percentage of issues still open](http://isitmaintained.com/badge/open/varying-vagrant-vagrants/vvv.svg)](http://isitmaintained.com/project/varying-vagrant-vagrants/vvv "Percentage of issues still open")

VVV is a local developer environment, mainly aimed at [WordPress](https://wordpress.org) developers. It uses [Vagrant](https://www.vagrantup.com) and VirtualBox, and can be used to build sites, and contribute to WordPress.

## How To Use

To use it, download and install [Vagrant](https://www.vagrantup.com) and [VirtualBox](https://www.virtualbox.org/). Then, clone this repository and run:

```shell
vagrant plugin install --local
vagrant up --provision
```

When it's done, visit [http://vvv.test](http://vvv.test).

The online documentation contains more detailed [installation instructions](https://varyingvagrantvagrants.org/docs/en-US/installation/).

* **Web**: [https://varyingvagrantvagrants.org/](https://varyingvagrantvagrants.org/)
* **Contributing**: Contributions are more than welcome. Please see our current [contributing guidelines](https://varyingvagrantvagrants.org/docs/en-US/contributing/). Thanks!

## Minimum System requirements

[For system requirements, please read the system requirements documentation here](https://varyingvagrantvagrants.org/docs/en-US/installation/software-requirements/)

## Software included

For a comprehensive list, please see the [list of installed packages](https://varyingvagrantvagrants.org/docs/en-US/installed-packages/).
