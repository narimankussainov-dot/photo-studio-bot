from google_sheets import append_to_sheet

test_data = {
    'tg_username': '@test_user',
    'name': 'Тест',
    'city': 'Павлодар',
    'school': '39',
    'class_num': '11А',
    'students_count': '25',
    'decision_maker': 'родители',
    'format': 'WhatsApp'
}

append_to_sheet(test_data)