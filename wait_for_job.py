#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import time

def wait_for_job(job_id, jobs_list_file):
    while True:
        with open(jobs_list_file, 'r') as file:
            first_line = file.readline().strip().split()[0]  # Get the first word of the first line
            if first_line == job_id:
                return {"status": "success"}
        time.sleep(5)  # Wait for 5 seconds before retrying

def main():
    module = AnsibleModule(
        argument_spec=dict(
            job_id=dict(required=True, type='str'),
            jobs_list_file=dict(required=True, type='str')
        )
    )

    job_id = module.params['job_id']
    jobs_list_file = module.params['jobs_list_file']

    result = wait_for_job(job_id, jobs_list_file)
    module.exit_json(**result)

if __name__ == '__main__':
    main()
