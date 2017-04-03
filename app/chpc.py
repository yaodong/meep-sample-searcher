import sys
from subprocess import Popen, PIPE
from app.params import *
import logging


def squeue(keyword=None):
    """
    %A job id  |  %j job name  |  %t status  |  %u user name
    %V submit time  |  %S expect start time
    """
    command = 'squeue -o \'%A %j %t %u %M %V %S\' | grep ' + CHPC_USER
    if keyword is not None:
        command += ' | grep %s' % keyword

    output = remote_cmd(command)
    jobs = []
    if len(output) > 0:
        lines = output.split('\n')
        for line in lines:
            job_id, job_name, state, user_name, time_used, time_submit, time_expect = line.split()
            jobs.append({
                'job_id': job_id,
                'job_name': job_name,
                'state': state,
                'user_name': user_name,
                'time_used': time_used,
                'time_submit': time_submit,
                'time_expect': time_expect
            })
    return jobs


def rsync(local, dst):
    return local_cmd('sshpass -p %s rsync -r %s %s:%s -q' % (CHPC_PWD, local, CHPC_LOGIN, dst))


def remote_cmd(cmd):
    return local_cmd('sshpass -p %s ssh %s "%s"' % (CHPC_PWD, CHPC_LOGIN, cmd))


def remote_shell_file(file):
    return remote_cmd('bash %s' % file)


def sbatch(filename):
    return remote_cmd('sbatch %s' % filename)


def local_cmd(command):
    logging.debug(command)
    try:
        res = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = res.communicate()
        logging.debug([out, err])
        return out.decode('utf-8').strip()
    except OSError as e:
        logging.info("Error2: ", e.strerror)
        sys.exit()
