import logging
import os

# Убедимся, что директория для логов существует
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "logs.txt")

# Настройка логирования
logging.basicConfig(
    filename=log_file,  # Путь к файлу лога
    level=logging.INFO,  # Уровень логирования (INFO - все сообщения, WARNING - только предупреждения и ошибки)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_check(domain, result, message):
    """Логируем результат проверки домена."""
    try:
        logging.info(f'Checked domain: {domain}, Result: {result}, Message: {message}')
    except Exception as e:
        logging.error(f"Ошибка при записи в лог: {str(e)}")
