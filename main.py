import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

import sqlite3
import os
from datetime import datetime

DB_NAME = "samples.db"

# ---------- Инициализация базы данных ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            status TEXT,
            activity TEXT,
            contact1 TEXT,
            position1 TEXT,
            phone1 TEXT,
            contact2 TEXT,
            position2 TEXT,
            phone2 TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trade_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            point_code TEXT UNIQUE,
            client_id INTEGER,
            address TEXT,
            point_comment TEXT,
            visit_date TEXT,
            rep1_name TEXT,
            rep1_phone TEXT,
            rep2_name TEXT,
            rep2_phone TEXT,
            trade_point_comment TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS point_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            point_id INTEGER,
            collection_id INTEGER,
            status TEXT CHECK(status IN ('Есть', 'ненужно', 'нет нужно', 'нет', 'возвращен')),
            FOREIGN KEY (point_id) REFERENCES trade_points(id),
            FOREIGN KEY (collection_id) REFERENCES collections(id),
            UNIQUE(point_id, collection_id)
        )
    """)
    conn.commit()
    conn.close()

# ---------- Функции для работы с БД ----------
def get_all_clients():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM clients ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_trade_points():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT tp.id, tp.point_code, c.name, tp.address
        FROM trade_points tp
        LEFT JOIN clients c ON tp.client_id = c.id
        ORDER BY tp.point_code
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_trade_point_by_id(point_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT point_code, client_id, address, point_comment, visit_date,
               rep1_name, rep1_phone, rep2_name, rep2_phone, trade_point_comment
        FROM trade_points WHERE id = ?
    """, (point_id,))
    row = cur.fetchone()
    conn.close()
    return row

def get_point_samples(point_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, ps.status
        FROM point_samples ps
        JOIN collections c ON ps.collection_id = c.id
        WHERE ps.point_id = ?
        ORDER BY c.name
    """, (point_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def update_point_sample_status(point_id, collection_name, new_status):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id FROM collections WHERE name = ?", (collection_name,))
    coll = cur.fetchone()
    if not coll:
        conn.close()
        return False
    coll_id = coll[0]
    cur.execute("""
        INSERT INTO point_samples (point_id, collection_id, status)
        VALUES (?, ?, ?)
        ON CONFLICT(point_id, collection_id) DO UPDATE SET status=excluded.status
    """, (point_id, coll_id, new_status))
    conn.commit()
    conn.close()
    return True

def add_trade_point(code, client_id, address, comment):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO trade_points (point_code, client_id, address, point_comment)
            VALUES (?, ?, ?, ?)
        """, (code, client_id, address, comment))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_collections():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM collections ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- Kivy-экраны ----------
class TradePointsScreen(Screen):
    def on_enter(self):
        self.load_points()

    def load_points(self, client_filter='', address_filter=''):
        points = get_all_trade_points()
        filtered = []
        for p in points:
            if client_filter and client_filter not in p[2]:
                continue
            if address_filter and address_filter.lower() not in p[3].lower():
                continue
            filtered.append({'text': f"{p[1]} – {p[2] or 'Без клиента'} – {p[3][:30]}", 'point_id': p[0]})
        self.ids.points_list.data = filtered

    def apply_filters(self):
        client = self.ids.client_spinner.text
        address = self.ids.address_input.text
        self.load_points(client, address)

    def reset_filters(self):
        self.ids.client_spinner.text = ''
        self.ids.address_input.text = ''
        self.apply_filters()

    def go_to_detail(self, point_id):
        self.manager.current = 'detail'
        self.manager.get_screen('detail').load_point(point_id)

    def open_add_point(self):
        self.manager.current = 'add_point'


class SampleItem(BoxLayout, RecycleDataViewBehavior):
    index = None
    collection = StringProperty('')
    status = StringProperty('')
    point_id = NumericProperty(0)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.collection = data['collection']
        self.status = data['status']
        self.point_id = data['point_id']
        return super().refresh_view_attrs(rv, index, data)

    def change_status(self, new_status):
        if update_point_sample_status(self.point_id, self.collection, new_status):
            self.status = new_status
            app = App.get_running_app()
            detail_screen = app.root.get_screen('detail')
            detail_screen.load_point(self.point_id)


