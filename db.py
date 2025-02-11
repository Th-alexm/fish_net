'''
 * @file domain_check.py
 * @brief Модуль для работы с базой данных SQLite, который хранит результаты проверки доменов.
 *
 * Этот модуль предоставляет функции для создания базы данных, добавления результатов
 * проверок доменов в базу данных, а также для получения последних результатов
 * проверки по домену.
 *
 * Модуль использует SQLite для хранения результатов проверки и их временных меток.
 
'''
import sqlite3
from datetime import datetime

'''
 * @brief Инициализирует базу данных и таблицу, если они еще не существуют.
 *
 * Эта функция создает базу данных `checked_domains.db` и таблицу `domain_check_results`,
 * если они еще не существуют. Таблица содержит следующие поля:
 * - id: уникальный идентификатор записи (целое число, автоинкремент).
 * - domain: домен, который проверяется (строка).
 * - result: результат проверки домена (строка).
 * - message: сообщение, связанное с результатом проверки (строка, может быть пустым).
 * - timestamp: временная метка, когда запись была создана (время по умолчанию - текущее).
 * - checked_at: время проверки домена (строка).
 *
 * @return None
 '''
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

"""
/**
 * @brief Добавляет результат проверки домена в базу данных.
 *
 * Эта функция добавляет новый результат проверки домена в таблицу `domain_check_results`.
 * В качестве аргументов передаются:
 * - domain: домен, который проверяется (строка).
 * - result: результат проверки (строка).
 * - message: сообщение, связанное с результатом проверки (строка).
 * 
 * Функция добавляет запись с текущим временем в поле `checked_at`.
 *
 * @param domain Домен, который проверяется.
 * @param result Результат проверки домена.
 * @param message Сообщение, связанное с результатом проверки.
 * @return None
 */
 """
def insert_result(domain, result, message):
    conn = sqlite3.connect('checked_domains.db')  # Используем только checked_domains.db
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO domain_check_results (domain, result, message, checked_at)
    VALUES (?, ?, ?, ?)
    ''', (domain, result, message, datetime.now()))
    
    conn.commit()
    conn.close()
'''
 
  * @brief Получает последний результат проверки домена из базы данных.
  *
  * Эта функция позволяет получить последний результат проверки для заданного домена.
  * Функция выполняет запрос по домену, сортирует по дате и времени и возвращает последний результат.
  * Если результат для данного домена найден, возвращается словарь с тремя полями:
  * - result: результат проверки.
  * - message: сообщение, связанное с результатом.
  * - checked_at: время, когда проверка была проведена.
  *
  * @param domain Домен, для которого требуется получить результат.
  * @return Словарь с результатами проверки, если результат найден. Если домен пустой или запись не найдена, возвращается None.
  
  '''
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
