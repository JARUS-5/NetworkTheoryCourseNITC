"""
Author: Suraj S (B170389EC)
Contributors: Sayed Muhsin & Senna Manoj

Python Version: 3.6.9
OS: Ubuntu 18.04

ICMP echo source: https://tools.ietf.org/html/rfc792#page-14
"""

import socket
import sys
import time

try:
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_RAW,
                      socket.getprotobyname("icmp"))
except:
    print("Program requires root permission. Error with assigning socket.")
    sys.exit()

addr = input("Enter server address (leave blank for 'facebook.com'): ")
ct = int(input("Enter number of times to ping ( -1 to send infinitely ): "))

if addr=='':
    addr = 'facebook.com'
    temp = ['facebook','com']
else:
    temp = addr.split('.')

try:
    temp_var = int(temp[-1])
    if len(temp)!=4:
        print("Wrong IPv4 address. IPv6 address not supported.")
        sys.exit()
except:
    addr = socket.gethostbyname("%s"%addr)

def calc_checksum(t,c,i,se,d):
    '''
    Accepts Type, Code, Identifier, Sequence & Data
    and returns checksum in two parts with type integer
    '''
    p = (t*256)+ c + i + se
    
    for i in range(0,len(d),2):
        p = p + ord(d[i])*256
    for i in range(1,len(d),2):
        p = p + ord(d[i])
    
    if p>65535:
        carry = p - 65535
        p = p + carry
    
    p = 65535 - p
    lp = p//256
    hp = p%256
    
    return lp,hp

ec_type = 8
code = 8
identifier = 80
seq = 1
data = 'HELLO'

pl,pr = calc_checksum(ec_type,code,identifier,seq,data)
dlist = list(map(ord,data))
header = [ec_type,code,pl,pr,0,identifier,0,seq]
header = header + dlist
header.append(0)

def send_packet(skt,hd,ip,data):
    '''
    This function sends & receives the packet, prints the required info.
    Also calculates time taken.
    '''
    bh = bytes(hd)
    start_time = time.time()
    skt.send(bh)
    rec = skt.recv(2048)
    end_time = time.time()
    tot_time = (end_time-start_time)*1000
    rec = list(rec)
    ttl = rec[8]
    data_length = len(data)
    if data_length%2==1:
        data_length = data_length+1   # 1 bytes of zeros are padded
    d_size = 8 + data_length
    print("{} bytes of data from {} :".format(d_size,ip),end=' ')
    print("icmp_seq= {0} ttl={1} time={2:0.3f}ms".format(hd[7],ttl,tot_time))

try:
    s.connect(('%s'%addr,8888))
except:
    print("Cannot connect to server.")
    sys.exit()

if ct==-1:
    while (True):
        send_packet(s,header,addr,data)
        seq = seq+1
        header[2],header[3] = calc_checksum(ec_type,code,identifier,seq,data)
        if seq>65535:    #Reset sequence if it is greater than 0xffff
            seq = 1
        elif seq>255:
            header[7] = seq%256
            header[6] = seq//256
        else:
            header[7] = seq
            
else:
    for i in range(1,abs(ct)+1,1):
        seq = i
        if seq>65535:  #Reset sequence if it is greater than 0xffff
            seq = 1
        elif seq>255:
            header[7] = seq%256
            header[6] = seq//256
        else:
            header[7] = seq
            
        header[2],header[3] = calc_checksum(ec_type,code,identifier,seq,data)
        send_packet(s,header,addr,data)

s.close()