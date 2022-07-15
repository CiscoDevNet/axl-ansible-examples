# axl-ansible-samples

## Overview

These samples demonstrates how to use Ansible playbooks to read/update CUCM configurations via the AXL SOAP API and CUCM CLI/SSH.  Also included is a sample custom Ansible module which can execute CUCM CLI commands and return the output.

[https://developer.cisco.com/site/axl/](https://developer.cisco.com/site/axl/)

https://docs.ansible.com/

The concepts and techniques shown can be extended to enable automated management of virtually any configuration setting on CUCM or other Voice Operating System (VOS) based appliances.

**Tested with:**

- Ubuntu 22.04
- Ansible 2.12.6
- Python 3.10.4
- CUCM 14

> **Note:** this project was developed on Linux.  While core concepts and most code should port to Windows/Mac well, some differences in Ansible implentation/capabilities may require workarounds.

## Pre-requisites

* Python 3.8+

## Available samples

* `axl_add_line_simple.yml` - Demonstrates adding a single line with the basic built-in Ansible `uri` module ( `<addLine>`).

* `axl_cucm_version_simple.yml` - Retrieve CUCM and AXL versions in a single playbook.

* `axl_cucm_version.yml` - Retrieves the node product and AXL versions.  Uses sub-task (`<getCCMVersion>`).

* `axL_add_line.yml` - Add a new line (`<addLine>`).

* `axl_add_phone.yml` - Add a new phone (`<addLine>`).

* `axl_add_user.yml` - Add a new user (`<addUser>`).

* `axl_add_line_phone_user.yml` - Compose multiple sub-tasks to add a user/phone/line in one playbook.

* `axl_bulk_add_users.yml` - Bulk-add users with associated phones/lines, as retrieved from a `.csv` file.
 
* `cisco_vos_cli.py` - Custom Ansible module using Python/[Paramiko](https://www.paramiko.org/) to run arbitrary commands on a node and parse/return the output.

* `cli_show_version.yml` - Run a CLI command to get the active version and display/parse the output.

* `cli_addhoc_command.yml` Run a run-time-defined CLI command on the node and display the output.

* `cli_set_cli_session_timeout.yml` - Run a CLI command which requires user input responses.

* `paramiko_test.py` - Stand-alone version of the `cisco_vos_cli.py` module (easier to debug).

## Getting started

* Create/activate a Python virtual environment named `venv`:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* Install needed dependency packages:

  ```bash
  pip install -r requirements.txt
  ```

* Rename `inventory.yml.example` to `inventory.yml`, and edit it to specify your host(s) address and AXL/CLI user credentials.

* To run a specific sample, use the following command, e.g.:

  ```bash
  ansible-playbook axl_new_line.yml
  ```

  You will be prompted for needed values (e.g. directory number/partition) if not provided via `--extra-vars`:

  ```bash
  ansible-playbook axl_new_line.yml --extra-vars "dn=1001 routePartition=''"
  ```
    
 ## Hints

* Run playbooks with extra verbosity for debugging:

  ```bash
  ansible-playbook axl_version.yml -vvv
  ```

* The AXL sub-tasks do a little checking to see if adding objects fails due to the object already existing - if so the sub-task is marked as '`changed: no`' (otherwise it is marked '`changed: yes`') - a small attempt to follow the Ansible [indempotency](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html) pattern.  The CLI module/sub-tasks do not do any special checking and so all tasks are left as default ('`changed: no`') whether they actually change something or not.

* The AXL playbooks use `getCCMVersion` to determine the AXL version of each host at run-time, and and AXL sub-tasks modify the `SOAPAction` header and `xlmns:ns` namespace in the XML templates accordingly.  However, no attempt is made to modify the schema of the AXL request itself based on version.  As AXL request schemas are pretty mature/stable (especially for basic/common requests) this works fine for now, at least for the current set of samples.

## Todo

* It should be possible to create a custom module using [Zeep](https://docs.python-zeep.org/en/master/) which can build AXL XML dynamically based on the AXL WSDL, per version.  This would also probably make development of additional AXL sub-tasks easier too, by avoiding XML templating.