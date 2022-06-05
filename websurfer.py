#!/usr/bin/env python3
import argparse

import websurf.utils as utils
import websurf.logger as logger
from websurf.discovery import begin_discovery

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='websurfer',
        description='A utility for discovering web servers on a network.')
    
    parser.add_argument('range', 
        help='The IP range to scan.')

    parser.add_argument('-v', 
        action='store_true', dest='verbose',
        help='Outputs more information.',
        default=False)

    parser.add_argument('-d', 
        action='store_true', dest='debug',
        help='Outputs debug information.',
        default=False)

    parser.add_argument('-s', 
        action='store_true', dest='skip_ping',
        help='Skips the ping process and jumps straight to the discovery process.',
        default=False)

    parser.add_argument('-c', type=int, dest='size',
        help='The number of hosts in each chunk for the pinging process.',
        default=16)

    args = parser.parse_args()

    logger.debug_mode = args.debug

    # print(args)
    begin_discovery(args)

    # logger.message(utils.expand_ip_range('192.0.2.0/29'))