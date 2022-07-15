from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False))
    # seed the result dict in the object
    result = dict(changed=False,
        original_message='',
        message='')
    # the AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(argument_spec=module_args,
        supports_check_mode=True)
    # manipulate or modify the state as needed
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'
    # AnsibleModule.fail_json() to pass in failure message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)
    # in the event of a successful module execution, pass the key/value results
    module.exit_json(**result)
def main():
    run_module()
if __name__ == '__main__':
    main()



