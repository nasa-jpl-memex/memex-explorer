""" Module for querying supervisor for running/available services
"""

import xmlrpclib
import socket
import time

# supervisor doesn't know how to "wait to bring up a process until other processes are ready"
# but I can wait for 3 seconds before querying supervisor on other process status to give them a chance to get ready
wait_3 = True


def check_process_state(process_name, state='RUNNING'):
    global wait_3
    if wait_3:
        time.sleep(3)
        wait_3 = False
    server = xmlrpclib.Server('http://localhost:9001/RPC2')
    try:
        response = server.supervisor.getProcessInfo(process_name)['statename'] == state
    except socket.error:
        response = None
    return response