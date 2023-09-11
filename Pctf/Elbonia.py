
from scapy.all import *

p= rdpcap('file.pcapng')

for packet in p :
    dst = packet['UDP'].dport
    character = chr(dst)
    print (character, end='')

    '''
    code is here : MÌPCTF{53cr3t_c0d3_1n_p0rt5}/ 
    {secret_code_in_ports}

    '''
