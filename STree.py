#!/usr/bin/env python
#
#
#  method to check whether a Tree is SearchTree
#
# auther: cyliu7@gmail.com
# date: 2018/2/8
#

import os
import sys

class BTNode(object):
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right
        pass

######
# search tree is ordered tree. left-middle-right travel the tree, and
# test if all value are ordered.
seq = []
def isValidBT(node):
    # make a seqencial list
    global seq
    seq = []
    travelBT(node)
    for i in range(len(seq)-1):
            if seq[i] >= seq[i+1]:
                return False
    return True


def travelBT(node):
    global seq
    if node.left:
        travelBT(node.left)

    seq.append(node.value)

    if node.right:
        travelBT(node.right)

def test1():
    n5 = BTNode(5, None, None)
    n6 = BTNode(6, None, None)
    n20 = BTNode(20, None, None)
    n15 = BTNode(15, n6, n20)
    n10 = BTNode(10, n5, n15)

    #bst = BTree(n10)
    #bst.seqBTree()
    #assert bst.isSTree() == False
    assert isValidBT(n10) == False
    global seq
    print seq

def test2():
    n6 = BTNode(6, None, None)
    n5 = BTNode(5, None, n6)
    n20 = BTNode(20, None, None)
    n15 = BTNode(15, None, n20)
    n10 = BTNode(10, n5, n15)
    assert isValidBT(n10) == True
    global seq
    print seq


#######################
# for a search tree, all the node in its left tree shoud in a range(MIN, current node value).
# and all the node in its right tree shoud in range (current node value, MAX).
# recersively checking whether subtree is in valid range.
MAXINT = sys.maxint
MININT = -sys.maxint-1
def isValidBT2(node):
    if not node:
        return True

    return travelBT2(node, MININT, MAXINT)

def travelBT2(node, minv, maxv):
    if not node:
        return True

    if node.value <= minv or node.value >= maxv:
        return False

    return travelBT2(node.left, minv, node.value) and \
            travelBT2(node.right, node.value, maxv)

def test3():
    n5 = BTNode(5, None, None)
    n6 = BTNode(6, None, None)
    n20 = BTNode(20, None, None)
    n15 = BTNode(15, n6, n20)
    n10 = BTNode(10, n5, n15)
    assert isValidBT2(n10) == False

def test4():
    n6 = BTNode(6, None, None)
    n5 = BTNode(5, None, n6)
    n20 = BTNode(20, None, None)
    n15 = BTNode(15, None, n20)
    n10 = BTNode(10, n5, n15)
    assert isValidBT2(n10) == True

if __name__ == '__main__':
    # construct the test Tree
    test1()
    test2()
    test3()
    test4()