class TradePointDetailScreen(Screen):
    point_id = NumericProperty(0)

    def load_point(self, point_id):
        self.point_id = point_id
        data = get_trade_point_by_id(point_id)
        if data:
            self.ids.point_code.text = data[0]
            client_name = ''
            if data[1]:
                for c in get_all_clients():
                    if c[0] == data[1]:
                        client_name = c[1]
                        break
            self.ids.client.text = client_name or 'Не указан'
            self.ids.address.text = data[2] or 'Адрес не указан'
        samples = get_point_samples(point_id)
        sample_data = [{'collection': s[0], 'status': s[1], 'point_id': point_id} for s in samples]
        self.ids.samples_list.data = sample_data

    def set_all_status(self, status):
        for item in self.ids.samples_list.data[:]:
            if update_point_sample_status(self.point_id, item['collection'], status):
                item['status'] = status
        self.load_point(self.point_id)

    def go_back(self):
        self.manager.current = 'points'

    def add_collection_dialog(self):
        collections = get_collections()
        if not collections:
            popup = Popup(title='Ошибка', content=Label(text='Нет коллекций'), size_hint=(0.8, 0.4))
            popup.open()
            return
        layout = BoxLayout(orientation='vertical')
        for coll_id, coll_name in collections:
            btn = Button(text=coll_name, size_hint_y=None, height=40)
            btn.bind(on_press=lambda x, c=coll_name: self.add_collection_with_status(c))
            layout.add_widget(btn)
        popup = Popup(title='Выберите коллекцию', content=layout, size_hint=(0.9, 0.8))
        popup.open()

    def add_collection_with_status(self, collection_name):
        if update_point_sample_status(self.point_id, collection_name, 'Есть'):
            self.load_point(self.point_id)
            popup = Popup(title='Успех', content=Label(text='Добавлено'), size_hint=(0.6, 0.3))
            popup.open()
        else:
            popup = Popup(title='Ошибка', content=Label(text='Не удалось добавить'), size_hint=(0.6, 0.3))
            popup.open()


class AddPointScreen(Screen):
    def save_point(self):
        code = self.ids.code_input.text.strip()
        if not code:
            self.show_error('Введите код точки')
            return
        client_sel = self.ids.client_spinner.text
        client_id = None
        if client_sel and client_sel != 'Без клиента':
            for c in get_all_clients():
                if c[1] == client_sel:
                    client_id = c[0]
                    break
        address = self.ids.address_input.text.strip()
        comment = self.ids.comment_input.text.strip()
        if add_trade_point(code, client_id, address, comment):
            self.ids.code_input.text = ''
            self.ids.address_input.text = ''
            self.ids.comment_input.text = ''
            self.show_msg('Точка добавлена')
            self.manager.current = 'points'
        else:
            self.show_error('Точка с таким кодом уже существует')

    def show_error(self, msg):
        popup = Popup(title='Ошибка', content=Label(text=msg), size_hint=(0.8, 0.4))
        popup.open()

    def show_msg(self, msg):
        popup = Popup(title='Успех', content=Label(text=msg), size_hint=(0.8, 0.4))
        popup.open()


class ReportScreen(Screen):
    def on_enter(self):
        self.show_needed_report()

    def show_needed_report(self):
        # Пример отчёта – можно расширить логикой
        txt = "Отчёт о необходимости привезти:\n"
        txt += "Клиент А | Коллекция Х | нужно\nКлиент Б | Коллекция Y | есть\n"
        self.ids.report_label.text = txt

    def show_collection_report(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            SELECT c.name, COUNT(ps.point_id) as cnt
            FROM collections c
            JOIN point_samples ps ON c.id = ps.collection_id
            WHERE ps.status = 'Есть'
            GROUP BY c.id
            ORDER BY c.name
        """)
        rows = cur.fetchall()
        conn.close()
        if rows:
            txt = "Коллекция | Кол-во точек\n"
            for name, cnt in rows:
                txt += f"{name} | {cnt}\n"
        else:
            txt = "Нет образцов со статусом 'Есть'"
        self.ids.report_label.text = txt

    def go_back(self):
        self.manager.current = 'points'


class SamplesApp(App):
    def get_all_clients_simple(self):
        return get_all_clients()

    def build(self):
        init_db()
        sm = ScreenManager()
        sm.add_widget(TradePointsScreen(name='points'))
        sm.add_widget(TradePointDetailScreen(name='detail'))
        sm.add_widget(AddPointScreen(name='add_point'))
        sm.add_widget(ReportScreen(name='reports'))
        return sm


if __name__ == '__main__':
    SamplesApp().run()
