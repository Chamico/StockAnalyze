from kivy.app import App
from kivy.uix.label import Label

class ChamicoApp(App):

    def build(self):
        return Label(text = "hello world")
    

def UIProcee():
     ChamicoApp().run()

   