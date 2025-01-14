import wx, re, time
from decoding import getMedia, killFirefox

formato= '.jpg'
button = 0
def getTipo():
    global formato
    return formato
def setTipo(tipo):
    global formato
    formato=tipo

#Frame class constructor
class Frame(wx.Frame):
    def __init__(self, parent, title):
        super(Frame, self).__init__(parent, title=title)
        #tipo='jpg'
        self.Panel()
        self.Centre()
        self.SetSize(500,220)

    def Panel(self):

        panel = wx.Panel(self)
        #Setting FONT
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)#font type
        font.SetPointSize(11) #font size
        #Box Sizers
        vbox = wx.BoxSizer(wx.VERTICAL) #Box sizer VERTICAL
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) #Box sizer Horizontal
        #Static Text 1
        st1 = wx.StaticText(panel, label='Insert a URL:') #Static Text Above Field Camp
        st1.SetFont(font) #st1 Font
        hbox1.Add(st1, flag=wx.RIGHT | wx.TOP, border=8)#Inserting ST1 into the FRAME
        #Field 1
        self.field1 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER) #Field for Input
        hbox1.Add(self.field1, proportion=1)#Inserting FIELD1 into the FRAME
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)#Adjusting FRAME

        vbox.Add((-1, 32))# Adjust Vertical Position

        #CheckBoxes Static Text
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Select File Type:')
        st2.SetFont(font)
        hbox2.Add(st2,flag=wx.LEFT, border=8)
        vbox.Add(hbox2, flag=wx.RIGHT, border=10)

        vbox.Add((-1, 10))

        #RadioButtons
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.rb1 = wx.RadioButton(panel, label='Imagem')
        self.rb1.SetFont(font)
        hbox4.Add(self.rb1)
        self.rb2 = wx.RadioButton(panel, label='Video')
        self.rb2.SetFont(font)
        hbox4.Add(self.rb2)
        self.rb3 = wx.RadioButton (panel, label='GIF')
        self.rb3.SetFont(font)
        hbox4.Add(self.rb3, flag=wx.LEFT, border=2)
        vbox.Add(hbox4, flag=wx.LEFT, border=2)

        vbox.Add((-1, 25))

        #Buttons
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Save', size=(70, 30))
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)


        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        #Call vbox Adjustments
        panel.SetSizer(vbox)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, id=btn2.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=btn1.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.FileType)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSave)


    #CloseButton Event
    def OnCloseWindow(self, event):
        dial = wx.MessageDialog(None, 'Close the program?', 'Exit',
        wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        resp = dial.ShowModal()
        if resp == wx.ID_YES:
            self.Destroy()
            killFirefox()
        else:
            event.Skip()
    
    #RadioButton Event
    def FileType(self, event):
        state1 = self.rb1.GetValue()
        state2 = self.rb2.GetValue()
        state3 = self.rb3.GetValue()
        if (state2 == True):
            self.tipo='.mp4'
        elif (state3 == True):
            self.tipo= 'gif'
        else:
            self.tipo='.jpg'
        setTipo(self.tipo)
    #Save to PC Message
    def MessageSave(self):
        wx.MessageBox('File saved on your computer!', '',
        wx.OK | wx.ICON_INFORMATION)
    #Open URL Message
    def MessageBrowser(self):
        wx.MessageBox('The link was opened on your browser!', '',
        wx.OK | wx.ICON_INFORMATION)
    #Wait MessageBox
    def Aguarde(self):
        wx.MessageBox('This can take up to 1 minute', 'Please stand by',
        wx.OK | wx.ICON_INFORMATION)

    def MessageErro(self):
        wx.MessageBox('Error. Try again!', '',
        wx.OK | wx.ICON_INFORMATION)

    def MessageAuth(self):
        wx.MessageBox("Couldn't Login to Instagram", 'Erro de Autenticação',
        wx.OK | wx.ICON_INFORMATION)

    def MessageM4s(self):
        wx.MessageBox('Unsupported video format. Try another.', 'Error',
        wx.OK | wx.ICON_INFORMATION)



    #Save Button
    def OnSave(self, event):
        global button
        self.tipo = getTipo()
        self.url = self.field1.GetValue()
        self.stories = re.search('https://www.instagram.com/stories', self.url)
        self.posts = re.search('https://www.instagram.com/p', self.url)
        self.twt = re.search('https://twitter.com/', self.url)
        if (self.posts != None):
            dlg = wx.MessageDialog(None, 'Would you like to save to your pc?', 'Save or Open in Browser?',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            resp = dlg.ShowModal()
            if resp == wx.ID_YES:
                self.Aguarde()
                self.response='Computador'                     
                time.sleep(1)
                if(getMedia(self.url, self.tipo, self.response, self.posts, button) == True):    
                    self.MessageSave()
                    button += 1
                else:
                    self.MessageErro()

            else:
                dlg2 = wx.MessageDialog(None, 'Would you like to open in your browser?', '',
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                resp = dlg2.ShowModal()
                if resp == wx.ID_YES:
                    self.Aguarde()
                    self.response='Navegador'
                    time.sleep(1)
                    if(getMedia(self.url, self.tipo, self.response, self.posts, button) == True):    
                        self.MessageSave()
                        button += 1
                    else:
                        self.MessageErro()

                    

                else:
                    event.Skip()
        elif (self.stories != None):
            dlg = wx.MessageDialog(None, 'Would you like to save to your pc?', 'Save or Open in Browser?',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            resp = dlg.ShowModal()
            if resp == wx.ID_YES:
                self.Aguarde()
                self.response='Computador'
                time.sleep(1)
                if(getMedia(self.url, self.tipo, self.response, self.posts, button) == True):    
                    self.MessageSave()
                    button += 1
                else:
                    self.MessageErro()

            else:
                dlg2 = wx.MessageDialog(None, 'Would you like to open in your browser?', '',
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                resp = dlg2.ShowModal()
                if resp == wx.ID_YES:
                    self.Aguarde()
                    self.response='Navegador'
                    time.sleep(1)
                    if(getMedia(self.url, self.tipo, self.response, self.posts, button) == True):    
                        self.MessageSave()
                        button += 1
                    else:
                        self.MessageErro()
                else:
                    event.Skip()
        
        elif (self.twt != None):
            dlg = wx.MessageDialog(None, 'Would you like to save to your pc?', 'Save or Open in Browser',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            resp = dlg.ShowModal()
            if resp == wx.ID_YES:
                self.Aguarde()
                self.response='Computador'
                time.sleep(1)
                if(getMedia(self.url, self.tipo, self.response, self.twt, button) == True):
                    self.MessageSave()
                elif (getMedia(self.url, self.tipo, self.response, self.twt, button) == False):
                    self.MessageM4s()
                else:
                    self.MessageErro()

            else:
                dlg2 = wx.MessageDialog(None, 'Would you like to open in your browser?', '',
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                resp = dlg2.ShowModal()
                if resp == wx.ID_YES:
                    self.Aguarde()
                    self.response='Navegador'
                    if(getMedia(self.url, self.tipo, self.response, self.twt, button) == True):
                        self.MessageSave()
                    else:
                        self.MessageErro()

        else:
            dlg3 = wx.MessageBox('Please insert a link', '',
            wx.OK | wx.ICON_INFORMATION)
            event.Skip()


def main():

    app = wx.App()
    dlg = Frame(None, title='Media Saver')
    dlg.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
