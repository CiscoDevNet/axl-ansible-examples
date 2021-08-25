# axl-ansible-samples

## Overview

These samples demonstrates how to use Ansible playbooks to read/update CUCM configurations via the AXL SOAP API.

[https://developer.cisco.com/site/axl/](https://developer.cisco.com/site/axl/)

The concepts and techniques shown can be extended to enable automated management of virtually any configuration or setting in the CUCM admin UI.

Tested with:

- Ubuntu 21.04
- Ansible 2.11.3
- Python 3.9.5
- CUCM 14

## Pre-requisites

- Python 3 

## Available samples

* `addLine.yml` - Demonstrates adding a single line ( `<addLine>`).

* `addPhone.yml` - a simple phone (`<addPhone>`).

* `addUser.yml` - add a simple user (`<updateDevicePool>`).

* `addLinePhoneUserLoop.yml` - Adds a series of users, phones and lines read from a `.csv` file, associated lines->phones and phones->users.

## Getting started

* Install Python 3

    On Windows, choose the option to add to PATH environment variable

* (Optional) Create/activate a Python virtual environment named `venv`:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* Install needed dependency packages:

    ```bash
    pip install -r requirements.txt
    ```

* Rename `inventory.yml.example` to `inventory.yml`, and edit it to specify your CUCM address and AXL user credentials.

* The AXL v14 schema was used in this project.  If you'd like to use a different version, update the `SOAPAction` header and `xmlns:ns` namespace in the XML `body` to reflect your desired version.  If there actual schema differences, you may need to modify the XML as needed

* To run a specific sample, use the following command, e.g.:

    ```bash
    ansible-playbook addLine.yml
    ```

    You will be prompted for appropriate values (e.g. directory number/partition).  
    
    Alternatively, you can provide values as 'key=value' pairs in the command, e.g.:

    ```bash
    ansible-playbook addLine.yml -e "dn=1001 partition=testPartition"
    ```

* The `addLinePhoneUserLoop.yml` sample is in its own subdirectory, and can be run like this:

    ```bash
    ansible-playbook addLinePhoneUserLoop/addLinePhoneUserLoop.yml
    ```

    It does not take any command line arguments, but rather reads the contents of `addLinePhoneUserLoop.csv`.  You can modify this file as needed before running

## Hints

* Note: the samples do not currently do any checking to see if objects are already created before attempting to create them, or perform any 'cleanup' of the AXL objects.  You may need to delete these objects (i.e. manually via CUCM admin) before re-running any of the samples to prevent duplicate item errors.

## Todo

* These samples simply use the `uri` module to do their thing; the result is not very indempotent, in the Ansible fashion.  It should be possible to write a custom module which does things like checking for existence and current config of AXL objects before addding/updating/deleting, so you can get to a more 'declarative' place.
* Several attempts to affect CUCM CLI commands were not successful (`cli_show_version_active.yml` is included, but non-functional), i.e. to drive certain configurations via CLI 'scraping' that can't be done via AXL.  I suspect this could be done by, again, writing a custom module that uses Python paramiko to do its thing.