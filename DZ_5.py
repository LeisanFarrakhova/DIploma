# Импортируем библиотеки
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests
import json


def update_b_label(event):
    code = base_combobox.get() # Получаем код валюты из списка
    name = currencies[code]    # Находим название в словаре
    b_label.config(text=name)  # Обновляем надпись на экране


def update_2b_label(event):
    code = base_combobox2.get()
    name = currencies[code]
    b_label2.config(text=name)


def update_t_label(event):
    code = target_combobox.get()
    name = currencies[code]
    t_label.config(text=name)


def exchange():
    target_code = target_combobox.get()
    base_code = base_combobox.get()
    base2_code = base_combobox2.get()

    if target_code and base_code and base2_code:
        try:
            response = requests.get(f'https://open.er-api.com/v6/latest/{base_code}')# Запрос к интернету
            response.raise_for_status()
            data = response.json()
            response2 = requests.get(f'https://open.er-api.com/v6/latest/{base2_code}')
            response2.raise_for_status()
            data2 = response2.json()
            if target_code in data['rates']:
                exchange_rate = data['rates'][target_code]
                base = currencies[base_code]
                base2 = currencies[base2_code]
                target = currencies[target_code]
                mb.showinfo("Курс обмена", f"Курс {exchange_rate:.2f} {target} за 1 {base}\n Курс {exchange_rate:.2f} {target} за 1 {base2}")
            else:
                mb.showerror("Ошибка", f"Валюта {target_code} не найдена")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите коды валют")

# Словарь с валютами
currencies = {
    "USD": "Американский доллар",
    "EUR": "Евро",
    "AUD": "Австралийский доллар",
    "CAD": "Канадский доллар",
    "GBP": "Британский фунт стерлингов",
    "RUB": "Российский рубль",
    "JPY": "Японская йена",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "KZT": "Казахстанский тенге",
    "UZS": "Узбекский сум"
 }

window = Tk()
window.title("Курс обмена валюты к доллару")
window.geometry("460x520")

Label(text="Базовая валюта:").pack(padx=10, pady=5) # Создаём текстовое поле
base_combobox = ttk.Combobox(values=list(currencies.keys()))
base_combobox.pack(padx=10, pady=5)
base_combobox.bind("<<ComboboxSelected>>", update_b_label)# При выборе значения из списка, вызывается функция update_b_label

b_label = ttk.Label()
b_label.pack(padx=10, pady=10)

Label(text="Вторая базовая валюта:").pack(padx=10, pady=5)
base_combobox2 = ttk.Combobox(values=list(currencies.keys()))
base_combobox2.pack(padx=10, pady=5)
base_combobox2.bind("<<ComboboxSelected>>", update_2b_label)

b_label2 = ttk.Label()
b_label2.pack(padx=10, pady=10)

Label(text="Целевая валюта:").pack(padx=10, pady=5)
target_combobox = ttk.Combobox(values=list(currencies.keys()))
target_combobox.pack(padx=10, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=10)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)

window.mainloop()
