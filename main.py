from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import os

class SavingsApp(App):
    def build(self):
        # 1. Main Layout
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # 2. Title Label
        self.label = Label(text="Customer Savings: Rs 50", font_size='30sp', bold=True)
        
        # 3. Create the Button
        self.btn = Button(text="LOADING...", font_size='25sp')
        self.btn.bind(on_press=self.toggle)

        # 4. Check Saved State (Local Storage)
        if os.path.exists("save_data.txt"):
            with open("save_data.txt", "r") as f:
                saved_state = f.read()
        else:
            saved_state = "OFF"

        # 5. Set Initial Look
        if saved_state == "ON":
            self.set_on()
        else:
            self.set_off()

        layout.add_widget(self.label)
        layout.add_widget(self.btn)
        return layout

    def toggle(self, instance):
        # If currently ON, turn OFF. If OFF, turn ON.
        if self.btn.text == "Turn OFF (Active)":
            self.set_off()
        else:
            self.set_on()

    def set_on(self):
        self.btn.text = "Turn OFF (Active)"
        self.btn.background_color = (0, 1, 0, 1) # Green
        # Save to file
        with open("save_data.txt", "w") as f:
            f.write("ON")

    def set_off(self):
        self.btn.text = "Turn ON"
        self.btn.background_color = (1, 0, 0, 1) # Red
        # Save to file
        with open("save_data.txt", "w") as f:
            f.write("OFF")

if __name__ == '__main__':
    SavingsApp().run()
