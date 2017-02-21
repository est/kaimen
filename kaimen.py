#!/usr/bin/env python
# coding: utf-8

import sys
import subprocess
import socket

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
        print ' [ALLOW] %s -> :%s' % (src_ip, self.port)
        return shell('iptables -A INPUT -p tcp -s %s --destination-port %s -j DROP' % (src_ip, self.port))

    def disallow(self, src_ip):
        print ' [DISALLOW] %s -> :%s' % (src_ip, self.port)
        return shell('iptables -D INPUT -p tcp -s %s --destination-port %s -j DROP' % (src_ip, self.port))


class Listener(object):
    def __init__(self, port, ):
        self.port = port
        sock.bind(('', 0))
        sock.settimeout(1)  # will fire event every 1 seconds
        self.ticks = 0
        self.iptables = IpTables(port)
        self.iptables.drop()
        self.iptables.keep()

    def __iter__(self):
        while 1:
            try:
                yield sock.recvfrom(1024)
            except:
                self.ticks += 1
                continue


def daemon():
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    else:
        port = 443
    l = Listener(port)
    for data, addr in l:
        # IP + ICMP header == 28 bytes
        if len(data) - 28 == 90:
            l.iptables.allow(addr[0])


if '__main__' == __name__:
    daemon()
