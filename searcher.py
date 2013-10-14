#!/usr/bin/python

import wx
import os

labels = "1 2 3 4 5 6 7 8 9 0".split()

class TestFrame(wx.Frame):
    def __init__(self):
        self.cwd = os.path.dirname(os.environ['_'])
        self.fileDB = []
        wx.Frame.__init__(self, None, -1, "Searcher")
        sizer = wx.GridBagSizer(hgap=5, vgap=3)
        
        self.tc = wx.TextCtrl(self, -1, "", pos=(40, 10))
        sizer.Add(self.tc, pos=(0,0), span=(1,1), flag=wx.EXPAND)

        fb = wx.Button(self, label='find')
        sizer.Add(fb, pos=(0,1))
        fb.Bind(wx.EVT_BUTTON, self.OnFind)
        
        sampleList = ['0', '1', '2', '3', '4']
        listBox = wx.ListBox(self, -1, (20, 20), (80, 120), sampleList, wx.LB_SINGLE)
        sizer.Add(listBox, pos=(1,0), span=(1,2), flag=wx.EXPAND)

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

    def OnOpen(self, event):
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            #print dialog.GetPath()
            for root, dirs, files in os.walk(dialog.GetPath()):
                for f in files:
                    if f.endswith('.gyp') or f.endswith('.gypi'):
                        self.fileDB.append(os.path.join(root, f))
            #print self.fileDB
            self.sb.SetStatusText('Search files are %d'% len(self.fileDB))
            
        dialog.Destroy()

    def OnFind(self, event):
        key = self.tc.GetValue()
        i = 0
        for fname in self.fileDB:
            #print '::' +fname
            f = open(fname)
            try:
                for line in f:
                    if line.find(key) > -1:
                        #print ':' + line
                        pass
            except UnicodeDecodeError:
                print '::' +fname
                print line
                #return
            i=i+1
            self.sb.SetStatusText(str(i))
app = wx.PySimpleApp()
TestFrame().Show()

app.MainLoop()
