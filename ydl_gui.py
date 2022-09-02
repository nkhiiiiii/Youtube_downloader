from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.clock import Clock
from yt_dlp import YoutubeDL
import os
from kivy.lang import Builder
import threading


Builder.load_string("""
<MainScreen>:
    canvas.before:
        Color:
            rgba: 0.191,0.245,0.245,1
        Rectangle:
            pos: self.pos
            size: self.size

    
    BoxLayout:
        orientation: 'vertical'
        size: root.size


        BoxLayout:
            orientation: 'vertical'
            Label:
                id: labelUrlHeader
                text: 'URL Input'

            BoxLayout:
                orientation: 'horizontal'
                TextInput:
                    id: tiUrl
                    size_hint: 0.9, 0.8
                    text: ''
                    on_text_validate: root.enterClickedUrl()
                    multiline: False

                Button:
                    id: tiButton
                    size_hint: 0.1, 0.8
                    text: 'Save'
                    on_press: root.pressSaveUrl()

                Button:
                    id: tcButton
                    size_hint: 0.1, 0.8
                    text: 'Clear'
                    on_press: root.pressClearUrl()

        Label:
            id: labelUrl
            text: 'Default'
            text_size: self.size
            halign: 'left'
            valign: 'top'




        BoxLayout:
            orientation: 'vertical'
            Label:
                id: labelFilenameHeader
                text: 'Filename Input'

            BoxLayout:
                orientation: 'horizontal'
                TextInput:
                    id: tiFilename
                    size_hint: 0.9, 0.8
                    text: ''
                    on_text_validate: root.enterClickedFilename()
                    multiline: False                    

                Button:
                    id: tiButton
                    size_hint: 0.1, 0.8
                    text: 'Save'
                    on_press: root.pressSaveFilename()

                Button:
                    id: tcButton
                    size_hint: 0.1, 0.8
                    text: 'Clear'
                    on_press: root.pressClearFilename()

        Label:
            id: labelFilename
            text: 'Default'
            text_size: self.size
            halign: 'left'
            valign: 'top'



        BoxLayout:
            orientation: 'vertical'
            Label:
                id: labelPathHeader
                text: 'Path Input'

            BoxLayout:
                orientation: 'horizontal'
                TextInput:
                    id: tiPath
                    size_hint: 0.9, 0.8
                    text: ''
                    on_text_validate: root.enterClickedPath()
                    multiline: False

                Button:
                    id: tiButton
                    size_hint: 0.1, 0.8
                    text: 'Save'
                    on_press: root.pressSavePath()

                Button:
                    id: tcButton
                    size_hint: 0.1, 0.8
                    text: 'Clear'
                    on_press: root.pressClearPath()


        Label:
            id: labelPath
            text: 'Default'
            text_size: self.size
            halign: 'left'
            valign: 'top'


        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Start downloads'
                on_release: root.releaseDLStart()
                size_hint_x: 0.9

            Button:
                text: 'Clear All'
                on_release: root.releaseClearAll()
                size_hint_x: 0.1


        ProgressBar:
            id: pb
            min: 0
            max: 100
""")

class MainScreen(Widget):
    text = StringProperty('')
    pct = 0
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def enterClickedUrl(self):
        self.ids.labelUrl.text = self.ids.tiUrl.text
        taget_textinput = self.ids.tiFilename
        taget_textinput.focus = True

    def enterClickedFilename(self):
        self.ids.labelFilename.text = self.ids.tiFilename.text
        taget_textinput = self.ids.tiPath
        taget_textinput.focus = True

    def enterClickedPath(self):
        self.ids.labelPath.text = self.ids.tiPath.text

    def pressSaveUrl(self):
        self.ids.labelUrl.text = self.ids.tiUrl.text


    def pressSaveFilename(self):
        self.ids.labelFilename.text = self.ids.tiFilename.text


    def pressSavePath(self):
        self.ids.labelPath.text = self.ids.tiPath.text


    def pressClearUrl(self):
        self.ids.labelUrl.text = 'Default'
        self.ids.tiUrl.text = ''


    def pressClearFilename(self):
        self.ids.labelFilename.text = 'Default'
        self.ids.tiFilename.text = ''


    def pressClearPath(self):
        self.ids.labelPath.text = 'Default'
        self.ids.tiPath.text = ''

    def releaseClearAll(self):
        self.ids.labelUrl.text = 'Default'
        self.ids.tiUrl.text = ''
        self.ids.labelFilename.text = 'Default'
        self.ids.tiFilename.text = ''
        self.ids.labelPath.text = 'Default'
        self.ids.tiPath.text = ''


    def releaseDLStart(self):
        url = self.ids.tiUrl.text
        if url == '':
            self.ids.labelUrl.text = 'No URL'
        elif 'http' not in url:
            self.ids.labelUrl.text = 'Please check url again'
        else:
            ydl_thread = threading.Thread(target=self.download)
            ydl_thread.start()
            self.ids.pb.value = 0
            Clock.schedule_interval(self.pb_clock, 1/60)



    def pb_clock(self, dt):
        if self.ids.pb.value == 100:
            return False


    def download(self):
        url = self.ids.tiUrl.text
        fn = self.ids.tiFilename.text
        fpath = self.ids.tiPath.text
        if fn == '':
                ydl_opts = {'progress_hooks': [self.progress_state]}
        else:
                out_tmpl = '\\' + fn + '.mp4'
                ydl_opts = {
                        'outtmpl': fpath + out_tmpl,
                        'progress_hooks': [self.progress_state]
                        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


    def progress_state(self, p):
        if p['status'] == 'downloading':
                pct = p['downloaded_bytes'] / p['total_bytes'] * 100 
        elif p['status'] == 'finished':
            pct = 100
            fn = self.ids.tiFilename.text
            donetext = fn + ' has been downloaded!!'
            self.ids.labelUrl.text = donetext
        else:
            self.ids.labelUrl.text = 'Download error!!!'
        self.ids.pb.value = pct
        

class MainGuiApp(App):
    def __init__(self, **kwargs):
        super(MainGuiApp, self).__init__(**kwargs)
        self.title = 'Youtube downloader_v4'

    def build(self):
        MS = MainScreen()
        return MS


def GuiAppStart():
    if __name__ == '__main__':
        App_thread = threading.Thread(target=MainGuiApp().run())
        App_thread.start()
        

if __name__ == '__main__':
    MainGuiApp().run()