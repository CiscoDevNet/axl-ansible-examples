#!/usr/bin/python

# Based on code from https://github.com/ponchotitlan/ansible_cucm_ssh_module (Alfonso Sandoval)

DOCUMENTATION = '''
---
module: cisco_vos_cli
short_description: Module to execute CLI commands on Cisco UC Voice Operating System (VOS) hosts
description:
    - Logs into the VOS host CLI via SSH (using Paramiko)
    - Tokenizes by lines and white-space separated items in the CLI text output
    - Returns a list of lines, where each line is a list of white-space delimited tokens (as well as the full text response)
    - Please verify options and example for supported usage
author: 'David Staudt'
options:
# One or more of the following
    cli_address:
        description:
            - Target address of the VOS server
        required: false
    cli_user:
        description:
            - OS admin (CLI) user name
        required: true
    cli_password:
        description:
            - OS admin (CLI) user password
        required: true
    cli_command:
        description:
            - Text of the CLI command to be executed
        required: true
    cli_responses:
        description:
            - A list of dicts containing the next expected outputs and corresponding new inputs, with a timeout and newline True/False.
              (timeout and newline a optional)
        required: false
notes:
    - This module supports VOS versions 9.x / 10.x / 11.x / 12.x
    - Supports only single line commands, currently (do not require additional CLI inputs)
requirements:
    - ansible==2.9.12
    - paramiko==2.0.0
    - paramiko-expect==0.2.8
'''

EXAMPLES = '''
- name: Get CUCM DB Replication status 
  hosts: hosts
  connection: local
  gather_facts: no
  tasks:
    - name: Get CUCM DB Replication status
      cisco_vos_cli:
        cli_address: '{{ ansible_host }}'
        cli_user: '{{ ansible_cli_user }}'
        cli_pwd: '{{ ansible_cli_password }}'
        cli_command: set cli session timeout
        cli_responses:
            - expect: "Continue (y/n)?"
              response: y
              timeout: 30
              newline: False
      register: result
    - debug: var=result
'''

from secrets import token_bytes
import paramiko
from paramiko_expect import SSHClientInteraction
from ansible.module_utils.basic import AnsibleModule

def main():
    fields = {'cli_address': {'required': True, 'type': 'str'},
              'cli_user': {'required': True, 'type': 'str'},
              'cli_password': {'required': True, 'type': 'str', "no_log": True},
              'cli_command': {'required': True, 'type': 'str'},
              'cli_responses': {'required': False, 'type': 'list', 'elements': 'dict'}
    }
    module = AnsibleModule(argument_spec=fields)

    cli_address, cli_user, cli_password, cli_command, cli_responses = module.params.values()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=cli_address, username=cli_user, password=cli_password, timeout=30, look_for_keys=False)        
    except Exception as e:
        module.fail_json(msg=f'Unable to establish CLI connection: {e}/{type(e)}')

    try:
        interact = SSHClientInteraction(ssh, display=False) 
        interact.expect('admin:')
        interact.send(cli_command)
        output = interact.current_output
        if cli_responses is not None:
            for index, item in enumerate(cli_responses):
                try:
                    expect = item['expect']
                    response = item['response']
                    timeout = item.get('timeout')
                    newline = '\n' if item.get('newline', True) else ''
                except KeyError as e:
                    module.fail_json(msg=f'Error: key {e} missing in cli_responses[{index}]')
                interact.expect(expect, timeout=timeout)
                interact.send(response, newline=newline)
                output += interact.current_output
        interact.expect('admin:')
        output += interact.current_output
        ssh.close()
    except Exception as e:
        module.fail_json(msg=f'Error executing CLI command: {e}')

    if 'Executed command unsuccessfully' in output:
        module.fail_json(msg='CLI command did not execute successfully', output=output)

    tokens = output.splitlines()
    tokens = tokens[tokens.index(f'admin:{cli_command}')+1:-1]
    tokens[:]=[line.split() for line in tokens]

    module.exit_json(output={'raw': output, 'tokenized': tokens})

if __name__ == '__main__':
    main()