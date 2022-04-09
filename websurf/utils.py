#!/usr/bin/env python3

import platform
import ipaddress
import subprocess

import websurf.logger as logger

"""
Expands a given netblock into it's individual addresses.
"""
def expand_ip_range(range):
    addresses = []

    # We have to do it in this way because it's a generator.
    for addr in ipaddress.ip_network(range).hosts():
        addresses.append(str(addr))

    return addresses

"""
Returns a list of hosts that successfully pinged back.
"""
def ping_hosts(hosts, attempts=3, verbose=False):
    alive_hosts = []

    # TODO: Make this update in real time and rewrite this fucking mess.

    # https://stackoverflow.com/questions/12101239/multiple-ping-script-in-python/12102040#12102040
    procs = {} # ip -> process

    for host in reversed(hosts):
        # logger.message(f'Pinging host \'{host}\'.')

        procs[host] = subprocess.Popen(
            f'ping -n {attempts} {host}',
            stdout=subprocess.PIPE)

    while procs:
        # Shitty hack to avoid an error.
        host = list(procs)[-1]
        proc = procs[list(procs)[-1]]

        # Wait until the process is finished.
        if proc.poll() is not None:
            output, err = proc.communicate()
            output = output.decode('utf-8')

            # Parse the output.
            if 'TTL' in output:
                if verbose:
                    logger.message(f'Received response from host \'{host}\'.')

                alive_hosts.append(host)
            elif 'unreachable' in output:
                pass
            elif 'timed out' in output:
                if verbose:
                    logger.error(f'Connection to host {host} timed out.')
            else:
                output_lines = output.split('\r\n')

                for line in output_lines:
                    print(line)

            procs.popitem()

    return alive_hosts