#!/usr/bin/env python
# coding: utf-8

import sys
import subprocess
import socket
from collections import defaultdict

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)


def shell(cmd):
    return subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


class IpTables(object):

    def __init__(self, port):
        self.port = port

    def keep(self):
        """keep existing TCP connections open"""
        shell('iptables -D INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT')
        shell('iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT')

    def drop(self):
        print ' [DROP]', self.port
        return shell('iptables -A INPUT -p tcp --destination-port %s -j DROP' % self.port)

    def allow(self, src_ip):
        # dont use -A
        cmd = 'iptables -I INPUT 2 -p tcp -s %s --destination-port %s -j ACCEPT' % (src_ip, self.port)
        print ' [ALLOW] %s -> :%s\n  %s' % (src_ip, self.port, cmd)
        return shell(cmd)

    def disallow(self, src_ip):
        cmd = 'iptables -D INPUT -p tcp -s %s --destination-port %s -j ACCEPT' % (src_ip, self.port)
        print ' [DISALLOW] %s -> :%s\n  %s' % (src_ip, self.port, cmd)
        return shell(cmd)


class Listener(object):
    def __init__(self, port, ):
        self.port = port
        sock.bind(('', 0))
        sock.settimeout(1)  # will fire event every 1 seconds
        self.ticks = 0
        self.iptables = IpTables(port)
        self.iptables.keep()
        self.iptables.drop()

    def __iter__(self):
        while 1:
            try:
                yield sock.recvfrom(1024)
            except:
                self.ticks += 1
                continue


def daemon():
    if len(sys.argv) != 3:
        print 'Usage: ./kaimen.py <PORT> SIZExTIMES'
        exit(0)
    else:
        port = sys.argv[1]
        size, times = sys.argv[2].lower().split('x')
    # check params
    if port.isdigit() and 0 < int(port) < 65536:
        port = int(port)
    else:
        exit('PORT needs to between 1-65535')

    # check params
    if size.isdigit() and times.isdigit():
        size, times = int(size), int(times)
    else:
        exit('Bad SIZExTIMES')

    l = Listener(port)
    hits = defaultdict(int)
    for data, addr in l:
        # IP + ICMP header == 28 bytes
        print '[PING]', addr[0], len(data) - 28
        if len(data) - 28 == size:
            hits[addr[0]] += 1
            if hits[addr[0]] > times:
                l.iptables.allow(addr[0])
        else:
            hits.pop(addr[0], None)


if '__main__' == __name__:
    daemon()
