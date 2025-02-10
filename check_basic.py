import whois
import datetime
from urllib.parse import urlparse

# База известных доменов для проверки
KNOWN_PAYMENT_SERVICES = ["yookassa.ru", "tinkoff.ru", "qiwi.com", "pay.pochta.ru"]

# Функция для проверки, является ли домен известным
def is_known_payment_service(domain):
    known_services = ["yookassa", "tinkoff", "qiwi", "pay", "sberbank"]
    return any(service in domain for service in known_services)


# Функция для проверки домена
def check_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Проверяем, является ли домен известным сервисом
    if is_known_payment_service(domain):
        return True
    else:
        return False

# Функция для получения возраста домена
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

# Функция для проверки на наличие https
def check_https(url):
    """Проверяет, используется ли HTTPS в URL."""
    if url.startswith("https://"):
        return True, "Ссылка использует HTTPS."
    else:
        return False, "URL не использует HTTPS. Это может быть опасным."

# Функция для проверки длины домена
def check_domain_length(url):
    """Проверяет длину домена."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Проверяем длину домена
    domain_length = len(domain)
    if domain_length < 3:
        return False, "Домен слишком короткий. Это может быть фишинг."
    elif domain_length > 253:
        return False, "Домен слишком длинный. Это может быть подозрительным."
    
    return True, "Домен имеет нормальную длину."