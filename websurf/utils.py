#!/usr/bin/env python3
import platform
import ipaddress
import subprocess

import websurf.logger as logger

"""
Breaks a list into chunks of a given size.
"""
def split_list(orig, chunk_size):
    chunks = []

    for i in range(0, len(orig), chunk_size):
        chunks.append(orig[i:i + chunk_size])

    return chunks

"""
Expands a given netblock into it's individual addresses.
"""
def expand_ip_range(range):
    addresses = []

    # We have to do it in this way because it's a generator.
    for addr in ipaddress.ip_network(range, strict=False).hosts():
        addresses.append(str(addr))

    return addresses

"""
Returns a list of hosts that successfully pinged back.
"""
def ping_hosts(hosts, attempts=3, chunk_size=16, verbose=False):
    alive_hosts = []

    # TODO: Make this update in real time and rewrite this fucking 
    #       mess with a proper ping system.

    # Make sure we aren't running a shit ton of processes at once.
    # If we weren't relying off the ping command, this wouldn't be
    # a thing we'd ever need to do.
    chunks = split_list(hosts, chunk_size) # was 256 but my pc couldn't handle it lol

    while chunks:
        chunk = chunks[0]
        
        # TODO: This is more debug info, add a -d flag for debug messages?
        logger.debug(f'Processing chunk of size: {len(chunk)} ({len(chunks)} chunk/s left)')

        # https://stackoverflow.com/questions/12101239/multiple-ping-script-in-python/12102040#12102040
        procs = {} # ip -> process

        # NOTE: THIS IS VERY CPU INTENSIVE WITH LARGE CHUNKS!!!! STOP DOING THIS 
        for host in reversed(chunk):
            # logger.message(f'Pinging host \'{host}\'.')

            # Doesn't work on linux, the output is spammed as of now.
            procs[host] = subprocess.Popen(
                ('ping -c ' if platform.system() == 'Linux' else 'ping -n ') + 
                f'{attempts} {host}', shell=True, stdout=subprocess.PIPE)

        while procs:
            # Shitty hack to avoid an error.
            host = list(procs)[-1]
            proc = procs[list(procs)[-1]]

            # Wait until the process is finished.
            if proc.poll() is not None:
                output, err = proc.communicate()
                print(output)
                output = output.decode('utf-8')

                # Parse the output.
                if 'TTL' in output:
                    if verbose:
                        logger.message(f'Received response from host \'{host}\'.')

                    alive_hosts.append(host)
                elif 'unreachable' in output:
                    pass
                elif 'timed out' in output:
                    # if verbose:
                    #     logger.error(f'Connection to host {host} timed out.')

                    pass
                else:
                    output_lines = output.split('\r\n')

                    for line in output_lines:
                        print(line)

                procs.popitem()

        chunks.pop(0)

    return alive_hosts