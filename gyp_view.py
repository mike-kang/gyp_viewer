#!/usr/bin/python

import wx
import os
import sys
import re
import subprocess
 
class TestFrame(wx.Frame):
    def __init__(self):
        #print os.environ['_']
        self.cwd = os.path.dirname(os.environ['_']) 
        config = os.path.join(self.cwd, 'gyp_view.ini')
        self.gypfile = os.path.realpath(sys.argv[1])
        t = self.gypfile
        if os.path.exists(config):
            f = file(config)
            s = f.read()
            data = eval(s)
            #print data['depth']
            for p in data['depths']:
                if self.gypfile.find(p,0) == 0:
                    t = self.gypfile.replace(p, '')
                    break
        wx.Frame.__init__(self, None, title=t, size=(400,500))
        #print os.environ['_'] 

        self.toolbarData =  (("Search", "search.bmp", "Search", self.OnSearch),
                ("", "", "", ""),
                ("vi", "open.bmp", "vi", self.OnVi),
                ("Refesh", "refresh.bmp", "Refresh", self.OnRefresh))
        
        self.toolbarColorData =  ("Black", "Red", "Green", "Blue")
#memubar = wx.MenuBar()
        self.createToolBar()

        # Create the tree
        self.tree = wx.TreeCtrl(self)
        self.tree.SetWindowStyle(wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
        
        if not os.access(self.gypfile, os.F_OK):
            dlg = wx.MessageDialog(None, 'File is not exist!',
                                   'MessageDialog', wx.OK).ShowModal()
            self.Close() 
        
        self.drawTree()
 
        # Bind some interesting events
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.tree)
 
        # Expand the first level
        #self.tree.Expand(root)
 
    def drawTree(self):
        #f = file('/home/san/project/chromium/src/build/all.gyp')
        f = file(sys.argv[1])
        s = f.read()
        data = eval(s)
        # Add a root node
        root = self.tree.AddRoot("GYP")
        #print data
        self.AddTreeNodes(root, data)
 
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
        val = self.GetItemText(evt.GetItem())
        print "OnActivated:    ", val
        so = re.match('.*\.gypi?', val)
        if so: 
            if os.fork() == 0:
                dirname = os.path.dirname(self.gypfile)
                os.execl(os.environ['_'],"gyp_view.py", os.path.join(dirname, so.group())) 

    def OnSearch(self, event): pass
    def OnVi(self, event):
        print 'vi'
        #if os.fork() == 0:
        #    os.execl('/usr/bin/gedit',"gedit", self.gypfile) 
        subprocess.Popen(['gnome-terminal','-x', 'sh', '-c', 'vim '+ self.gypfile])

    def OnRefresh(self, event):
        self.tree.DeleteAllItems()
        self.drawTree()

    def createToolBar(self):
        toolbar = self.CreateToolBar()
        for each in self.toolbarData:
            self.createSimpleTool(toolbar, *each)
        toolbar.AddSeparator()
        for each in self.toolbarColorData:
            self.createColorTool(toolbar, each)
        toolbar.Realize()

    def createSimpleTool(self, toolbar, label, filename, help, handler):
        if not label:
            toolbar.AddSeparator()
            return
        bmp = wx.Image(os.path.join(self.cwd, filename), wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        tool = toolbar.AddSimpleTool(-1, bmp, label, help)
        self.Bind(wx.EVT_MENU, handler, tool) 

    def createColorTool(self, toolbar, color):
        bmp = self.MakeBitmap(color)
        tool = toolbar.AddSimpleTool(-1, bmp, color)
        #self.Bind(wx.EVT_MENU, self.OnColor, tool)

    def MakeBitmap(self, color):
        bmp = wx.EmptyBitmap(16, 15)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(color))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        return bmp

    def toolbarColorData(self):
        return ("Black", "Red", "Green", "Blue")


#app = wx.PySimpleApp(redirect=True)
app = wx.PySimpleApp()
frame = TestFrame()
frame.Show()
app.MainLoop()


