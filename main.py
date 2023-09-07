from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
import sqlite3

from kivy.core.window import Window
Window.size = (420, 720)

def connect_db(name):
    connect = sqlite3.connect(name)
    cursor = connect.cursor()
    return connect, cursor

class Clicker(Widget):
    def ready(self):
        connect, cursor = connect_db("clicker.db")
        cursor.execute("""
                        SELECT points FROM game WHERE id = 1;
                    """)
        data = cursor.fetchone()
        return str(data[0])
    def click(self):
        connect, cursor = connect_db("clicker.db")
        cursor.execute("""
                SELECT points, power_touch FROM game WHERE id = 1;
            """)
        data = cursor.fetchone()
        cursor.execute(f"""
                        UPDATE game SET points = {data[0] + data[1]} WHERE id = 1;
                    """)
        connect.commit()
        self.ids._label.text = str(data[0] + data[1])

def start():
    connect, cursor = connect_db("clicker.db")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game(
            id INTEGER,
            points INTEGER,
            power_touch INTEGER,
            UNIQUE(id)
        );
    """)
    connect.commit()
    cursor.execute("""
        INSERT OR IGNORE INTO game VALUES(?,?,?)
    """, [1, 0, 1])
    connect.commit()

class MyApp(MDApp):
    def build(self):
        start()
        return Clicker()

MyApp().run()