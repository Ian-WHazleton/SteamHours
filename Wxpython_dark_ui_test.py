import wx

class PriceBreakdownFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wxPython Styled Box", size=(600, 400))
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#2b2b2b")
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Price Breakdown")
        title.SetForegroundColour("white")
        title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        vbox.Add(title, flag=wx.ALL, border=10)

        summary = wx.StaticText(panel, label="Total Cost: $99.99 | Games: 5")
        summary.SetForegroundColour("white")
        summary.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        vbox.Add(summary, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)

        box = wx.TextCtrl(panel, value="Game Name                Bundle Cost   Steam Price   Bundle %\n"
                                       "----------------------------------------------------------\n"
                                       "Example Game 1           $10.00        $20.00        10.0%\n"
                                       "Example Game 2           $20.00        $30.00        20.0%\n",
                          style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.SetBackgroundColour("#404040")
        box.SetForegroundColour("white")
        box.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        vbox.Add(box, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)

        btn = wx.Button(panel, label="Proceed with These Prices")
        btn.SetBackgroundColour("#4CAF50")
        btn.SetForegroundColour("white")
        btn.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        vbox.Add(btn, flag=wx.ALL|wx.ALIGN_RIGHT, border=10)

        panel.SetSizer(vbox)

app = wx.App(False)
frame = PriceBreakdownFrame()
frame.Show()
app.MainLoop()