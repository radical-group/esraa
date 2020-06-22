#!/usr/bin/env python
from radical.entk import Pipeline, Stage, Task, AppManager
import os
import time
# ------------------------------------------------------------------------------
# Set default verbosity
if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'
os.environ['RADICAL_ENTK_PROFILE'] = "True"
os.environ['RADICAL_LOG_LVL'] = "DEBUG"
os.environ['RADICAL_LOG_TGT'] = "radical.log"
os.environ['RADICAL_PROFILE'] = "TRUE"
os.environ['RADICAL_PILOT_DBURL'] = "mongodb://esraa:4U4bc6sxyJfHvbdP@129.114.17.185:27017/esraa"
# Description of how the RabbitMQ process is accessible
# No need to change/set any variables if you installed RabbitMQ has a system
# process. If you are running RabbitMQ under a docker container or another
# VM, set "RMQ_HOSTNAME" and "RMQ_PORT" in the session where you are running
# this script.
hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))
username = os.environ.get('RMQ_USERNAME', 'esraa')
password = os.environ.get('RMQ_PASSWORD', '4U4bc6sxyJfHvbdP')

def generate_pipline(stages, tasks_per_stage=1):
    p = Pipeline()

    ##Create 8 stages each with one task
    for s_cnt in range(stages):
        s= Stage()
        s.name = 'stage %s' %(s_cnt+1)

        for t_cnt in range(tasks_per_stage):
            t = Task()
            t.name = 'task %s' %(t_cnt+1)    
            t.executable = '/bin/sleep'
            t.arguments = ['100']
            # Add the Task to the Stage
            s.add_tasks(t)
    # Add Stage to the Pipeline
        p.add_stages(s)

    return p



if __name__ == '__main__':
    total_time = []
    run_time = []
    terminateTimeArray=[]


    start_time = time.time()
    piplines=[]

    for i in range(16):
        pipline = generate_pipline(stages=8, tasks_per_stage=1)
        piplines.append(pipline)

    


    # Create Application Manager
    appman = AppManager(hostname=hostname, port=port, autoterminate=False, username=username, password=password)
    # Create a dictionary describe four mandatory keys:
    # resource, walltime, and cpus
    # resource is 'local.localhost' to execute locally
    res_dict = {
        'resource': 'xsede.comet_ssh',
        'project' : 'unc100',
        'queue' : 'compute',
        'walltime': 30,
        'cpus': 128,
        'access_schema': 'gsissh'
    }

    # Assign resource request description to the Application Manager
    appman.resource_desc = res_dict
    # Assign the workflow as a set or list of Pipelines to the Application Manager
    # Note: The list order is not guaranteed to be preserved
    appman.workflow = set(piplines)

    run_time_start= time.time()

    #run the application manager
    appman.run()
    terminateTimeStart=time.time()
    appman.terminate()
    terminateTimeArray.append(time.time()-terminateTimeStart)

    run_time.append(time.time()-run_time_start)
    total_time.append(time.time()-start_time)

    print("total_time",total_time,"runTime",run_time,"terminateTimeArray", terminateTimeArray)

