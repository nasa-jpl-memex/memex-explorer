""" Module for querying supervisor for running/available services
"""

import xmlrpclib
import socket

def check_process_state(process_name, state='RUNNING'):
    server = xmlrpclib.Server('http://localhost:9001/RPC2')
    try:
        response = server.supervisor.getProcessInfo(process_name)['statename'] == state
    except socket.error:
        response = None
    return response