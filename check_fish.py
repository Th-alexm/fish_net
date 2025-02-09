from urllib.parse import urlparse
import re
import requests
import whois
import datetime
from check_rank import is_top_1_million, get_domain_authority, get_alexa_rank

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
    
def get_domain_age(domain):
    """Получить возраст домена."""
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age = (datetime.datetime.now() - creation_date).days / 365
            return age
        else:
            return None
    except Exception as e:
        return None

# Функция для проверки URL на фишинг
# Функция для проверки URL на фишинг
def check_phishing(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Проверка домена (на известность)
    if not check_domain(url):
        return False, "Подозрительный домен."

    # Проверка на наличие https
    if not url.startswith("https://"):
        return False, "URL не использует HTTPS. Это может быть опасным."

    # Проверка на наличие www в начале (некоторые фишинговые сайты это игнорируют)
    if domain.startswith("www."):
        domain = domain[4:]

    # Проверка на использование кириллических символов
    if re.search(r"[а-яА-Я]", domain):  # Если в домене используются кириллические символы
        return False, "В домене использованы кириллические символы. Это может быть фишинг."
# Проверка Alexa Rank
    in_top_1m, alexa_message = is_top_1_million(domain)
    if not in_top_1m:
        return False, f"Alexa Rank: {alexa_message}"

    # Проверка Domain Authority
    da, da_message = get_domain_authority(domain)
    if da and da < 30:  # Примерное значение, можно корректировать
        return False, f"Domain Authority низкий: {da_message}"

    # Проверка возраста домена
    age = get_domain_age(domain)
    if age is not None and age < 1:  # Например, домен младше 1 года
        return False, "Возраст домена меньше 1 года. Это может быть фишинговый сайт."

    # Дополнительная проверка на наличие фишинговых признаков
    if "pay" in domain and "com" in domain:
        return False, "Подозрительное имя домена (возможно фишинг)."

    # Проверка SSL сертификата
    try:
        response = requests.get(url, timeout=5, verify=True)
    except requests.exceptions.SSLError:
        return False, "SSL-сертификат сайта не действителен. Это может быть фишинг."

    return True, "Ссылка безопасна."
# Пример использования
url = "https://pay.yookassa.ru"
result, message = check_phishing(url)
print(result, message)
