#!/usr/bin/env python
from radical.entk import Pipeline, Stage, Task, AppManager
import os
import time
# ------------------------------------------------------------------------------
# Set default verbosity
# Set default verbosity
if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
    os.environ['RADICAL_ENTK_REPORT'] = 'True'
os.environ['RADICAL_ENTK_PROFILE'] = "True"
os.environ['RADICAL_LOG_LVL'] = "DEBUG"
os.environ['RADICAL_LOG_TGT'] = "radical.log"
os.environ['RADICAL_PROFILE'] = "TRUE"
os.environ['RADICAL_PILOT_DBURL'] = "mongodb://esraa:@129.114.17.185:27017/esraa"
# Description of how the RabbitMQ process is accessible
# No need to change/set any variables if you installed RabbitMQ has a system
# process. If you are running RabbitMQ under a docker container or another
# VM, set "RMQ_HOSTNAME" and "RMQ_PORT" in the session where you are running
# this script.
hostname = os.environ.get('RMQ_HOSTNAME', 'localhost')
port = int(os.environ.get('RMQ_PORT', 5672))
username = os.environ.get('RMQ_USERNAME', 'esraa')
password = os.environ.get('RMQ_PASSWORD', '')

if __name__ == '__main__':
    total_time = []
    run_time = []
    terminateTimeArray=[]

    number_of_cores=[1,2,4,8,16,32]


    for i in range(6):

        start_time = time.time()
        
        # Create a Pipeline object
        Pipelines=[]

        # Create piplines. #piplines = 4 * #cores
        for cnt in range(10):
            p = Pipeline()

            #Create the stages in a pipline
            for cnt2 in range (12):
                # Create a Stage object
                s = Stage()
                # Create a Task object
                t = Task()
                if cnt2 % 2 ==0:
                    t.name = 'a %s' %(cnt2+1) 
                else:
                    t.name = 'b %s' %(cnt2+1) 

                #The task does nothing ("sleeps") for one second  
                t.executable ='$HOME/tem/stress-ng'   # Assign executable to the task
                t.arguments = ['-c','1','-t','100']  
                #t.arguments = ['100']  # Assign arguments for the task executable
                # Add the Task to the Stage
                s.add_tasks(t)
                # Add Stage to the Pipeline
                p.add_stages(s)
            Pipelines.append(p)




        # Create Application Manager
        appman = AppManager(hostname=hostname, port=port, autoterminate=False, username=username, password=password)
        # Create a dictionary describe four mandatory keys:
        # resource, walltime, and cpus
        # resource is 'local.localhost' to execute locally
        res_dict = {
            'resource': 'xsede.comet_ssh',
            'project' : 'unc100',
            'queue' : 'compute',
            'walltime':500,
            'cpus': number_of_cores[i],
            'access_schema': 'gsissh'
        }


        # Assign resource request description to the Application Manager
        appman.resource_desc = res_dict
        # Assign the workflow as a set or list of Pipelines to the Application Manager
        # Note: The list order is not guaranteed to be preserved
        appman.workflow = set(Pipelines)
        # Run the Application Manager
        run_time_start=time.time()
        appman.run()
        terminateTimeStart=time.time()
        appman.terminate()
        terminateTimeArray.append(time.time()-terminateTimeStart)

        run_time.append(time.time()-run_time_start)
        total_time.append(time.time()-start_time)
        print("runTime",run_time,"number_of_cores", number_of_cores[i])


    print("FINAL--->","total_time",total_time,"runTime",run_time,"terminateTimeArray", terminateTimeArray)

