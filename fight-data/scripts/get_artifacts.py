#!/usr/bin/env python3
import requests

projectid = "39193"
def get_job_id(headers):
    s = requests.Session()
    print("Will use these headers:")
    print(headers)
    s.headers.update(headers)
    # Get the list of jobs
    url = f'https://gitlab.mitre.org/api/v4/projects/{projectid}/jobs/'
    print("Sending this request:")
    print(url)
    r = s.get(url)
    print("Received this response:")
    jdata = r.json()
    print(jdata)
    jobs = {}
    for job in jdata:
        jobid = job['id']
        jobs[jobid] = [job['ref'], job['status']]
    latest_jobid = 0
    latest_job_branch = ""
    # Find the most recent job in the develop branch that was successful.
    for jobid in sorted(jobs.keys(), reverse=True):
        #if jobs[jobid][0] == 'develop' and jobs[jobid][1] == 'success':
        if jobs[jobid][1] == 'success':
            latest_jobid = jobid
            latest_job_branch = jobs[jobid][0]
            break
    return latest_jobid, latest_job_branch

def get_artifacts(headers, jobid):
    s = requests.Session()
    s.headers.update(headers)
    local_filename = 'artifacts.zip'
    url = f'https://gitlab.mitre.org/api/v4/projects/{projectid}/jobs/{jobid}/artifacts/'
    # NOTE the stream=True parameter
    r = s.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush() 
    f.close()
    return local_filename

if __name__ == "__main__":
    headers = {
       'PRIVATE-TOKEN': '37xPm9qeYSbV81aMXq7c' 
    }
    jobid, branch = get_job_id(headers)
    print(f'Fetching artifacts for job {jobid}, branch {branch}')
    filename = get_artifacts(headers, jobid)
    print(f'Saved {filename}')
