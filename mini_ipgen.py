#!/usr/bin/env python
#
# If you just want a few random IPs, this might be easier...
#

import netaddr, random, os, sys

def random_ips(num, bogons_file=None):
    # Load bogons
    bogon_networks = []
    if bogons_file is not None:
        with open('bogons.txt', 'r') as fp:
            for line in fp:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                net = netaddr.IPNetwork(line, implicit_prefix=False, version=4)
                bogon_networks.append(net)
    bogon_ipset = netaddr.IPSet(bogon_networks)

    # Generate IPs
    ips = set()
    while len(ips) < num:
        x = random.randint(0, 0xFFFFFFFF)
        ip = netaddr.IPAddress(x)
        if ip not in bogon_ipset:
            ips.add(ip)

    return ips

def main():
    if len(sys.argv) < 2:
        print "Usage: mini_ipgen.py <number-of-ips>"
        sys.exit(1)

    num = int(sys.argv[1])
    for ip in random_ips(num, 'bogons.txt'):
        print ip

if __name__ == '__main__':
    main()
    
