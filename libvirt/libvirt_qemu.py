#! /usr/bin/python -i
#
# WARNING WARNING WARNING WARNING
#
# This file is automatically written by generator.py. Any changes
# made here will be lost.
#
# To change the manually written methods edit libvirt-qemu-override.py
# To change the automatically written methods edit generator.py
#
# WARNING WARNING WARNING WARNING
#
#
# WARNING WARNING WARNING WARNING
#
# Automatically written part of python bindings for libvirt
#
# WARNING WARNING WARNING WARNING
try:
    import libvirtmod_qemu
except ImportError, lib_e:
    try:
        import cygvirtmod_qemu as libvirtmod_qemu
    except ImportError, cyg_e:
        if str(cyg_e).count("No module named"):
            raise lib_e

import libvirt

#
# Functions from module libvirt-qemu
#

def qemuMonitorCommand(domain, cmd, flags):
    """Send an arbitrary monitor command through qemu monitor of domain """
    ret = libvirtmod_qemu.virDomainQemuMonitorCommand(domain._o, cmd, flags)
    if ret is None: raise libvirt.libvirtError('virDomainQemuMonitorCommand() failed')
    return ret

def qemuAttach(conn, pid, flags):
    """This API is QEMU specific, so it will only work with hypervisor
    connections to the QEMU driver.
    
    This API will attach to an externally launched QEMU process
    identified by @pid. There are several requirements to successfully
    attach to an external QEMU process:
    
      - It must have been started with a monitor socket using the UNIX
        domain socket protocol.
      - No device hotplug/unplug, or other configuration changes can
        have been made via the monitor since it started.
      - The '-name' and '-uuid' arguments should have been set (not
        mandatory, but strongly recommended)
    
    If successful, then the guest will appear in the list of running
    domains for this connection, and other APIs should operate
    normally (provided the above requirements were honored). """
    ret = libvirtmod_qemu.virDomainQemuAttach(conn._o, pid, flags)
    if ret is None: raise libvirt.libvirtError('virDomainQemuAttach() failed')
    __tmp = virDomain(conn,_obj=ret)
    return __tmp

# virDomainQemuMonitorCommandFlags
VIR_DOMAIN_QEMU_MONITOR_COMMAND_DEFAULT = 0
VIR_DOMAIN_QEMU_MONITOR_COMMAND_HMP = 1
