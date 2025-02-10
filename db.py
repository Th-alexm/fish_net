import sqlite3
from datetime import datetime

# Инициализация БД и таблицы (если еще не существует)
def create_db():
    conn = sqlite3.connect('checked_domains.db')  # Используем только checked_domains.db
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domain_check_results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            result TEXT NOT NULL,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            checked_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Функция для добавления результата в БД
def insert_result(domain, result, message):
    conn = sqlite3.connect('checked_domains.db')  # Используем только checked_domains.db
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO domain_check_results (domain, result, message, checked_at)
    VALUES (?, ?, ?, ?)
    ''', (domain, result, message, datetime.now()))
    
    conn.commit()
    conn.close()

# Функция для получения результата из базы данных по домену
def get_result(domain):
    if not domain:  # Проверяем, что домен не пуст
        return None

    conn = sqlite3.connect('checked_domains.db')  # Используем только checked_domains.db
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT result, message, checked_at FROM domain_check_results
    WHERE domain = ?
    ORDER BY checked_at DESC LIMIT 1
    ''', (domain,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'result': result[0],
            'message': result[1],
            'checked_at': result[2]
        }
    return None
