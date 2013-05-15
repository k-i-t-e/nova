'''
Created on Mar 12, 2013

@author: kite
'''

# import repr
import operator
# import placement_exeptions
from placement_exeptions import NoHostsLeftExeption
from vm_instance import VMInstance
from physical_host import PhysicalHost
import random
from random import seed, choice
from copy import deepcopy
import math
        

class ScheduldingAlgorithm:

    def __init__(self):
        self.VMs = []
        
        self.hosts = []
    

    def show_hosts(self):
        for host in self.hosts:
            host.show_host_props()
        print ''


    def show_vms(self):
        for vm in self.VMs:
            vm.show_props()

    def show(self):
        self.show_vms()
        self.show_hosts()
    
    def first_fit_descending(self):
        print 'Running FFD placement algorithm'
        # sorted_cpu = sorted(self.VMs, key = lambda vm: vm.cpu_usage)
        sorted_cpu = sorted(self.VMs, key=operator.attrgetter('cpu_usage'), reverse=True)
        sorted_mem = sorted(self.VMs, key=operator.attrgetter('mem_usage'), reverse=True)
#        sorted_hdd = sorted(self.VMs, key=operator.attrgetter('hdd_usage'), reverse=True)
        
        sorted_list = [sorted_cpu, sorted_mem]
        
        
        for sort in sorted_list:
            print sort
        
        
        vm_cnt = 0  # VM counter
        host_cnt = 0  # host counter
        for sort in sorted_list:
            while vm_cnt < len(sort):
                print 'Using list ' + str(sort)
                if sort[vm_cnt].host == '':
                    while True:
                        if self.hosts[host_cnt].run_vm(sort[vm_cnt]):
                            break
                        else:
                            if host_cnt < len(self.hosts):
                                host_cnt += 1
                            else:
                                raise NoHostsLeftExeption
                                
                    vm_cnt = 0
                    break
                else:
                    vm_cnt += 1
                
    
    def first_fit(self, vm):
        print 'Running a first fit algorithm to place vm ' + vm.vm_name
        host_cnt = 0
        while host_cnt < len(self.hosts):
            if self.hosts[host_cnt].run_vm(vm):
                break
            else:
                if host_cnt < len(self.hosts):
                    host_cnt += 1
                else:
                    raise NoHostsLeftExeption
        
        return self.hosts[host_cnt]
    
    def add_vm(self, vm):
        self.VMs.append(vm)
        self.first_fit(vm)
        
    def cost_func(self, hosts):
        cost = 0
        for host in hosts:
            if host.running:
                cost += 1
        return cost
    
    def root_mean_sqr(self, hosts):
        cost_cpu = 0
        cost_mem = 0
#        cost_hdd = 0
        for host in hosts:
            cost_cpu += math.pow((host.cpu_cap - host.cpu_available), 2)
            cost_mem += math.pow((host.mem_cap - host.mem_available), 2)
#            cost_hdd += math.pow((host.hdd_cap - host.hdd_available), 2)
        cost_cpu = math.sqrt(cost_cpu/len(hosts))
        cost_mem = math.sqrt(cost_mem/len(hosts))
#        cost_hdd = math.sqrt(cost_hdd/len(hosts))
        
        cost = (cost_cpu + cost_mem)/3
        return cost
    
    
    def simulated_annealing(self):
        k = 1.3806488 * (10**(-23))
        print 'Running Simulated Annealing algoritm'
        temp = 1000
        no_changes_iterations = 0
        old_delta = 0
        result_iter = 0
        for i in xrange(100):
            result_iter = i
            temp_hosts = deepcopy(self.hosts)
            seed()
            host1 = choice(temp_hosts)
            seed()
            host2 = choice(temp_hosts)
            seed()
            try:
                vm = choice(host1.assigned_vms)
            except IndexError:
                continue
                
            host1.migrate(vm, host2)
            delta = self.cost_func(self.hosts) - self.cost_func(temp_hosts)
            if delta>=0:
                self.hosts = temp_hosts
                    #no_changes_iterations = 0
            else: 
                if k*temp>0:
                    r = random.random()
                    # some debug information
                    print '///Debug stuff///'
                    print i
                    print delta
                    print math.exp(delta/temp)
                    #print math.exp(-(delta/temp)) 
                    print temp
                    print r
                    print '/////////////////'
                    if math.exp(delta/temp) > r:
                        self.hosts = temp_hosts
                    else:
                        no_changes_iterations = 0
                        
            temp *= 0.7
            if delta == old_delta:
                no_changes_iterations += 1
                #break #optionally
            else:
                no_changes_iterations = 0 
            if no_changes_iterations>2:
                break
            old_delta = delta
            self.show_hosts()
        return result_iter   
    
    
    def simulated_annealing_abstract(self, cost_function):
        k = 1.3806488 * (10**(-23))
        print 'Running Simulated Annealing algoritm'
        temp = 1000
        no_changes_iterations = 0
        old_delta = 0
        result_iter = 0
        for i in xrange(100):
            result_iter = i
            temp_hosts = deepcopy(self.hosts)
            seed()
            host1 = choice(temp_hosts)
            seed()
            host2 = choice(temp_hosts)
            seed()
            try:
                vm = choice(host1.assigned_vms)
            except IndexError:
                continue
                
            host1.migrate(vm, host2)
            delta = cost_function(self.hosts) - cost_function(temp_hosts)
            if delta>=0:
                self.hosts = temp_hosts
                    #no_changes_iterations = 0
            else: 
                if k*temp>0:
                    r = random.random()
                    # some debug information
                    print '///Debug stuff///'
                    print i
                    print delta
                    print math.exp(delta/temp)
                    #print math.exp(-(delta/temp)) 
                    print temp
                    print r
                    print '/////////////////'
                    if math.exp(delta/temp) > r:
                        self.hosts = temp_hosts
                    else:
                        no_changes_iterations = 0
                        
            temp *= 0.7
            if delta == old_delta:
                no_changes_iterations += 1
                #break #optionally
            else:
                no_changes_iterations = 0 
            if no_changes_iterations>2:
                break
            old_delta = delta
            self.show_hosts()
        return result_iter   