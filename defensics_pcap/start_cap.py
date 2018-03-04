import distutils.spawn
import logging
import os
import platform
import subprocess
import sys
import time

TSHARK_DEFAULT_PATH = os.path.join('C:', os.sep, 'Program Files', 'Wireshark', 'tshark.exe')


def main(interface, tshark_full_path=None):
    defensics_result_dir = os.environ['CODE_RESULT_DIR']
    defensics_test_case = os.environ['CODE_TEST_CASE_PADDED']

    pcap_filename = os.path.join(defensics_result_dir,
                                 '{defensics_test_case}.pcapng'.format(defensics_test_case=defensics_test_case))
    pid_filename = os.path.join(defensics_result_dir, 'tshark-pid.txt')

    pid = start_pcap(tshark_full_path=find_tshark(tshark_full_path_arg=tshark_full_path),
                     pcap_filename=pcap_filename,
                     interface=interface, )
    with open(pid_filename, 'w') as f:
        f.write(pid)
    pend_on_file(filename=pcap_filename)


def find_tshark(tshark_full_path_arg=None):
    if tshark_full_path_arg is not None:
        return tshark_full_path_arg
    else:
        search_result = distutils.spawn.find_executable('tshark')
        if search_result is not None:
            return search_result
        else:
            return TSHARK_DEFAULT_PATH


def start_pcap(tshark_full_path, pcap_filename, interface):
    """Start a new pcap process (using tshark).

    :param tshark_full_path: Path to tshark, including executable name, e.g., 'C:\\Program Files\\Wireshark\\tshark.exe'
    :type tshark_full_path: str

    :param pcap_filename: Path to filename of new pcap
    :type pcap_filename: str

    :param interface: Interface number. Interface numbers can be checked using `tshark -D`
    :type interface: int

    :return: Pid (process ID) of new process.
    :rtype: str
    """
    devnull = open(os.devnull, 'wb')
    # set system/version dependent "start_new_session" analogs
    kwargs = {}
    if platform.system() == 'Windows':
        # from msdn
        CREATE_NEW_PROCESS_GROUP = 0x00000200  # note: could get it from subprocess
        DETACHED_PROCESS = 0x00000008  # 0x8 | 0x200 == 0x208
        kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP, close_fds=True)
    elif sys.version_info < (3, 2):  # assume posix
        kwargs.update(preexec_fn=os.setsid, stdout=devnull, stderr=devnull)
    else:  # assume posix AND Python 3.2+
        kwargs.update(start_new_session=True, stdout=devnull, stderr=devnull)
    logging.debug("starting tshark ({full_path})...".format(full_path=tshark_full_path))

    results = subprocess.Popen(
        [tshark_full_path, '-i{i}'.format(i=interface), '-Ql', '-w', pcap_filename],
        **kwargs)
    logging.debug("tshark start complete.".format(full_path=tshark_full_path))
    return str(results.pid)


def pend_on_file(filename, max_wait=5):
    """Wait for filename to start existing.

    This function is used to determine when a target pcap file has been created, thus signaling that the tshark process
    has started collecting. The fact that the pcap file signals collection has started is technically an undocumented
    detail, and has not been rigorously verified, and could therefore be subject to future change, which could result
    in lost packets at the beginning of a test.

    :param filename: Name of file on which to wait
    :type filename: str

    :param max_wait: Maximum time in seconds to wait.
    :type max_wait: float

    :return: None
    """
    start = time.time()
    while not os.path.isfile(filename) and not (time.time() - start >= max_wait):
        pass
