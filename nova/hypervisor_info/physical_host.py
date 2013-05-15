'''
Created on Mar 13, 2013

@author: kite
'''
import libvirt
class PhysicalHost:
    def __init__(self, host_name):
        # Model fields
        self.host_name = host_name
        self.cpu_cap = 100
        self.mem_cap = 100
#        self.hdd_cap = 100
        self.running = False
        self.cpu_available = self.cpu_cap
        self.mem_available = self.mem_cap
#        self.hdd_available = self.hdd_cap
        self.assigned_vms = []
        
        # Real host fields
#        self.conn = libvirt.open(URI)
#        self.cpuTimeStart = []
#        self.cpuTimeEnd = []
#        self.stats = []
#        self.memory = []
#        self.domains = []
#        self.totalMemory = 0
        
    def can_run_vm(self, vm):
        if self.cpu_available - vm.cpu_usage >= 0 and self.mem_available - vm.mem_usage >= 0: #and self.hdd_available - vm.hdd_usage >= 0
            return True
        else:
            return False
    
    def run_vm(self, vm):
        if self.can_run_vm(vm):
            self.running = True
            self.cpu_available -= vm.cpu_usage
            self.mem_available -= vm.mem_usage
#            self.hdd_available -= vm.hdd_usage
            self.assigned_vms.append(vm)
            vm.host = self.host_name
            #print 'VM ' + vm.vm_name + ' running on host ' + self.host_name
            return True
        else:
            return False
    
    def stop_vm(self, vm):
        if vm in self.assigned_vms:
            self.assigned_vms.remove(vm)
            self.cpu_available += vm.cpu_usage
            self.mem_available += vm.mem_usage
#            self.hdd_available += vm.hdd_usage
            vm.host = ''
            if len(self.assigned_vms) == 0:
                self.running = False
            return True
        else: 
            return False
            
    def migrate(self, vm, to):
        #print 'Trying migration from ' + self.host_name + ' to ' + to.host_name
        if to == self:
            return
        if not to.run_vm(vm):
            print 'Destination host unable to run VM'
            return False
        
        if not self.stop_vm(vm):
            print 'Error while stopping VM'
            return False
        #print 'Migration completed successfully'
        return True
    
    def show_host_props(self):
        print 'Host ' + self.host_name + ' has resources available:\n\
cpu: ' + str(self.cpu_available) + '%\n\
mem: ' + str(self.mem_available) + '%\n\
and has VMs currently running:\n'\
        + str(self.assigned_vms)