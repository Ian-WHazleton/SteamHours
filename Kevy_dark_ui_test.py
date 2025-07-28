from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor = (43/255, 43/255, 43/255, 1)  # #2b2b2b

class PriceBreakdownApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=10)
        title = Label(text="Price Breakdown", color=(1,1,1,1), font_size=24, bold=True, size_hint=(1, None), height=40)
        summary = Label(text="Total Cost: $99.99 | Games: 5", color=(1,1,1,1), font_size=18, size_hint=(1, None), height=30)
        box = BoxLayout(orientation='vertical', size_hint=(1, 0.7), padding=10)
        with box.canvas.before:
            Color(64/255, 64/255, 64/255, 1)
            box_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[10])
        def update_box_rect(instance, value):
            box_rect.pos = box.pos
            box_rect.size = box.size
        box.bind(pos=update_box_rect, size=update_box_rect)
        text = TextInput(text="Game Name                Bundle Cost   Steam Price   Bundle %\n"
                              "----------------------------------------------------------\n"
                              "Example Game 1           $10.00        $20.00        10.0%\n"
                              "Example Game 2           $20.00        $30.00        20.0%\n",
                         readonly=True, background_color=(64/255,64/255,64/255,1), foreground_color=(1,1,1,1),
                         font_size=16)
        box.add_widget(text)
        btn = Button(text="Proceed with These Prices", size_hint=(None, None), size=(250, 50),
                     background_color=(76/255, 175/255, 80/255, 1), color=(1,1,1,1), font_size=18)
        root.add_widget(title)
        root.add_widget(summary)
        root.add_widget(box)
        root.add_widget(btn)
        return root

PriceBreakdownApp().run()