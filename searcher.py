#!/usr/bin/python

import wx

labels = "1 2 3 4 5 6 7 8 9 0".split()

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Searcher")
        sizer = wx.GridBagSizer(hgap=5, vgap=3)
        
        self.posCtrl = wx.TextCtrl(self, -1, "", pos=(40, 10))
        sizer.Add(self.posCtrl, pos=(0,0), span=(1,1), flag=wx.EXPAND)

        bw = wx.Button(self, label='find')
        sizer.Add(bw, pos=(0,1))
        
        sampleList = ['0', '1', '2', '3', '4']
        listBox = wx.ListBox(self, -1, (20, 20), (80, 120), sampleList, wx.LB_SINGLE)
        sizer.Add(listBox, pos=(1,0), span=(1,2), flag=wx.EXPAND)

        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(1)
        
        self.SetSizer(sizer)
        self.Fit()
        

app = wx.PySimpleApp()
TestFrame().Show()

app.MainLoop()
