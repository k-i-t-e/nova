'''
Created on Mar 28, 2013

@author: kite
'''
import libvirt
import sys
import time


#conn = libvirt.openReadOnly("qemu:///system")
conn = libvirt.open("qemu:///system")
#conn = libvirt.openReadOnly("qemu://195.208.117.178/system")
if conn == None:
    print 'Failed to open connection to hypervisor'
    sys.exit(1)

hypervisor_type = conn.getType()
print "hypervisor type = "+hypervisor_type


info = conn.getInfo()
print "Info:"
print info

print "cell free memory = "
memory = conn.getCellsFreeMemory(0, 1)
print "%d" %(memory[0])

print "CPU Stats:"
print conn.getCPUStats(1, 0)

# -1 for all cells statistic
mem_stat = conn.getMemoryStats(-1, 0)
print "Memory stats:"
print mem_stat

#print "Sys Info:"
#print conn.getSysinfo(0)

#this gets list of domains IDs
#print "Domain IDs"
#domainsIDs = conn.listDomainsID()
#print domainsIDs


#print "Memory stats for Dom number 0"
#dom0_mem_stats = dom.memoryStats()
#print dom0_mem_stats
##print "for domain number 1:"
##print dom2.memoryStats()
#
#print "Max memory:"
#print dom.maxMemory()
#
#print "Max VCPUS"
#print dom.maxVcpus()
#dom.vcpuPinInfo(0)

#print "Domain state:"
#print dom.state(0)


#domains = []
#for domID in domainsIDs:
#    domains.append(conn.lookupByID(domID))
#    #print domains[len(domains)-1].info
#
#for dom_ in domains:
#    print dom_.info()
    
#print dom.getCPUStats(0,0)  #This gets stats for all cpus of a domain (this method is missing in my library
                            # but, however, exists on the server)
#print dom.getCPUStats(1,0)  #This gets total stats for a domain

#print domains[0].ID()
#print domains[0].getCPUStats(0,0)
#print "%f" %(domains[0].getCPUStats(1,0)[0]['cpu_time']*(10**(-9))) #convert from nanosec to sec

print "Now let's try to guess how much CPU time does the domain consume:"
#cpuTimeStart = []
#cpuTimeEnd = []
#stats = []
#memory = []
#period = 10
#totalMemory = conn.getMemoryStats(-1, 0)['total'] - conn.getMemoryStats(-1, 0)['buffers']\
#    - conn.getMemoryStats(-1, 0)['cached']
#for dom_ in domains:
#    stat = dom_.getCPUStats(1,0)[0]
#    cpuTimeStart.append(stat['cpu_time'])
#
#time.sleep(period)
#for dom_ in domains:
#    stat = dom_.getCPUStats(1,0)[0]
#    cpuTimeEnd.append(stat['cpu_time'])
#    memory.append(dom_.memoryStats()['rss'])
#
#for i in xrange(len(cpuTimeStart)):
#    time_ = (cpuTimeEnd[i] - cpuTimeStart[i])*(10**(-9))
#    memory_ = float(memory[i])/totalMemory
#    stats.append( dict(id=domains[i].ID(), time=time_,
#                         load_cpu = (time_/period)*100, memory = float(memory[i])/1024, load_mem = memory_*100) )
#    #stats.append((cpuTimeEnd[i] - cpuTimeStart[i])*(10**(-9)))
#    print str(domains[i].ID())+'\t'+str(time_)
#
#
#print stats



def getDomainStats(period, conn_):
    cpuTimeStart = []
    cpuTimeEnd = []
    stats = []
    memory = []
    domains = []
    
    domainsIDs_ = conn_.listDomainsID()
    
    for domID in domainsIDs_:
        domains.append(conn_.lookupByID(domID))
    
    totalMemory = conn_.getMemoryStats(-1, 0)['total'] - conn_.getMemoryStats(-1, 0)['buffers']\
        - conn_.getMemoryStats(-1, 0)['cached']
    
    for dom_ in domains:
        stat = dom_.getCPUStats(1,0)[0]
        cpuTimeStart.append(stat['cpu_time'])
    
    time.sleep(period)
    
    for dom_ in domains:
        stat = dom_.getCPUStats(1,0)[0]
        cpuTimeEnd.append(stat['cpu_time'])
        memory.append(dom_.memoryStats()['rss'])

    for i in xrange(len(cpuTimeStart)):
        time_ = (cpuTimeEnd[i] - cpuTimeStart[i])*(10**(-9))
        memory_ = float(memory[i])/totalMemory
        stats.append( dict(id=domains[i].ID(), time=time_,
                         load_cpu = (time_/period)*100, memory = float(memory[i])/1024, 
                         load_mem = memory_*100) )
        
    return stats


print getDomainStats(10, conn)