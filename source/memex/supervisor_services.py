""" Module for querying supervisor for running/available services
"""

import xmlrpclib
import supervisor.xmlrpc

def check_process_state(process_name, state='RUNNING'):
    server = xmlrpclib.Server('http://localhost:9001/RPC2')
    return server.supervisor.getProcessInfo(process_name)['statename'] == state
