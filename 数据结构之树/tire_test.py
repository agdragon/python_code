#!/usr/bin/python   
#coding=utf-8

'''
http://my.oschina.net/u/158589/blog/61037

Trie 的原理和实现

'''
 
class Node:
    def __init__(self):
        self.value = None
        self.children = {}    # children is of type {char, Node}                                                                                                       
 
class Trie:
    def __init__(self):
        self.root = Node()
 
    def insert(self, key):      # key is of type string                                                                                                                
        # key should be a low-case string, this must be checked here!                                                                                                  
        node = self.root
        for char in key:
            if char not in node.children:
                print char
                child = Node()
                node.children[char] = child
                node = child
            else:
                print char
                node = node.children[char]
        node.value = key
        

    def search(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            else:
                node = node.children[char]
        return node.value
 
    def display_node(self, node):
        if (node.value != None):
            print node.value
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char in node.children:
                self.display_node(node.children[char])
        return
 
    def display(self):
        self.display_node(self.root)

if __name__ == '__main__':
    print '================ A Trie Demo =============='
    trie = Trie()
    print "*" * 20
    trie.insert('hello world')

    print "\n"

    trie.insert('hello')
    
    # print trie.search('hello')
    # trie.display()
    print '================= END ====================='