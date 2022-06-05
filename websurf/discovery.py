#!/usr/bin/env python3
import re
import requests

import websurf.utils as utils
import websurf.logger as logger

# TODO: Make this controllable via an argument.
common_ports = [80, 8000, 8080]

def check_host(host, verbose=False):
    # TODO: Add support for SSL.
    for port in common_ports:
        try:
            # If no exception is raised from this, that means there's a web server here.
            r = requests.get(f'http://{host}:{port}/', timeout=0.5, verify=False)

            # Add a separator for each entry if verbosity is on.
            # TODO: Fuck off with this shit
            if verbose:
                logger.message('-' * 50)
            
            logger.success(f'Found server at http://{host}:{port}/')

            if verbose:
                try:
                    # TODO: Check status code
                    html = r.text
                    d = re.search('<\W*title\W*(.*)</title', html, re.IGNORECASE)

                    if d.group(1):
                        logger.success(f'    Page title:  \'{d.group(1)}\'')

                    if 'Server' in r.headers:
                        logger.success(f'    Server type: \'{r.headers["Server"]}\'')
                except:
                    # There is no title found.
                    pass

        except requests.exceptions.ConnectTimeout:
            # if verbose:
            #     logger.error(f'{host}:{port} timed out.')

            pass
        except requests.exceptions.ConnectionError as ex:
            # Temporary
            if 'The requested address is not valid' in ex.args[0].args[0]: # ew
                if verbose:
                    logger.warning(f'Skipping invalid address: {host}')

                return

            logger.error(ex.args[0])

"""
Main discovery logic.
"""
def begin_discovery(args):
    try:
        addresses = utils.expand_ip_range(args.range)
    except Exception as ex:
        # really shitty hack
        if 'does not appear to be a' in ex.args[0]:
            logger.error('Invalid range given!')
        else:
            logger.error(ex)

        return

    if not args.skip_ping:
        logger.message(f'Checking for active hosts... (Block size: {len(addresses) + 2})')

        alive_addresses = utils.ping_hosts(addresses, 
            chunk_size=args.size, verbose=args.verbose)

        if len(alive_addresses) <= 0:
            logger.error('0 hosts responded.')
            return

        logger.message(f'Finished ping process. ({len(alive_addresses)}/{len(addresses) + 2})')

        addresses = alive_addresses
    else:
        logger.warning('Skipped ping check. (NOTE: This can be very slow!)')

    logger.message('Beginning discovery process...')

    for addr in addresses:
        # if args.verbose:
        #     logger.message(f'Checking host \'{addr}\'.')

        check_host(addr, args.verbose)

    logger.message('Discovery process finished.')
