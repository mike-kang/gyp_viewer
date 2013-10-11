#!/usr/bin/python

import wx
import os
import sys
import re
 
class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=sys.argv[1], size=(400,500))
 
        # Create the tree
        self.tree = wx.TreeCtrl(self)
        self.tree.SetWindowStyle(wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        # Add a root node
        root = self.tree.AddRoot("GYP")
        if not os.access(sys.argv[1], os.F_OK):
            dlg = wx.MessageDialog(None, 'File is not exist!',
                                   'MessageDialog', wx.OK).ShowModal()
            self.Close() 
        #f = file('/home/san/project/chromium/src/build/all.gyp')
        f = file(sys.argv[1])
        s = f.read()
        data = eval(s)
        #print data
        self.AddTreeNodes(root, data)
 
        # Bind some interesting events
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.tree)
 
        # Expand the first level
        self.tree.Expand(root)
 
 
    def AddTreeNodes(self, parentItem, items):
        """
        Recursively traverses the data structure, adding tree nodes to
        match it.
        """
        if len(items) == 0:
            return False
             
        bFind = False
        bExt = False        
        if type(items) == dict:
            for key in items.keys():
                #print key     
                keyNode = self.tree.AppendItem(parentItem, key)
                val = items[key]
                if type(val) == str:
                    valNode = self.tree.AppendItem(keyNode, val)
                    if key == 'target_name':
                        self.tree.SetItemTextColour(valNode, wx.Colour(255,0,0))
                        self.tree.Expand(keyNode)
                        bFind = True
                elif type(val) == int:
                    valNode = self.tree.AppendItem(keyNode, str(val))
                elif type(val) == dict or type(val) == list:
                    bExt = self.AddTreeNodes(keyNode, val)
                    if bExt:
                        self.tree.Expand(keyNode)

                    
        elif type(items) == list:
            for i in range(len(items)):
                val = items[i]
                if type(val) == str:
                    self.tree.AppendItem(parentItem, val)
                elif type(val) == int:
                    self.tree.AppendItem(parentItem, str(val))
                else:
                    idxNode = self.tree.AppendItem(parentItem, str(i))
                    bExt = self.AddTreeNodes(idxNode, val)
                    if bExt:
                        self.tree.Expand(idxNode)
        return (bExt or bFind)        
    
    def SearchItem(self, item, val, items):
        """ 
        item : start node 
        val : key string
        items : result list
        """
        return items
                 
    def GetItemText(self, item):
        if item:
            return self.tree.GetItemText(item)
        else:
            return ""
         
    def OnItemExpanded(self, evt):
        print "OnItemExpanded: ", self.GetItemText(evt.GetItem())
         
    def OnItemCollapsed(self, evt):
        print "OnItemCollapsed:", self.GetItemText(evt.GetItem())
 
    def OnSelChanged(self, evt):
        print "OnSelChanged:   ", self.GetItemText(evt.GetItem())
 
    def OnActivated(self, evt):
        print "OnActivated:    ", self.GetItemText(evt.GetItem())
 
 
#app = wx.PySimpleApp(redirect=True)
app = wx.PySimpleApp()
frame = TestFrame()
frame.Show()
app.MainLoop()


