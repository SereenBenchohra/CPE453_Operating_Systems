# Damien Trunkey, Sereen Benchohra, Danveer Cheema
# CPE 453 Program 2-Scheduler

import sys, getopt

# job class to store priority, timing, turnaround, and wait time
class Job():
    arrival_time = 0
    burst_time = 0
    job_num = 0
    turnaround_time = 0
    wait_time = 0
    remaining_time = 0
    exit_time = 0
    
    def __init__(self, burst_time, arrival_time):
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time

# This function reads the job file and puts the job into a Job class and then sorts based on arrival time
def readFile(file_name):
    schedule = []
    try:
        f = open(file_name, "r")
    except:
        print("File {} not found".format(file_name))
        sys.exit(0)
    job_number = 0
    for line in f:
        split_line = line.split(' ')
        job = Job(int(split_line[0]), int(split_line[1].strip('\n')))
        schedule.append(job)
    # sort job based on arrival time and add job number
    sorted_sched = sorted(schedule, key=lambda x : x.arrival_time, reverse = False)
    for job in sorted_sched:
        job.job_num = job_number
        job_number+=1
    return sorted_sched

# this function executes first in first out job scheduling algorithm.
# it runs each job to completion and moves on to the next
def FIFO(schedule):
    time = 0
    for job in schedule:
        job.wait_time = time - job.arrival_time
        time = time + job.burst_time
        job.turnaround_time = time - job.arrival_time

# This function executes round robin based on the quantum parameter passed in.
def RoundRobin(schedule, quantum):
    time = 0
    num_jobs = len(schedule)
    while num_jobs > 0:
        for job in schedule:
            if job.arrival_time <= time:
                if job.remaining_time > quantum:
                    job.exit_time += quantum
                    time += quantum
                    job.remaining_time -= quantum
                elif job.remaining_time <= quantum and job.remaining_time > 0:
                    job.wait_time = time - job.exit_time - job.arrival_time
                    time += job.remaining_time
                    job.remaining_time = 0
                    num_jobs -= 1
                    job.turnaround_time = time - job.arrival_time
            else:
                time += 1

# helper function to find the shortest remaining job next
def find_lowest_job(schedule, time):
    min_job = Job(0xFFFF, 0xFFFF)
    for job in schedule:
        if job.arrival_time <= time:
            if job.remaining_time < min_job.remaining_time and job.remaining_time != 0:
                min_job = job
    return min_job

# executes shortest runtime next scheduling alorithm
def SRTN(schedule):
    time = 0
    num_jobs = len(schedule)
    prev_job = -1
    while num_jobs > 0:
        job = find_lowest_job(schedule, time)
        time += 1
        job.remaining_time -= 1
        prev_job = job.job_num
        if job.remaining_time == 0:
            # turnaround and wait time calculations
            num_jobs -= 1
            job.turnaround_time = time - job.arrival_time
            job.wait_time = job.turnaround_time - job.burst_time

# prints each jobs turnaround and wait times and the average turnaround and wait time
def print_stats(schedule):
    length = len(schedule)
    tot_wait = 0
    tot_turnaround = 0
    for job in schedule:
        tot_wait += job.wait_time
        tot_turnaround += job.turnaround_time
        print("Job %3d -- Turnaround %3.2f  Wait %3.2f" % (job.job_num, job.turnaround_time, job.wait_time))
    avg_wait = tot_wait / length
    avg_turnaround = tot_turnaround / length
    print("Average -- Turnaround %3.2f  Wait %3.2f" % (avg_turnaround, avg_wait))
        

def main(argv):
    alg = ''
    quantum = 1
    if len(argv) < 2:
        print('Usage: schedSim.py <job-file.txt> -p <ALGORITHM> -q <QUANTUM>')
        sys.exit(2)
    filename = argv.pop(0)
    try:
        opts, args = getopt.getopt(argv,"hp:q:",["alg=","quantum="])
    except getopt.GetoptError:
        print('Usage: schedSim.py <job-file.txt> -p <ALGORITHM> -q <QUANTUM>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-p", "--alg"):
            alg = arg
        elif opt in ("-q", "--quantum"):
            quantum = int(arg)
    
    schedule = readFile(filename) 
    if alg == 'FIFO':
        FIFO(schedule)
    elif alg == 'RR':
        RoundRobin(schedule, quantum)
    elif alg == 'SRTN':
        SRTN(schedule)
    else:
        FIFO(schedule)
    
    print_stats(schedule)

if __name__ == "__main__":
    main(sys.argv[1:])




