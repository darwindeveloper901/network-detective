import argparse
import asyncio
import socket
import os
from pyfiglet import Figlet

# Custom banner
def print_banner():
    custom_fig = Figlet(font='banner')
    banner = custom_fig.renderText('Network Detective')
    print(banner)
    print("made by Darreus")
    print()


async def port_scan(target, port, log_file):
    """
    Investigate a port on the provided target.
    """
    try:
        # Using asyncio.wait_for() for managing timeouts
        reader, writer = await asyncio.wait_for(asyncio.open_connection(target, port), timeout=5)
        print(f"Port {port}: Accessible")
        log_file.write(f"Port {port}: Accessible\n")
        writer.close()
    except (ConnectionRefusedError, asyncio.TimeoutError):
        pass


async def scan_ports(target, port_range, log_file):
    """
    Probe a spectrum of ports on the given target.
    """
    print(f"Conducting port scans for {target}...")
    tasks = [port_scan(target, port, log_file) for port in port_range]
    await asyncio.gather(*tasks)


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Rapid Network Investigator")
    parser.add_argument("target", help="Target to examine.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-100", help="Port range for scanning, default is 1-100.")
    args = parser.parse_args()

    target = args.target
    port_range = args.port_range

    try:
        start_port, end_port = map(int, port_range.split("-"))
    except ValueError:
        print("Invalid port range format. Please provide the range as 'start-end'.")
        return

    ports = [p for p in range(start_port, end_port + 1)]

    log_filename = f"network_investigation_results_{target}.txt"

    with open(log_filename, "w") as log_file:
        asyncio.run(scan_ports(target, ports, log_file))

    print(f"\nScanning complete. Findings stored in '{log_filename}'.")


if __name__ == "__main__":
    main()