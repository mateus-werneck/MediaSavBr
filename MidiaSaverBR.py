import wx, re, time, os
from decoding import getMedia, killFirefox
from threading import *

formato='.jpg'
button = 0
EVT_RESULT_ID = wx.NewId()
ID_START = wx.NewId()
url=''

def getTipo():
    global formato
    return formato

def setTipo(tipo):
    global formato
    formato=tipo
######################################################Thread Class##########################################################################################
def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.start()
    #Open URL Message
    def MessageBrowser(self):
        wx.MessageBox('O link foi aberto no seu navegador!', '',
        wx.OK | wx.ICON_INFORMATION)
    #Wait MessageBox
    def Aguarde(self):
        wx.MessageBox('Isso pode demorar até 1 minuto.', 'Aguarde um instante',
        wx.OK | wx.ICON_INFORMATION)

    def MessageErro(self):
        wx.MessageBox('Erro, tente novamente.', '',
        wx.OK | wx.ICON_INFORMATION)

    def MessageM4s(self):
        wx.MessageBox('Formato de video inválido tente outro.', 'Erro',
        wx.OK | wx.ICON_INFORMATION)

    def run(self):
        global button
        global url
        self.tipo = getTipo()
        self.url = url
        self.stories = re.search('https://www.instagram.com/stories', self.url)
        self.posts = re.search('https://www.instagram.com/p', self.url)
        self.twt = re.search('https://twitter.com/', self.url)

########################################################## Instagram Posts ##################################################################################        
        if (self.posts != None):
            dlg = wx.MessageDialog(None, 'Deseja salvar no seu computador?', '',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            resp = dlg.ShowModal()
            if resp == wx.ID_YES:
                self.Aguarde()
                self.response='Computador'
                time.sleep(1)
                if(getMedia(self.url, self.tipo, self.response, self.posts, button) == True):    
                    button += 1
            else:
                dlg2 = wx.MessageDialog(None, 'Deseja abrir no seu navegador?', 'Salvar ou Abrir No Navegador',
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                resp = dlg2.ShowModal()
                if resp == wx.ID_YES:
                    self.Aguarde()
                    self.response='Navegador'
                    time.sleep(1)
                    if(getMedia(self.url, self.tipo, self.response, self.posts, button) == True):  
                        button += 1
                else:
                    event.Skip()
########################################################## Instagram Stories ##################################################################################        
        elif (self.stories != None):
            dlg = wx.MessageDialog(None, 'Deseja salvar no seu computador?', 'Salvar ou Abrir No Navegador',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            resp = dlg.ShowModal()
            if resp == wx.ID_YES:
                self.Aguarde()
                self.response='Computador'
                time.sleep(1)
                if(getMedia(self.url, self.tipo, self.response, self.stories, button) == True): 
                    button += 1
            else:
                dlg2 = wx.MessageDialog(None, 'Deseja abrir no seu navegador?', '',
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                resp = dlg2.ShowModal()
                if resp == wx.ID_YES:
                    self.Aguarde()
                    self.response='Navegador'
                    time.sleep(1)
                    if(getMedia(self.url, self.tipo, self.response, self.stories, button) == True):
                        button += 1
                else:
                    event.Skip()
########################################################## Twitter Media ##################################################################################         
        elif (self.twt != None):
            dlg = wx.MessageDialog(None, 'Deseja salvar no seu computador?', 'Salvar ou Abrir No Navegador',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            resp = dlg.ShowModal()
            if resp == wx.ID_YES:
                self.Aguarde()
                self.response='Computador'
                time.sleep(1) 
                getMedia(self.url, self.tipo, self.response, self.twt, button)
            
            else:
                dlg2 = wx.MessageDialog(None, 'Deseja abrir no seu navegador?', '',
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                resp = dlg2.ShowModal()
                if resp == wx.ID_YES:
                    self.Aguarde()
                    self.response='Navegador'
                    time.sleep(1)
                    getMedia(self.url, self.tipo, self.response, self.twt, button) 
        
        
        if self._want_abort:
            wx.PostEvent(self._notify_window, ResultEvent(None))
            return
        wx.PostEvent(self._notify_window, ResultEvent(True))

    def abort(self):
        """abort worker thread."""
        self._want_abort = 1            

########################################################################################################################
#Frame class constructor
class Frame(wx.Frame):
    def __init__(self, parent, title):
        super(Frame, self).__init__(parent, title=title)
        self.Panel()
        self.Centre()
        self.SetSize(500,220)
        
###########################################################################################################################
#Panel
    def Panel(self):

        panel = wx.Panel(self)
        #Setting FONT
        
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)#font type
        font.SetPointSize(11) #font size
        #Box Sizers
        vbox = wx.BoxSizer(wx.VERTICAL) #Box sizer VERTICAL
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) #Box sizer Horizontal
        #Static Text 1
        st1 = wx.StaticText(panel, label='Insira Um Link: ') #Static Text Above Field Camp
        st1.SetFont(font) #st1 Font
        hbox1.Add(st1, flag=wx.RIGHT | wx.TOP, border=8)#Inserting ST1 into the FRAME
        #Field 1
        self.field1 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER) #Field for Input
        hbox1.Add(self.field1, proportion=1)#Inserting FIELD1 into the FRAME
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)#Adjusting FRAME

        vbox.Add((-1, 32))# Adjust Vertical Position
############################################################################################################################
        #CheckBoxes Static Text
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Escolha o Tipo do Arquivo:')
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
        btn1 = wx.Button(panel, ID_START, label='Salvar', size=(90, 90))
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Fechar', size=(90, 90))
        hbox5.Add(btn2)


        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=5)
#########################################################################################################################################
        #Adjustments
        panel.SetSizer(vbox)


        self.CreateStatusBar()
        
        self.worker = None
        
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=ID_START)
        
        EVT_RESULT(self,self.OnResult)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, id=btn2.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=ID_START)
        self.Bind(wx.EVT_RADIOBUTTON, self.FileType)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSave)

###################################################################################################
#Events    
    
    #CloseButton Event
    def OnCloseWindow(self, event):
        dial = wx.MessageDialog(None, 'Deseja sair?', 'Sair',
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
    
    #Save Button
    def OnSave(self, event):
      global url
      url = self.field1.GetValue()
      if (url == ''):
        dlg3 = wx.MessageBox('Voce não inseriu um link', '',
                            wx.OK | wx.ICON_INFORMATION)
        event.Skip()
      else:    
        if not self.worker:
            self.worker = WorkerThread(self)
            self.SetStatusText('Salvando seu link...')  
       
    #On getMedia() result
    def OnResult(self, event):
        """Show Result status."""
        if event.data is None:
            self.SetStatusText('Operação cancelada.')
        elif event.data is False:
            self.MessageM4s()
        else:
            self.SetStatusText('Arquivo salvo com sucesso.')
            self.MessageSave()
        self.worker = None   

     #Save to PC Message
    def MessageSave(self):
        wx.MessageBox('Arquivo salvo com sucesso!', 'Finalizado',
        wx.OK | wx.ICON_INFORMATION)  


def main():

    app = wx.App()
    dlg = Frame(None, title='Midia Save')
    dlg.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
