'''
Created on Apr 12, 2013

@author: kite
'''
import libvirt
import time
import vm_instance
from physical_host import PhysicalHost

# Got to do for all hypervisors simultaneously

class HypervisorInfo:
    def __init__(self, URIs, hostnames):
        self.conns = []
        self.hosts = []
        for i in xrange(len(URIs)):
            self.conns.append(libvirt.open(URIs[i]))
            self.hosts.append(PhysicalHost(hostnames[i]))
        
        
    def getDomainStats(self, period):
        host_cpuTimeStart = []
        host_cpuTimeEnd = []
        host_totalMemory = []
        host_stats = []
        host_memory = []
        host_domains = []
        
        for conn in self.conns:
            domainsIDs_ = conn.listDomainsID()
            domains = []
            for domID in domainsIDs_:
                domains.append(conn.lookupByID(domID))
            host_domains.append(domains)
        
        for domains in host_domains:    #get cpuTime for all the domains on each host
            cpuTimeStart = []
            for dom_ in domains:
                stat = dom_.getCPUStats(1,0)[0]
                cpuTimeStart.append(stat['cpu_time'])
            host_cpuTimeStart.append(cpuTimeStart)
        
        time.sleep(period)  #now sleep a little
        
        for domains in host_domains:    #get cpuTime for all the domains on each host
            cpuTimeEnd = []
            for dom_ in domains:
                stat = dom_.getCPUStats(1,0)[0]
                cpuTimeEnd.append(stat['cpu_time'])
            host_cpuTimeEnd.append(cpuTimeEnd)
        
        for conn in self.conns:     #get totalMemeory amount for each hosts
            host_totalMemory.append(conn.getMemoryStats(-1, 0)['total'] - conn.getMemoryStats(-1, 0)['buffers']\
            - conn.getMemoryStats(-1, 0)['cached'])
        
        
        for domains in host_domains:    #get memory stats for all the domains on each host
            memory = []
            for dom_ in domains:
                memory.append(dom_.memoryStats()['rss'])
            host_memory.append(memory)
            
    
        for i in xrange(len(host_domains)):
            stats = []
            for j in xrange(len(host_cpuTimeStart[i])):
                time_ = (host_cpuTimeEnd[i][j] - host_cpuTimeStart[i][j])*(10**(-9))
                memory_ = float(host_memory[i][j])/host_totalMemory[i]
                stats.append( dict(id=host_domains[i][j].ID(), time=time_,
                             load_cpu = (time_/period)*100, memory = float(host_memory[i][j])/1024, 
                             load_mem = memory_*100) )
            host_stats.append(stats)
            
#        for i in xrange(len(cpuTimeStart)):
#            time_ = (cpuTimeEnd[i] - cpuTimeStart[i])*(10**(-9))
#            memory_ = float(memory[i])/totalMemory
#            stats.append( dict(id=domains[i].ID(), time=time_,
#                             load_cpu = (time_/period)*100, memory = float(memory[i])/1024, 
#                             load_mem = memory_*100) )
        for i in xrange(len(host_stats)):
            for j in xrange(len(host_stats[i])):
                vm = vm_instance.VMInstance('custom', 'vm'+str(host_stats[i][j]['id']))
                vm.cpu_usage = host_stats[i][j]['load_cpu']
                vm.mem_usage = host_stats[i][j]['load_mem']
                self.hosts[i].run_vm(vm)
            
        return host_stats
    
    def showVMs(self):
        for host in self.hosts:
            host.show_host_props()