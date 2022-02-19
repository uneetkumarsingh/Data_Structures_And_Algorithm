import os
import sys
from mylist import *
from collections import namedtuple

class myvm_bad_state_change(Exception):
    def __init__(self, vm, newstate, message="Active VMs are present"):
        self.vm=vm
        self.newstate=newstate
        self.message=message
    def __str__(self):
        return f'{self.vm.vm} oldstate: {self.oldstate} newstate: {newstate} bound to: {self.sr} -> {self.message}'


# This object implements the relevant operations/sate for the workings described
# in the mycrm object above. It will maintain the stats in the stats object sent
# in the init. Do not change the signature of the init class. You can add any
# more members you want other than what is listed.

# states:
#
# 'idle' :  not bound to any server. Happens when a server has failed. need to be
# reprovisioned only via mycrm.provision_all_idle_vms() or
# mycrm.provision_idle_vms(server) function. the idle vm being bound to a server
# does not go through the same provision, commit, undo etc. it is an internally
# managed operation by the mycrm.
#
# 'provision': in this state it is bound to a server, but not fully committed.
# It is a simple transition state until a commit or undo happens. undo deletes
# this vm, commit moves the vm to active state.
#
# 'active' : bound to a  server . happens when a commit is called on a
# provisioned 'vm' or when an idle vm is bound again to a server. 
# 'idle' --> active OR 'provision' --> active 
#
# 'deleted' : finally deleted but object will cease to exist after this.
# deprovision_vm will trigger this.

class myvm():

    # DO NOT change the init signature.
    # DO not change the members here. You are welcome to add more. But the
    # members described here has to be maintained, including the stats otherwise
    # Else all tests will fail and it wont be graded.
    # self.vc -->  a vconf immutable tuple that stores name, cpu and mem of this
    # vm.
    # self.amem, and self.acpu --> will be same as vc.mem and vc.ncpu and it
    # wont change during the life of this object for this assignment.
    # self.sr --> stores the bound server object.
    # self.stats--> where all the book keeping happens,. Have to be done
    # correctly.
    # self.state can be 'provision', 'idle', 'active'    when it is 'deleted'
    # the object will cease to exist.

    def __init__(self,vc,sr,stats):
        self.vc=vc
        self.name = vc.name
        self.amem=vc.mem
        self.acpu=vc.ncpu
        self.state="provision"
        self.sr=sr
        self.stats=stats
        self.stats['vprovision'] +=1#why starting with provision state?
        self.stats['vtotal'] += 1
        # your code any other member you want.
        #YOUR CODE

    # called during commit  by myserver object.
    # Set the vm state to active and do the accounting if 
    # the conditions for transiting to active state is met.
    # raise exceptions otherwise.
    # a vm can move to 'active' state from 'provision' state or 'idle' state.
    # do the book keeping on the self.stats right way.
    # self.sr should be set to sr to indicate it is bounded.

    def set_active(self, sr):
        if(self.state == "provision" or self.state == "idle"):
            if(self.state == "idle"):
                self.stats["vidle"]-=1
            else:
                self.stats["vprovision"] -=1
            self.state = "active"
            self.stats["vactive"]+=1
            self.sr = sr
        #YOUR CODE
        #raise NotImplementedError

    #  called by myserver when it goes to fail state.
    #  unbound the server by setting self.sr = None.
    #  vm can move to idle state only from 'active' state.
    #  do the book keeping in self.stats

    def set_idle(self, sr):
        if(self.state == "active"):
            self.state = "idle"
            self.stats["vactive"]-=1
            self.stats["vidle"] +=1
            self.sr = None

        #YOUR CODE
        #raise NotImplementedError

    # called by mycrm.delete_vm() routine to delete
    # this vm OR by mycrm.provision_undo() routine after deprovisioning it
    # from server OR if it was already 'idle'.
    # hence vm state can be 'active' or 'provision' or 'idle' state and when 
    #  deleted the object is "deleted" state.after which there should not be 
    # any references any where and no one can refer to it.

    def delete(self, sr):
        #master vm stack is managed in the mycrm class
        sr.vl.delete(self.vc.name)
        sr.amem+=self.vc.mem
        sr.acpu+=self.vc.ncpu
        sr.nvms-=1
        if(self.state == "active"):
            self.state = "deleted"
            self.stats["vactive"] -= 1
            self.stats["vdeleted"] += 1
            self.stats["vtotal"] -= 1
        elif(self.state == "idle"):
            self.state = "deleted"
            self.stats["vidle"] -= 1
            self.stats["vdeleted"] += 1
            self.stats["vtotal"] -= 1
        elif(self.state == "provision"):
            self.state = "deleted"
            self.stats["vprovision"] -= 1
            self.stats["vdeleted"] += 1
            self.stats["vtotal"] -= 1
        if(sr.state == "active" and sr.nvms == 0):
            self.sr.state = "idle"
            self.sr.stats["sidle"]+=1
            self.sr.stats["sactive"]-=1
        self.sr = None

        #YOUR CODE
        #raise NotImplementedError
