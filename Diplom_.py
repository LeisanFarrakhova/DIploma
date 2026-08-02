"""
Приложение для отображения курсов криптовалют к доллару США
"""

import os #Импорт модуля os для поиска пути к файлу иконки)
import tkinter as tk #
from tkinter import ttk, messagebox as mb #Импорт модуля tkinter (окна, кнопки, надписи) messagebox для отображения всплывающих окон с сообщениями.
import requests # для выполнения HTTP-запросов к API CoinGecko.

# Обновляет отображаемое название криптовалюты при выборе в выпадающем списке.
def update_crypto_label(event):
    code = crypto_combobox.get()
    name = cryptos[code]
    crypto_label.config(text=name)


# Обновляет отображаемое название целевой валюты (доллара) при выборе в выпадающем списке.
def update_target_label(event):
    code = target_combobox.get()
    name = target_currencies[code]
    target_label.config(text=name)

#Главная функция - получает актуальный курс выбранной криптовалюты к доллару США
# через API CoinGecko и показывает результат во всплывающем окне.
def get_crypto_price():
    crypto_code = crypto_combobox.get()
    target_code = target_combobox.get()

#Проверка, что обе валюты выбраны (не пустые строки)
    if crypto_code  and target_code:
        try:
# Запрос к API CoinGecko для первой криптовалюты
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": crypto_code, #код криптовалюты
                "vs_currencies": target_code.lower(),# код целевой валюты
                "include_24hr_change": "true"# включает информацию об изменении за 24 часа
            }

            response = requests.get(url, params=params, timeout=10) # получает от API с параметрами и таймаутом в 10с
            response.raise_for_status() # проверка статуса ответа
            data = response.json() # преобразование ответа в формате JSON в словарь Python

# Получаем данные для первой криптовалюты
            if crypto_code in data :
                price1 = data[crypto_code][target_code.lower()]
                change1 = data[crypto_code].get(f"{target_code.lower()}_24h_change", 0)

# Форматируем цену
                if price1 >= 1000:
                    price1_text = f"{price1:,.2f}"
                elif price1 >= 1:
                    price1_text = f"{price1:.2f}"
                elif price1 >= 0.01:
                    price1_text = f"{price1:.4f}"
                else:
                    price1_text = f"{price1:.6f}"


                crypto_name = cryptos[crypto_code]
                target_name = target_currencies[target_code]

# Формируем сообщение
                message = (f"Курс {crypto_name} к {target_name}: {price1_text} {target_code.upper()}\n"
                           f"Изменение за 24ч: {change1:+.2f}%\n\n")

                mb.showinfo("Курс криптовалют", message)
            else:
                mb.showerror("Ошибка", "Криптовалюта не найдена")

        except requests.exceptions.RequestException as e:
            mb.showerror("Ошибка сети", f"Не удалось подключиться к API: {e}")
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите криптовалюты и целевую валюту")


# Словарь с криптовалютами
cryptos = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "binancecoin": "Binance Coin (BNB)",
    "solana": "Solana (SOL)",
    "cardano": "Cardano (ADA)",
    "dogecoin": "Dogecoin (DOGE)",
    "polkadot": "Polkadot (DOT)",
    "polygon": "Polygon (MATIC)",
    "litecoin": "Litecoin (LTC)",
    "chainlink": "Chainlink (LINK)",
    "ripple": "Ripple (XRP)",
    "avalanche": "Avalanche (AVAX)"
}

# Словарь с целевыми валютами (только доллар в нашей задаче)
target_currencies = {
    "usd": "Доллар США"
}

# Создаем окно
window = tk.Tk()
window.title("Курс криптовалют к доллару")
window.geometry("500x400")
window.configure(bg="#f0f0f0")

icon_filename = "logo.ico"

# Автоматически находим путь к папке со скриптом
script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, icon_filename)

print(f" Ищу иконку здесь: {icon_path}")

try:
    # iconbitmap — нативный способ для Windows, не требует Pillow
    window.iconbitmap(icon_path)
    # print("Иконка установлена!")
except Exception as e:
    print(f" Ошибка: {e}")
    print(" Проверьте: файл logo.ico лежит в той же папке, что и скрипт?")
# Заголовок
tk.Label(window, text="Курс криптовалют к доллару",
    font=("Arial", 14, "bold"), bg="#f0f0f0").pack(padx=10, pady=10)

# Первая криптовалюта
tk.Label(text="Криптовалюта:", bg="#f0f0f0").pack(padx=10, pady=5)
crypto_combobox = ttk.Combobox(values=list(cryptos.keys()))
crypto_combobox.pack(padx=10, pady=5)
crypto_combobox.bind("<<ComboboxSelected>>", update_crypto_label)

crypto_label = ttk.Label()
crypto_label.pack(padx=10, pady=5)

# Целевая валюта (фиксированно USD)
tk.Label(text="Целевая валюта:", bg="#f0f0f0").pack(padx=10, pady=5)
target_combobox = ttk.Combobox(values=list(target_currencies.keys()))
target_combobox.set("usd")  # Устанавливаем USD по умолчанию
target_combobox.pack(padx=10, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_target_label)

target_label = ttk.Label()
target_label.config(text="Доллар США")
target_label.pack(padx=10, pady=5)

# Кнопка получения курса
(tk.Button(window,text="Получить курс обмена", command=get_crypto_price,
    bg="black", fg="white", font=("Arial", 10, "bold"),
    padx=20, pady=10).pack(padx=10, pady=15))

# Запуск главного цикла
window.mainloop()