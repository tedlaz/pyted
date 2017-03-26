# -*- coding: utf-8 -*-
'''
Created on Jan 15, 2012

@author: tedlaz
'''
import wx
import os

def mkpng(arxeio):
    str = './images/%s' % arxeio
    img_path = os.path.abspath(str)
    icon   = wx.Icon(img_path,type=wx.BITMAP_TYPE_PNG)
    return icon
class MyFrame(wx.Frame):
    def __init__(self,parent, id=wx.ID_ANY,title='',
                 pos=wx.DefaultPosition,size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 name='MyFrame'):
        super(MyFrame,self).__init__(parent,id,title,pos,size,style,name)
        
        self.panel = wx.Panel(self)
        self.SetIcon(mkpng('add.png'))
        ok_btn = wx.Button(self.panel,wx.ID_OK)
class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None,title=u'Δοκιμή')
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()