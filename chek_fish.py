import requests
import whois
from urllib.parse import urlparse
import re

# База известных доменов для проверки
KNOWN_PAYMENT_SERVICES = ["yookassa.ru", "tinkoff.ru", "qiwi.com", "pay.pochta.ru"]

# Функция для проверки, является ли домен известным
def is_known_payment_service(domain):
    return domain in KNOWN_PAYMENT_SERVICES

# Функция для проверки домена
def check_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Проверяем, является ли домен известным сервисом
    if is_known_payment_service(domain):
        return True
    else:
        return False

# Функция для проверки URL на фишинг
def check_phishing(url):
    # Проверка на наличие https (платежи всегда должны быть через защищенный протокол)
    if not url.startswith("https://"):
        return False, "URL не использует HTTPS. Это может быть опасным."

    # Проверка домена и поддомена
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if not check_domain(domain):
        return False, "Подозрительный домен или поддомен. Это может быть фишинг."

    # Проверка на использование подозрительных символов в домене
    # Например, домены с похожими символами (yookassa -> yokassa)
    if re.search(r"[а-яА-Я]", domain):  # Если в домене используются кириллические символы
        return False, "В домене использованы кириллические символы. Это может быть фишинг."

    # Проверка SSL сертификата
    try:
        response = requests.get(url, timeout=5, verify=True)
    except requests.exceptions.SSLError:
        return False, "SSL-сертификат сайта не действителен. Это может быть фишинг."

    # Дополнительная проверка WHOIS на подозрительность
    try:
        whois_info = whois.whois(domain)
        # Проверка на срок регистрации домена
        if whois_info.creation_date and isinstance(whois_info.creation_date, list):
            creation_date = whois_info.creation_date[0]
        else:
            creation_date = whois_info.creation_date

        # Если домен зарегистрирован недавно (менее 1 года), это может быть подозрительным
        if creation_date and (pd.to_datetime('now') - pd.to_datetime(creation_date)).days < 365:
            return False, "Домен был зарегистрирован недавно. Это может быть фишинг."
    except Exception as e:
        return False, f"Ошибка при проверке WHOIS: {str(e)}"

    return True, "Ссылка безопасна."

# Пример использования
url = "https://pay.yookassa.ru"
result, message = check_phishing(url)
print(result, message)
