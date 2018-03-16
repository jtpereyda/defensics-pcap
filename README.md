The Unofficial Defensics Packet Capture Assistant Tool
======================================================
The unofficial defensics-pcap tool provides per-case packet capture functionality for Defensics.

Prerequisites
-------------
Wireshark and Python.

Install
-------
The following command may need to be run as sudo (Linux) or in an
Administrator command prompt (Windows):

    python -m pip install --upgrade defensics-pcap

To verify proper installation, run:

    defensics-pcap --help

If installed properly, you should see some help text on how to use the
tool.

Usage
-----
 1. In Defensics, click **4) Instrumentation**.
 2. Click **External**.
 3. Use `tshark -D` (or `"C:\Program Files\Wireshark\tshark.exe" -D` on Windows) to identify the proper network interface
    on which to capture.
 4. Place the start-cap command in **Execute before each test case**, e.g.:
    `python -m defensics_pcap start -i 3`
 5. Place the stop-cap command in **Execute after each test case**, e.g.:
    `python -m defensics_pcap stop`
 6. Start your test and verify that .pcap files are being created in your test result directory, usually in
    `C:\Users\username\synopsys\defensics\results`.

How It Works
------------
The `start` command will start a PCAP in the currently running
Defensics results folder. It relies on the `CODE_RESULT_DIR` and
`CODE_TEST_CASE_PADDED` environment variables provided by Defensics, and
will not work if run alone in the command line.

`start-cap` looks for the `tshark` application in your operating system
PATH and also in the default location `C:\Program Files\Wireshark\tshark.exe`.
If you do not have tshark available via the PATH variable, you can
include a full path via the `start-cap` `--tshark-full-path` argument.
See `python -m defensics_pcap start-cap --help`.

`stop_cap.py` will stop the PCAP using the process ID value stored
temporarily in the Defensics results folder.
