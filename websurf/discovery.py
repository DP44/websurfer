#!/usr/bin/env python3
import requests

import websurf.utils as utils
import websurf.logger as logger

# TODO: Make this controllable via an argument.
common_ports = [80, 8000, 8080]

def check_host(host, verbose=False):
    # TODO: Add support for SSL.
    for port in common_ports:
        try:
            r = requests.get(f'http://{host}:{port}/', timeout=0.5, verify=False)

            print(r)
            # No exception raised, this means there's a web server here.
            logger.success(f'Found server at http://{host}:{port}/')
        except requests.exceptions.ConnectTimeout:
            # if verbose:
            #     logger.error(f'{host}:{port} timed out')
            pass
        except requests.exceptions.ConnectionError as ex:
            logger.error(ex)

"""
Main discovery logic.
"""
def begin_discovery(args):
    try:
        addresses = utils.expand_ip_range(args.range)
    except:
        logger.error('Invalid range given!')
        return

    if not args.skip_ping:
        logger.message("Checking for active hosts...")

        alive_addresses = utils.ping_hosts(addresses, verbose=args.verbose)

        if len(alive_addresses) <= 0:
            logger.error('0 hosts responded.')
            return

        logger.message(f'Finished ping process. ({len(alive_addresses)}/{len(addresses)})')

        addresses = alive_addresses
    else:
        logger.warning("Skipped ping check.")

    logger.message("Beginning discovery process...")

    for addr in addresses:
        # if args.verbose:
        #     logger.message(f'Checking host \'{addr}\'.')

        check_host(addr, args.verbose)

    logger.message("Discovery process finished.")
