#!/usr/bin/env python
#
# simulate train checking desk queue module
# - if passed, gone
# - if failed, queue at last again
# - if the person is older than 60, he can queue in tail but bypass 10 person at most.
#   - but can't bypass person order than him.
#
# auther: cyliu7@gmail.com
# date: 2018/2/8
#

import os
import sys
import mutex
import random
import time 
from threading import Thread
from threading import Lock

class Person(object):
    def __init__(self, age, sp=True):
        self.age = age
        self.flag = False
        # demo
        self.should_pass = sp

class QueueNode(object):
    def __init__(self, person, prev, next):
        self.p = person
        self.prev = prev 
        self.next = next

class CheckDeskQueue(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self._lock = Lock()

    def push(self, person):
        n = QueueNode(person, None, None)
        self._lock.acquire()

        # empty queue
        if self.head == None:
            self.head = n
            self.tail = n
            self._lock.release()
            return

        # can use bypass only once
        if person.flag or person.age < 60:
            self.tail.next = n
            n.prev = self.tail
            self.tail = n
            self._lock.release()
            return

        # for older than 60
        maxbypass = 10
        bypassnum = 0
        cur = self.tail
        while cur:
            if bypassnum >= 10:
                break

            if cur.p.age >= person.age:
                break
          
            cur = cur.prev
            bypassnum += 1

        if cur:
            if cur.next:
                n.next = cur.next
                cur.next.prev = n
            cur.next = n
            n.prev = cur
        else:
            n.next = self.head
            self.head.prev = n
            self.head = n
        n.p.flag = True
        self._lock.release()


    def pop(self):
        p = None
        self._lock.acquire()
        if self.head:
            p = self.head.p
            self.head = self.head.next
            if self.head:
                self.head.prev = None

        self._lock.release()
        return p


    def listQ(self):
        l = []
        cur = self.head
        while cur:
            l.append(cur.p.age)
            cur = cur.next
        return l
        
class CheckDesk(object):

    def __init__(self):
        self.q = CheckDeskQueue()

    def inQueue(self, person):
        p = Person(person)
        self.q.push(p)

    def check(self):
        """
           return (Person, checking_pass_or_not)
        """
        p = self.q.pop()
        if not p:
            return (None, None)

        passed = True
        # do the checking logic here
        #
        if not p.should_pass:
            self.q.push(p)
            return (p, False)
        else:
            return (p, True)
            #print 'go %s' % p.age
        
        pass

SAMPLE1 = [10, 20, 22, 47, 89, 76, 33, 8, 15, 23, 46, 55, 22, 44,65, 60, 61 , 33, 22]
EXPECT1 = [89, 76, 10, 20, 65, 60, 61, 22, 47, 33, 8, 15, 23, 46, 55, 22, 44, 33, 22]
def utest():
    checkdesk = CheckDesk()
    il = SAMPLE1
    for i in il:
        checkdesk.inQueue(i)
        print '%s in' % i

    ol = checkdesk.q.listQ()
    ils = ','.join([str(i) for i in il])
    ols = ','.join([str(i) for i in ol])
    els = ','.join([str(i) for i in EXPECT1])
    print ils
    print ols
    print els
    assert (ols == els) == True

class GateKeeper(Thread):
    def __init__(self, checkdesk):
        Thread.__init__(self)
        self.checkdesk = checkdesk

    def run(self):
        plist = SAMPLE1
        for i in plist:
            self.checkdesk.inQueue(i)
            print '%s in' % i
            time.sleep(1)

class CheckGate(Thread):
    def __init__(self, checkdesk):
        Thread.__init__(self)
        self.checkdesk = checkdesk

    def run(self):
        p,ret = self.checkdesk.check()
        while p:
            if ret:
                print '      %s go' % p.age
            else:
                print '      %s requeue' % p.age

            time.sleep(random.randint(1, 3))
            p,ret = self.checkdesk.check()


if __name__ == '__main__':

    #unit test
    utest()

    #threading test
    cd = CheckDesk()
    gk = GateKeeper(cd)
    cg = CheckGate(cd)

    gk.start()
    cg.start()
    time.sleep(120)
