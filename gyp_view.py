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
    #self.tree.SetWindowStyle(wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)
    self.tree.SetWindowStyle(wx.TR_HAS_BUTTONS)
    
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
    f = file(self.gypfile)
    s = f.read()
    data = eval(s)
    # Add a root node
    self.root = self.tree.AddRoot(os.path.basename(self.gypfile))
    #print data
    self.AddTreeNodes(self.root, data)
    self.tree.Expand(self.root)
 
  def AddTreeNodes(self, parentItem, lod):
    """
    Recursively traverses the data structure, adding tree nodes to
    match it.
    lod is list or dict.
    """
    if len(lod) == 0:
      return False
       
    bFind = False
    bExt = False    
    if type(lod) == dict:
      for key in lod.keys():
        #print key   
        keyNode = self.tree.AppendItem(parentItem, key)
        val = lod[key]
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

          
    elif type(lod) == list:
      for i in range(len(lod)):
        val = lod[i]
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
 
  def SearchTreeNodes(self, parentItem, val):
    item, cookie = self.tree.GetFirstChild(parentItem)
    while item:
      #print self.tree.GetItemText(item)
      if re.search(val, self.tree.GetItemText(item)):
        self.ShowItem(item, wx.Colour(0,0,255))
      if self.tree.ItemHasChildren(item):
        self.SearchTreeNodes(item, val)
      item, cookie = self.tree.GetNextChild(parentItem, cookie)

  def ShowItem(self, item, color):
    self.tree.SetItemTextColour(item, color)
    while True:
      parent = self.tree.GetItemParent(item)
      if parent:
        self.tree.Expand(parent)
        item = parent
      else:
        break
    
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
    path = self.GetItemText(evt.GetItem())
    print "OnActivated:  ", path
    dirname = os.path.dirname(self.gypfile)
    if path.endswith('.gyp') or path.endswith('.gypi'): 
      if os.fork() == 0:
        execution = os.path.join(os.path.dirname(os.environ['_']), 'gyp_view.py')
        os.execl(execution, "gyp_view.py", os.path.join(dirname, path)) 
    elif path.endswith('.grd'):
      subprocess.Popen(['gnome-terminal','-x', 'sh', '-c', 'vim '+ os.path.join(dirname, path)])
 
  def OnSearch(self, event):
    dlg = wx.TextEntryDialog(None, "Search string with Regular Expression...",
                   'Search', '');
    if dlg.ShowModal() == wx.ID_OK:
      self.SearchTreeNodes(self.tree.GetSelection(), dlg.GetValue())
 
  def OnVi(self, event):
    print 'vi'
    #if os.fork() == 0:
    #  os.execl('/usr/bin/gedit',"gedit", self.gypfile) 
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


