"""
* @file logger_setup.py
* @brief Настройка логирования и функция логирования результатов проверки доменов.
*
* Этот модуль инициализирует систему логирования, проверяет наличие папки для логов,
* создаёт файл логов и обеспечивает сохранение записей в файл и вывод в консоль.
"""
import logging
import os

"""
* @brief Директория, в которой будут храниться логи.
*
* Если директории `logs` не существует, она будет создана.
"""

log_dir = "logs"

# Убедимся, что директория для логов существует
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

"""
* @brief Путь к файлу логов.
"""
log_file = os.path.join(log_dir, "logs.txt")

"""
* @brief Настройка системы логирования.
*
* - Логи записываются в файл `logs.txt` в режиме добавления (`a`).
* - Уровень логирования установлен на INFO.
* - Формат логирования включает время, уровень и само сообщение.
* - Записи дублируются в файл и в консоль.
"""

logging.basicConfig(
    filename=log_file,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Запись в файл
        logging.StreamHandler()         # Вывод в консоль
    ]
)

"""
* @brief Логирует результат проверки домена.
*
* Эта функция записывает в логи информацию о домене, результате проверки и сообщении.
* В случае ошибки при записи в лог, ошибка также будет записана.
*
* @param domain Строка с доменным именем, которое проверяется.
* @param result Результат проверки (например, "Safe" или "Suspicious").
* @param message Дополнительная информация о проверке или её результате.
*
* @return None
"""

def log_check(domain, result, message):
    try:
        logging.info(f'Checked domain: {domain}, Result: {result}, Message: {message}')
    except Exception as e:
        logging.error(f"Ошибка при записи в лог: {str(e)}")
