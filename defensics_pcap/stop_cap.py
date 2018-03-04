import os
import signal
import time

PCAP_STOP_DELAY = 0.100
"""The delay in seconds to wait for packets to filter into the tshark process and file before killing tshark.

Without it, the final packet(s) in a test are sometimes dropped."""


def main():
    defensics_result_dir = os.environ['CODE_RESULT_DIR']
    pid_filename = os.path.join(defensics_result_dir, 'tshark-pid.txt')
    time.sleep(PCAP_STOP_DELAY)
    stop_pcap(get_pid(pid_filename=pid_filename))
    os.remove(pid_filename)  # Boy scout rule: Leave your file system cleaner than you found it.


def get_pid(pid_filename):
    with open(pid_filename, 'r') as f:
        pid = f.read()
    return int(pid)


def stop_pcap(pid):
    os.kill(pid, signal.SIGTERM)
