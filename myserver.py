import os
import sys
from mylist import *
from collections import namedtuple

class myserver_activevms(Exception):
    def __init__(self, server, message="Active VMs are present"):
        self.server=server
        self.message=message
    def __str__(self):
        return f'{self.server} -> {self.message}'

class myserver_bad_state_change(Exception):
    def __init__(self, server, newstate, message="Active VMs are present"):
        self.server=server
        self.newstate=newstate
        self.message=message
    def __str__(self):
        return f'{self.server.sr} oldstate: {self.state} newstate: {newstate} vmsactive: {self.nvms} -> {self.message}'

# This object implements the relevant operations/sate for the workings described
# in the mycrm object above. It will maintain the stats in the stats object sent
# in the init. Do not change the signature of the init class. You can add any
# more members you want other than what is listed.

# states:
# 'idle' : ready to accept vm's and can have vms in 'provision' state bound to
# it.
# 'active' : ready to accept vm's and should have atleast one vm in 'active'
# state and other vms can be in either 'active' or in 'provision' state.
#
# 'fail' : can be failed and go to this state if there are no vms bound to it.
#
# 'deleted' : finally deleted but object will cease to exist after this.

class myserver():

    # DO NOT change the init signature.
    # DO not change the members here. You are welcome to add more. But the
    # members described here has to be maintained, including the stats otherwise
    # Else all tests will fail and it wont be graded.

    # self.sc -- sconf named tuple sent as part of creation. just contains the
    # immutable name, ncpu and memory of this server.
    # self.amem -- store the remaining available memory after whatever vms have
    # been provisioned to this. 
    # self.acpu -- store the remaining available cpus after whatever has been
    # self.nvms -- no. of vms that are bound to this, which could be in
    # 'provision' state or in 'active' state.
    # taken by the vms provisioned to this. 
    # [[ for eg., if server has 4 cpus, and 4G memory and two vms each took 1
    # cpu and 1G for itself, then then self.acpu=2,self.amem=2
    # self.state -- will be 'idle', 'active', or 'fail'. as explained below.
    # do the proper state transitions modify this and also do the accounting.
    # use whatever list data structures you need to accomplish this project.

    def __init__(self,sc, stats):
        self.sc=sc #sconf named tupple sent as part of add method
        self.amem=sc.mem
        self.acpu=sc.ncpu
        self.state='idle'
        self.nvms=0
        self.vl=mylist("stack")
        self.vd={}
        self.stats=stats #This is crm_stat named tuple
        self.stats['sidle'] += 1
        self.stats['stotal'] += 1
        # your code any other member if you want.
        # YOUR CODE
        #raise NotImplementedError

