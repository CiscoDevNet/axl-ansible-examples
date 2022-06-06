import paramiko
from paramiko_expect import SSHClientInteraction
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(hostname='hq-cucm-pub.abc.inc', username='administrator', password='ciscopsdt', timeout=30, look_for_keys=False)        
except Exception as e:
    pass

cli_responses = [{
    'expect': 'Continue \(y/n\)\?',
    'response': 'y',
    'timeout': 5,
    'newline': False
}]
cli_command = 'set cli session timeout 30'

try:
    interact = SSHClientInteraction(ssh, display=False) 
    interact.expect('admin:')
    interact.send(cli_command)
    output = interact.current_output
    if cli_responses is not None:
        for index,item in enumerate(cli_responses):
            try:
                expect = item['expect']
                response = item['response']
                timeout = item.get('timeout')
                newline = '\n' if item.get('newline', True) else ''
            except KeyError as e:
                print(f'Error: key {e} missing in cli_responses[{index}]')
                sys.exit(1)
            interact.expect(expect, timeout=timeout)
            interact.send(response, newline=newline)
            output += interact.current_output
    interact.expect('admin:')
    output += interact.current_output
    tokens = output.splitlines()
    tokens = tokens[tokens.index(f'admin:{cli_command}')+1:-1]
    tokens[:]=[line.split() for line in tokens]    
    ssh.close()
except Exception as e:
    print(f'Error executing CLI command: {e}')
    sys.exit(1)

print(output)
print(tokens)
