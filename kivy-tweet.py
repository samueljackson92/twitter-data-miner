from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class Tweeter(App):
    def build(self):
        parent = Widget()
        text = TextInput(text='Type your status...', multiline=False)
        sendbtn = Button(text='Send')

        parent.add_widget(text)
        #parent.add_widget(sendbtn)
        return parent

 	def newSearch(self):
 		#make a new search
 		return None


if __name__ == '__main__':
    Tweeter().run()