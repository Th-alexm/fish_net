import logging
import os

# Убедимся, что директория для логов существует
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "logs.txt")

logging.basicConfig(
    filename=log_file,
    filemode='a',  # Добавлять логи к файлу, а не затирать его
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Запись в файл
        logging.StreamHandler()         # Запись в консоль
    ]
)

def log_check(domain, result, message):
    """Логируем результат проверки домена."""
    try:
        logging.info(f'Checked domain: {domain}, Result: {result}, Message: {message}')
    except Exception as e:
        logging.error(f"Ошибка при записи в лог: {str(e)}")
