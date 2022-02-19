import os
import sys

# as discussed in the class and subsequent discussions 
# have an ADT for this and you can use this to create
# whatever you want.
# you are welcome to implement this in a way you want and use it.
# I am giving you a template where a single linked list
# can be used for multiple objects .. 
# to share code as much as possible in a single ADT.
# l1 = mylist(list) --> behaves like a list
# l2 = mylist(stack) --> supports stack and other operations(like push, pop
# etc.)  are disallowed.
# l3 = mylist(queue) --> same here. (like enqueue, dequeue etc.)

# you are welcome to use your own ADT whatever way.

class myelem():
    def __init__(self, obj):
        self.next=self
        self.prev=self
        self.obj=obj # this is equivalent to data

class mylist():
    list_type=['stack', 'list', 'queue']

    # init function do not change this.

    def __init__(self, type):
        self.header=myelem(self)
        self.size=0
        if type not in self.list_type:
            raise Exception("List type incorrect")
        self.type=type
        self.tail=self.header
        self.current = self.header
    # cmp function is sent some time for users of
    # the lookup to return the right object. See usage
    # below. See same_
    # see comment in mycrm.py above server_same and vm_same.. functions.
    # the cmp method is used if it is not None to check for object
    # equality. 
    # for each element in list:
    #        if (cmp(val, element) is true:
    # return object

    def lookup(self, val, cmp=None):
        if cmp == None:
            e = self.header.next
            h = self.header
            while e != h:
                if (e.obj == val):
                    return e.obj
                e = e.next
            return None
        else:
            e = self.header.next
            h = self.header
            while e != h:
                if (cmp(e.obj,val)):
                    return e.obj
                e = e.next
            return None
        #YOUR CODE
        #raise NotImplementedError
    
    # returns true if list is not empty
    # if it is empty, returns False.

    def not_empty(self):
        if(self.size != 0):
            return True
        else:
            return False
        #YOUR CODE
        #raise NotImplementedError

    #  returns first element

    def first(self):
        return self.header.next.obj
        #YOUR CODE
        #raise NotImplementedError

    # returns last element

    def last(self):
        return self.tail.prev.obj
        #YOUR CODE
        #raise NotImplementedError

    # adds the element to 
    def add(self, obj):
        if(myl.type == "list"):
            e = myelem(obj)
            e.next = self.header.next
            e.prev = self.header
            self.header.next.prev = e
            self.header.next = e
            self.size+=1
            if(self.size==1):
                self.tail = e
        else:
            raise Exception("add supported only on list")
            #YOUR CODE
        #raise NotImplementedError

    def push(self, obj): # Pushing at the front
        if(self.type == "stack"):
            e = myelem(obj)
            e.next = self.header.next
            e.prev = self.header
            self.header.next.prev = e
            self.header.next = e
            self.size+=1
            if(self.size == 1):
                 self.tail = e
        else:
            raise Exception("Push supported only by stack")
    
    def pop(self):#popping from the front/header
        if(self.type == "stack"):
            if(self.size!=0):
                ans = self.header.next.obj
                self.header.next.next.prev = self.header
                self.header.next = self.header.next.next
                self.size-=1
                if(self.size == 0):
                    self.tail = self.header
                return ans
            else:
                return None
                #raise Exception("Cannot pop from empty stack")
        else:
            raise Exception("pop only for stack")
        #YOUR CODE
        #raise NotImplementedError

    def peek(self):
        if(self.type == "stack"):
            if(self.size!=0):
                return self.header.next.obj
            else:
                return None
                #raise Exception("Cannot peek from empty stack")
        else:
            raise Exception("mypeek only for stack")

    def enqueue(self, obj): #enqueues at the end/tail
        if(self.type == "queue"):
            e = myelem(obj)
            e.next = self.header
            e.prev = self.header.prev
            self.header.prev.next = e
            self.header.prev = e
            self.size+=1
            self.tail = e
        else:
            raise Exception("Enqueue supported only for queue")
        #YOUR CODE
        #raise NotImplementedError

    def dequeue(self): #dequeues from the head
        if(self.type == "queue"):
            if(self.size!=0):
                ans = self.header.next.obj
                self.header.next.next.prev = self.header
                self.header.next = self.header.next.next
                self.size-=1
                if(self.size == 0):
                    self.tail = self.header
                return ans
            else:
                return None
            #raise Exception("Cannot dequeue from empty queue")
        else:
            raise Exception("Dequeue only for queue")
        #YOUR CODE
        #raise NotImplementedError
   
   # works for all of the three types.

    def delete(self, obj):
        e = self.header.next
        h = self.header
        ans = None
        while e != h:
           if (e.obj == obj):
                ans = e
                if(self.tail == e):#if last element is deleted, tail needs to be shifted
                    self.tail = e.prev
                break
           e = e.next
        if(ans!=None):
            ans.next.prev = ans.prev
            ans.prev.next = ans.next
            self.size-=1
            if(self.size == 0):
                self.tail = self.header

    def deleteall(self):
        self.header.next = self.header
        self.header.prev = self.header
        self.tail = self.header
        self.size = 0    
        
    # iterator objects for all.

    def __iter__(self):
        self.current = self.header.next
        return self
        #YOUR CODE
        #raise NotImplementedError

    def __next__(self):
        if(self.current == self.header):
            raise StopIteration
        x = self.current.obj
        self.current = self.current.next
        return x
        #YOUR CODE
        #raise NotImplementedError

    def __str__(self):
        s=''
        h=self.header
        e=self.header.next
        s=f'List size: {self.size}'
        s += '\n'
        while e != h:
            s += f'{e.obj}'
            if (e.next != h):
                s += '\n'
            e = e.next
        s += '\n'
#       if e.prev != self.tail:
#            s += f'tail corrupt: tail: {self.tail.obj} list tail: {e.prev.obj}'

        if self.tail != self.header:
            s += f'Tail: {self.tail.obj}'
        s += '\n'
        return s
       

def main():
    x = mylist("stack")
    x.push(1)
    x.push(2)
    x.push(4)
    for i in x:
        print(i)
        if(i == 2):
            break
    print("faulty")
    for i in x:
        print(i)
    for i in x:
        print(i)

if __name__ == "__main__":
    main()
