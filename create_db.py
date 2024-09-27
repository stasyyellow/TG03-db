import sqlite3


# Функция для создания базы данных и таблицы students
def init_db():
    conn = sqlite3.connect('school_data.db')  # Подключение к базе данных (если её нет, она будет создана)
    cur = conn.cursor()

    # Создание таблицы students, если она не существует
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')

    conn.commit()  # Сохранение изменений
    conn.close()  # Закрытие подключения


# Запуск функции для создания базы данных
if __name__ == '__main__':
    init_db()
