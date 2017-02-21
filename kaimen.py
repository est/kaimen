#!/usr/bin/env python
# coding: utf-8

import subprocess
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)


def shell(cmd):
    return subprocess.Popen(
        cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


class IpTables(object):
    def __init__(self):
        # delete then add
        shell('iptables -D INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT')
        shell('iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT')

    def drop(self, port):
        print ' [DROP]', port
        return shell('iptables -A INPUT -p tcp --destination-port %s -j DROP' % port)

    def undrop(self, port):
        print ' [DROP]', port
        return shell('iptables -D INPUT -p tcp --destination-port %s -j DROP' % port)


def listen_forever():
    """yield data, addr"""
    sock.bind(('', 0))
    sock.settimeout(5)
    while 1:
        try:
            yield sock.recvfrom(1024)
        except:
            continue


def daemon():
    t = IpTables()
    t.drop(444)
    for data, addr in listen_forever():
        print len(data), addr
        if len(data) - 20 == 90:
            t.undrop(444)


if '__main__' == __name__:
    daemon()
