import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo

# Настройки доступа
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# ID твоей таблицы (берется из ссылки на таблицу, длинный набор букв и цифр)
SPREADSHEET_ID = "1Jsf5DX4cNPNE5nM_6-c2HvdUWqHejxg8FyKPgtlCkw8"


def append_to_sheet(data: dict):
    """Записывает собранные данные в новую строку Гугл Таблицы"""
    try:
        credentials = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

        # Убираем @None, если юзернейма нет
        tg_username = data.get('tg_username', '')
        if tg_username == '@None' or tg_username is None:
            tg_username = '-'

        # --- Задаем часовой пояс (UTC+5) ---
        tz = ZoneInfo("Asia/Almaty")

        # Формируем строку для записи
        row = [
            datetime.now(tz).strftime("%Y-%m-%d %H:%M"),  # <-- Передали tz внутрь now()
            tg_username,
            data.get('name', '-'),
            data.get('phone', '-'),
            data.get('city', '-'),
            data.get('school', '-'),
            data.get('class_num', '-'),
            data.get('students_count', '-'),
            data.get('decision_maker', '-'),
            data.get('format', '-')
        ]

        sheet.append_row(row)
        print("✅ Данные успешно записаны в Google Таблицу!")
    except Exception as e:
        print(f"❌ Ошибка при записи в таблицу: {e}")