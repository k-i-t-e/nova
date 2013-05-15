'''
Created on Apr 12, 2013

@author: kite
'''
import libvirt

conn = libvirt.open("qemu:///system")
conn2 = libvirt.open("qemu+ssh://root@195.208.117.184/system")

print conn.getType()
print conn2.getType()