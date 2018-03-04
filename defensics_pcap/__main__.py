import argparse
import logging
import os
from . import start_cap
from . import stop_cap


TSHARK_DEFAULT_PATH = os.path.join('C:', os.sep, 'Program Files', 'Wireshark', 'tshark.exe')

HELP_TEXT_MAIN = 'Automation assistance for Defensics'
HELP_TEXT_START_CAP = 'Start a packet capture; designed for use with Defensics'
HELP_TEXT_STOP_CAP = 'Stop a packet capture (designed for use in Defensics)'
HELP_INTERFACE_ARG = 'Interface on which to capture. Use tshark -D to see a list of interfaces.'
HELP_TSHARK_FULL_PATH_ARG = 'Full path to tshark executable. ' \
                            'Use when tshark is not available in the PATH ' \
                            'AND the default value ({0}) is not valid on your system.'.format(TSHARK_DEFAULT_PATH)
HELP_DEBUG_ARG = 'Enable debug logging'


def main():
    parser = argparse.ArgumentParser(description=HELP_TEXT_MAIN)
    parser.add_argument('--debug', '-d', help=HELP_DEBUG_ARG, action='store_true', required=False)

    subparsers = parser.add_subparsers(dest='subcommand_name')

    parser_start_cap = subparsers.add_parser("start", help=HELP_TEXT_START_CAP)
    parser_start_cap.add_argument('--interface', '-i', help=HELP_INTERFACE_ARG, type=int, required=True)
    parser_start_cap.add_argument('--tshark-full-path', help=HELP_TSHARK_FULL_PATH_ARG, type=str, default=None)

    subparsers.add_parser("stop", help=HELP_TEXT_STOP_CAP)

    parsed_args = parser.parse_args()

    # global arguments
    if parsed_args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # sub commands
    if parsed_args.subcommand_name == "start":
        start_cap.main(interface=parsed_args.interface, tshark_full_path=parsed_args.tshark_full_path)
    elif parsed_args.subcommand_name == "stop":
        stop_cap.main()


if __name__ == "__main__":
    main()
