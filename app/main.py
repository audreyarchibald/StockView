#!/usr/bin/env python

import wx, os, sys
from app.GUI.home_tab import HomeTab as dt
LIGHT_GREEN = '#000000'
VERSION_STR = "2023-09-20"
NUM_OF_HISTORY = 20

class GUI(wx.Frame):
    def __init__(self):
        super().__init__(None)
        panel = wx.Panel(self)
        panel.SetBackgroundColour(LIGHT_GREEN)
        self.panel = panel

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        nb = wx.Notebook(panel)
        if 1:
            tabs = []
            tabs.append((dt(nb), 'Data')) 
        for tab, name in tabs:
            nb.AddPage(tab, name)
        sizer.Add(nb, 1, wx.EXPAND)
        panel.SetSizer(sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Maximize()
        self.Layout() #forces EVT_SIZE
        self.Fit()   #shrink/expand the frame to just fit the contents
        self.Refresh()  #causes this frame and its children to repaint
        self.SetIcon(wx.Icon("app/icon.ico"))


if __name__ == '__main__':
    app = wx.App()
    frame = GUI()
    frame.Show()
    app.MainLoop()