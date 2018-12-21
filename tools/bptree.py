#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bisect
import queue

class BPNode(object):
    def __init__(self):
        self.keys = list()
        self.values = list()
        self.children = list()
        self.next = None

    def is_leaf(self):
        return not bool(self.children)

    def save_string(self):
        return '|%s|' % ' '.join(['{%s:%s}' % e for e in zip(self.keys, self.values)])

    def __repr__(self):
        return '|%s|' % ' '.join(['{%s:%s}' % e for e in zip(self.keys, self.values)])


class BPTree(object):
    def __init__(self, degree=3):
        # degree为每页出度
        self.degree = degree
        self.root = BPNode()
        self._maxkeys = degree + 1

    def search(self, node, key):
        i = bisect.bisect_left(node.keys, key)
        if i < len(node.keys) and key == node.keys[i]:
            if node.is_leaf():
                return node, i
            else:
                return self.search(node.children[i + 1], key)
        if node.is_leaf():
            return None, None
        else:
            return self.search(node.children[i], key)

    def split_child(self, x, i, y):
        z = BPNode()
        z.keys = y.keys[self.degree:]
        z.values = y.values[self.degree:]
        if not y.is_leaf():
            z.children = y.children[self.degree:]
            y.next = None
        else:
            z.keys.insert(0, y.keys[self.degree - 1])
            z.values.insert(0, y.values[self.degree - 1])
            z.next = y.next
            y.next = z
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[self.degree - 1])
        y.keys = y.keys[:self.degree - 1]
        y.values = y.values[:self.degree - 1]
        y.children = y.children[:self.degree]


    def insert(self, key, value):
        if len(self.root.keys) == self._maxkeys:
            oldroot = self.root
            self.root = BPNode()
            self.root.children.append(oldroot)
            # print(self.root.children)
            self.split_child(self.root, 0, oldroot)
            self.insert_nonfull(self.root, key, value)
        else:
            self.insert_nonfull(self.root, key, value)

    def insert_nonfull(self, curNode, key, value):
        i = bisect.bisect_left(curNode.keys, key)
        # 叶子结点
        if curNode.is_leaf():
            curNode.keys.insert(i, key)
            curNode.values.insert(i, value)
        else:
            if len(curNode.children[i].keys) == self._maxkeys:
                self.split_child(curNode, i, curNode.children[i])
                if key > curNode.keys[i]:
                    i += 1
            self.insert_nonfull(curNode.children[i], key, value)

    def __setitem__(self, k, v):
        self.insert(k, v)

    def __getitem__(self, k):
        node, i = self.search(self.root, k)
        if node:
            return node.values[i]
        else:
            return None

def BPlusTree(path, data, degree=2):
    b = BPTree(degree)
    for k in range(0, len(data)):
        b[k] = data[k]
    n, x = b.search(b.root, 0)
    data = list()
    data.append(n)
    while n.next:
        data.append(n.next)
        n = n.next
    with open(path, 'w') as f:
        for it in data:
            f.write(str(it))



if __name__ == '__main__':
    values = [101, 103, 105, 107, 108]
    kv1 = []
    path1 = r'C:\Users\yl_20\MyFiles\JuniorLastSemester\DBMS\student_sno_data.txt'
    for i in range(0, len(values)):
        t = (i, values[i])
        kv1.append(t)
    print(kv1)
    BPlusTree(path1,kv1)