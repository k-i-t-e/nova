'''
Created on Mar 13, 2013

@author: kite
'''
class VMInstance:
    def __init__(self, vm_type, vm_name):
        self.vm_type = vm_type
        self.vm_name = vm_name
        self.host = ''
        vm_types_cpu = {'computing':30, 'web-server':10}
        vm_types_mem = {'computing':30, 'web-server':20}
#        vm_types_hdd = {'computing':10, 'web-server':30}
            
            
        for type in vm_types_cpu:
            if type == vm_type:
                self.cpu_usage = vm_types_cpu[type]
            
        for type in vm_types_mem:
            if type == vm_type:
                self.mem_usage = vm_types_mem[type]
            
#        for type in vm_types_hdd:
#            if type == vm_type:
#                self.hdd_usage = vm_types_hdd[type]
            
    def show_props(self):
        print 'VM ' + self.vm_name + ' is a ' + self.vm_type + ' VM'
        print 'cpu_usage = ' + str(self.cpu_usage) + '%'
        print 'mem_usage = ' + str(self.mem_usage) + '%'
#        print 'hdd_usage = ' + str(self.hdd_usage) + '%\n'
        
    def __repr__(self):
        return self.vm_name
        # return strself.cpu_usage, self.mem_usage, self.hdd_usage
    def __str__(self):
        return self.vm_name