# The following list of functions is just a guideline for you to think through
# the implementation and gain more insight. Except for the get_vms() function
# and the members listed above. 

    # Set the server state to fail and do the accounting if 
    # the conditions for transiting to fail state is met.
    # raise exceptions otherwise.

    def set_fail(self):# Are there any conditions where a server can't fail? 
        self.state = "fail"

    # Set the server state to active and do the accounting if 
    # the conditions for transiting to active state is met.
    # raise exceptions otherwise.

    def set_active(self):
        self.state = "active"

    # check if the server can provision this ie. check if the vconf object vc
    # ncpu, and mem can be allocated by this server given its current self.acpu
    # and self.amem value.
    # return "vc" object if success, else, return None.
    # no state transitions should take place here, as the provisioning
    # process has not commited yet.

    def can_provision(self, vc):
        if(self.amem >= vc.mem and self.acpu >= vc.ncpu):
            return vc
        else:
            return None
        #YOUR CODE
        #raise NotImplementedError

    # provision the vm on this server. vc is the vconf of the vm, 
    # and vm is the myvm object passed by the mycrm object.
    # if the acpu and mem is not sufficient return None.
    # increment the self.nvms 
    # no state transitions happen here, as provisioning process has not
    # been completed it with commit. If an undo happens, whatever you do
    # here will be undone by the mycrm.provision_undo() by calling 
    # myobj.deprovision_vm()

    def provision_vm(self, vc, vm):
        self.vl.push(vc.name)
        self.vd[vc.name] = vm
        self.amem-=vc.mem
        self.acpu-=vc.ncpu
        self.nvms+=1
        #YOUR CODE
        #raise NotImplementedError

    # deprovision the vm on t his server. Recover the mem and cpu given.
    # decrement the self.nvms
    # called by mycrm.deprovision_vm()
    # do the staate transitions.

    def deprovision_vm(self, vm):
        self.vd[vm].delete(self)
        #YOUR CODE
        #raise NotImplementedError

    # commit the provisioning of the vm. at this point do the state
    # transitions and book keeping accordingly and mark the vm as 
    # active, using the vm.set_active() function.
    # raise exception if the vm is not already bound to you. (you will maintain
    # that. 

    def commit_vm(self, vm):
        self.stats["vactive"] +=1
        if(vm.state == "provision"):
            self.stats["vprovision"]-=1
        if(vm.state == "idle"):
            self.stats["vidle"]-=1
        vm.state = "active"
        if(self.state == "idle"):
            self.state = "active"
            self.stats["sidle"]-=1
            self.stats["sactive"]+=1
            
        #YOUR CODE
        #raise NotImplementedError

    # delete the server. raise exceptions if there are vms bound to it, and
    # active or provision vms. 
    # check the state transition requirements and do the state changes and book
    # keeping for the stats.
    # called by the mycrm.delete_server() routine.

    def delete(self):
        try:
            if(self.state!="active"):
                self.stats["sdeleted"] +=1
                self.stats["stotal"] -= 1
                if(self.state == "fail"):
                    self.stats["sfail"]-=1
                else:
                    self.stats["sidle"]-=1
                self.state = "deleted"
            else:
                raise Exception("Active Server cannot be deleted")
        except KeyError:
            raise Exception(f"{name} server doesn't exist")

        #YOUR CODE
        #raise NotImplementedError

    # Fail the server. Move all the bound vms to idle, by calling
    # myvm.set_idle() routine, and recover all the memory and cpu given, and
    # reduce the self.nvms value approopriately. Move the state to 'fail'. and
    # do the right book keeping depending on the initial state which could be
    # 'idle' or 'active'.
    # note that no one will fail a server when there are vms in 'provision'
    # state. A previous provision_vm() operation either has to undo or commit
    # and the vm will go to 'active'(commit) or be deleted (undo)

    def fail(self):
        try:
            if(self.state!="fail"):
                if(self.state == "active"):
                    self.stats["sactive"]-=1
                    for i in self.vl:
                        vm = self.vd[i]
                        if(vm.state == "active"):
                            self.stats["vactive"]-=1
                        if(vm.state == "provision"):
                            self.stats["vprovision"]-=1
                        self.stats["vidle"]+=1
                        vm.state = "idle"
                    #Some code for shifting bound VMs to idle state
                else:
                    self.stats["sidle"]-=1
                self.state = "fail"
                self.stats["sfail"]+=1
        except KeyError:
            raise Exception(f"{name} server doesn't exist")

        #YOUR CODE
        #raise NotImplementedError

    # unfail the server. change the state from 'fail' to 'idle'. Raise exception
    # if the initial state is not 'fail'.

    def unfail(self):
        try:
            if(self.state=="fail"):
                self.amem = self.sc.mem
                self.acpu = self.sc.ncpu
                self.state = "fail"
                self.state = "idle"
                self.nvms = 0
                self.vl.deleteall()
                self.vl = mylist("stack")
                self.vd = {}
                self.stats["sidle"]+=1
                self.stats["sfail"]-=1
        except KeyError:
            raise Exception(f"{name} server doesn't exist")
        
        #YOUR CODE
        #raise NotImplementedError
    
    # This has to be kept as is!! used by test cases and mycrm object.
    # to get the list of vm's bound to this server based on state. state could
    # be 'idle', 'active', and 'provision'.
    # returns the python list, and this should be the only place where python
    # list is used in this file.
    # if state is 'any' returns all.

    def get_vms(self, state):
        if(state == "any"):
            vl = []
            for i in self.vl:
                vl.append(self.vd[i])
            return vl
        elif(state == "idle"):
            vli = []
            for i in self.vl:
                if(self.vd[i].state == "idle"):
                    vli.append(self.vd[i])
            return vli
        elif(state == "active"):
            vla = []
            for i in self.vl:
                if(self.vd[i].state == "active"):
                    vla.append(self.vd[i])
            return vla
        elif(state == "provision"):
            vlp = []
            for i in self.vl:
                if(self.vd[i].state == "provision"):
                    vlp.append(self.vd[i])
            return vlp
        else:
            raise Exception(f"{state} is invalid state")

        #YOUR CODE
        #raise NotImplementedError

