#!/usr/bin/python

import wx
import os
import sys

class TestFrame(wx.Frame):
  def __init__(self):
    self.cwd = os.path.dirname(os.environ['_'])
    self.fileDB = []
    self.result = []
    wx.Frame.__init__(self, None, -1, "Searcher")
    sizer = wx.GridBagSizer(hgap=5, vgap=3)
    #self.tc = wx.TextCtrl(self, -1, "", pos=(40, 10))
    self.tc = wx.TextCtrl(self, -1, "", size=(300, 10))
    sizer.Add(self.tc, pos=(0,0), span=(1,1), flag=wx.EXPAND)

    fb = wx.Button(self, label='find')
    sizer.Add(fb, pos=(0,1))
    fb.Bind(wx.EVT_BUTTON, self.OnFind)
    
    #sampleList = ['0', '1', '2', '3', '4']
    #listBox = wx.ListBox(self, -1, (20, 20), (80, 120), sampleList, wx.LB_SINGLE)
    self.list = wx.ListCtrl(self, -1, size=(350,250), style=wx.LC_REPORT)
    self.list.InsertColumn(0, 'file')
    self.list.InsertColumn(1, 'contents')
    self.list.SetColumnWidth(0,70)
    self.list.SetColumnWidth(1,200)
    #self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
    sizer.Add(self.list, pos=(1,0), span=(1,2), flag=wx.EXPAND)

    sizer.AddGrowableCol(0)
    sizer.AddGrowableRow(1)
    
    self.SetSizer(sizer)
    self.Fit()

    toolbar = self.CreateToolBar()
    bmp = wx.Image(os.path.join(self.cwd, 'open.bmp'), wx.BITMAP_TYPE_BMP).ConvertToBitmap()
    tool = toolbar.AddSimpleTool(-1, bmp, 'open', '')
    self.Bind(wx.EVT_MENU, self.OnOpen, tool)
	
    self.sb = self.CreateStatusBar()
    self.sb.SetStatusText('Search file is need!')

  def OnOpen(self, evt):
    dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
      #print dialog.GetPath()
      self.root = dialog.GetPath()
      self.SetTitle('Searcher: ' + self.root)    
      self.StructFileDB()
      #print self.fileDB
      self.sb.SetStatusText('Search files are %d'% len(self.fileDB))
    dialog.Destroy()

  def StructFileDB(self):
    self.fileDB = []
    self.travel_forgyp(self.root)

  def travel_forgyp(self, repath):
    if '.nogyp' in os.listdir(repath):
      return

    dirs = []
    for f in os.listdir(repath):
      cpath = os.path.join(repath, f)
      if os.path.islink(cpath):
        continue
      if os.path.isdir(cpath):
        if f != '.git' and f != '.svn':
          dirs.append(f)
      elif os.path.isfile(cpath):
        if f.endswith('.gyp') or f.endswith('.gypi'):
           self.fileDB.append(cpath)

    for d in dirs:
      self.travel_forgyp(os.path.join(repath, d))

  
  def OnFind(self, evt):
    self.result = []
    self.list.DeleteAllItems()
    key = self.tc.GetValue()
    i = 0
    
    for fname in self.fileDB:
      #print '::' +fname
      f = open(fname)
      try:
        for line in f:
          if line.find(key) > -1:
            tmp = (fname.replace(self.root + '/', ''), line)
            self.result.append(tmp)
            index = self.list.InsertStringItem(sys.maxint, tmp[0])
            self.list.SetStringItem(index, 1, tmp[1])
      except UnicodeDecodeError:
        pass
      i=i+1
      self.sb.SetStatusText(str(i))
    #print self.result

#  def OnItemSelected(self, evt):
#    item = evt.GetItem()
    #print "Item Selected:", item.GetText()

  def OnItemActivated(self, evt):
    item = evt.GetItem()
    #print "Item Activated:", item.GetText()
    if os.fork() == 0:
      dirname = os.path.dirname(os.environ['_'])
      os.execl(os.path.join(dirname, 'gyp_view.py'), 'gyp_view.py', os.path.join(self.root, item.GetText()))


app = wx.PySimpleApp()
TestFrame().Show()

app.MainLoop()
