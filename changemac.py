#!/usr/bin/env python3

import subprocess
import os
import random
import click

SAFE_IDS = ['00', '02', '04', '06', '08', '0a', '0c', '0e', '10', '12', '14', '16', '18', '1a', '1c', '1e', '20', '22', '24', '26', '28', '2a', '2c', '2e', '30', '32', '34', '36', '38', '3a', '3c', '3e', '40', '42', '44', '46', '48', '4a', '4c', '4e', '50', '52', '54', '56', '58', '5a', '5c', '5e', '60', '62', '64', '66', '68', '6a', '6c', '6e', '70', '72', '74', '76', '78', '7a', '7c', '7e', '80', '82', '84', '86', '88', '8a', '8c', '8e', '90', '92', '94', '96', '98', '9a', '9c', '9e', 'a0', 'a2', 'a4', 'a6', 'a8', 'aa', 'ac', 'ae', 'b0', 'b2', 'b4', 'b6', 'b8', 'ba', 'bc', 'be', 'c0', 'c2', 'c4', 'c6', 'c8', 'ca', 'cc', 'ce', 'd0', 'd2', 'd4', 'd6', 'd8', 'da', 'dc', 'de', 'e0', 'e2', 'e4', 'e6', 'e8', 'ea', 'ec', 'ee', 'f0', 'f2', 'f4', 'f6', 'f8', 'fa', 'fc', 'fe']

def run(command):
    try:
        subprocess.check_output(command.split(" "))
        return 0
    except subprocess.CalledProcessError as e:
        return e.returncode

@click.group()
def cli():
    pass

@cli.command(name="generate")
@click.option("--safe", "-s", is_flag=True, default=False, help="Generate a mac address that can usualy be asigned to non-specialised network cards")
def get_mac(safe):
    click.echo(generate_mac(safe))

def generate_mac(safe=False):
    mac = ":".join(["".join([random.choice("0123456789abcdef") for y in range(2)]) for x in range(6)])
    if safe:
        mac = random.choice(SAFE_IDS) + mac[2::]
    return mac

@cli.command("set")
@click.option("--interface", "-i", default="wlp4s0")
@click.option("--mac", "-m", default=None)
@click.option("--regenerate", "-r", is_flag=True, default=False, help="Flag to alow regeneration of mac if failed to assign")
def set_mac_interface(interface, mac, regenerate):
    if not os.geteuid() == 0:
        click.echo("Changing mac requires root privileges")
        exit()
        return
    return set_mac(interface, mac, regenerate)

def set_mac(interface, mac, regenerate=False):
    mac = generate_mac() if mac is None else mac
    click.echo(f"Setting interface: {interface} to mac: {mac}")

    run("ip link show {}".format(interface))
    run("ip link set dev {} down".format(interface))

    success = 1
    while success != 0:
        print(f"Attempting to change mac to: {mac}")
        success = run("ip link set dev {} address {}".format(interface, mac))
        mac = generate_mac()
        if not regenerate: break
    if success == 0:
        click.echo(f"\nSet interface: {interface} to mac: {mac}")
        ret = True
    else:
        click.echo(f"\nFailed to set interface: {interface} to mac: {mac}")
        ret = False

    run("ip link set dev {} up".format(interface))
    run("ip link show {}".format(interface))
    return ret


if __name__ == "__main__":
    cli()
    # out = {}
    # out1 = []
    # a = "0123456789abcdef"
    # for i in range(len(a)):
    #     for j in range(len(a)):
    #         m = a[i]+a[j]

    #         out[m] = set_mac("wlp4s0", f"{m}:14:5c:25:d1:47", False)

    # for i in out:
    #     if out[i]:
    #         out1.append(i)
    # print(out1)


