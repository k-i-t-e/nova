'''
Created on Apr 12, 2013

@author: kite
'''

import hypervisor_info
import MySQLdb as mdb
from algorithm import ScheduldingAlgorithm

#URIs = ["qemu:///system", "qemu+ssh://root@195.208.117.184/system"]
#URIs = ["qemu:///system", "qemu+ssh://npc10.stu.neva.ru/system"] #works!
URIs = ["qemu+ssh://npc11.stu.neva.ru/system", "qemu+ssh://npc10.stu.neva.ru/system"] #works
hostnames = ['npc11', 'npc10']

#npc11 = hypervisor_info.HypervisorInfo("qemu:///system", 'npc11')
#npc10 = hypervisor_info.HypervisorInfo("qemu+ssh://root@195.208.117.184/system", 'npc10')

cloud = hypervisor_info.HypervisorInfo(URIs, hostnames)

print cloud.getDomainStats(60) 
cloud.showVMs()

try:
    con = mdb.connect('localhost', 'root', 'cl0udAdmin', 'nova')
except mdb.Error, e:
    print "Error in connecting to database"
else:
    try:
        cur = con.cursor()
        cur.execute("select hypervisor_hostname from compute_nodes")
        hosts = cur.fetchall()
        for host in hosts:
            print host[0]
    except:
        print "Error in executing query"

#print npc11.getDomainStats(10)
#npc11.showVMs()
#
#print npc10.getDomainStats(10)
#npc10.showVMs()
#
#test = ScheduldingAlgorithm()
#
#test.VMs = []
#test.VMs.extend(npc10.host.assigned_vms)
#test.VMs.extend(npc11.host.assigned_vms)
#test.hosts = [npc10.host, npc11.host]
#
#test.show()
#
#i = test.simulated_annealing_abstract(test.root_mean_sqr)
#
#test.show_hosts()
#print 'made '+str(i)+' iterations'