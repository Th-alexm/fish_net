"""
* @file domain_checks.py
* @brief Набор функций для проверки домена и URL.
*
* Этот модуль содержит функции для проверки:
* - Является ли домен известным платёжным сервисом.
* - Возраста домена (через whois).
* - Наличия HTTPS в ссылке.
* - Длины домена.
* - Другие вспомогательные проверки.
"""

import whois
import datetime
from urllib.parse import urlparse


"""
* @brief Проверяет, содержит ли домен какие-либо известные платёжные сервисы.
*
* Функция определяет, есть ли в заданном домене подстрока, совпадающая с одним из
* известных платёжных сервисов (напр. "yookassa", "qiwi", "tinkoff" и т.д.).
*
* @param domain Строка с доменным именем, например "pay.qiwi.com".
* @return bool True, если домен содержит одно из ключевых слов, иначе False.

"""
def is_known_payment_service(domain):
    known_services = ["yookassa", "tinkoff", "qiwi", "pay", "sberbank"]
    return any(service in domain for service in known_services)


"""
* @brief Выполняет проверку домена по URL, чтобы выяснить, относится ли он к известному платёжному сервису.
*
* Функция анализирует URL, извлекает из него домен и затем проверяет, содержится ли он в списке
* известных сервисов (через функцию @ref is_known_payment_service).
*
* @param url Полный URL, например "https://tinkoff.ru/pay".
* @return bool True, если домен известен как платёжный сервис, иначе False.
"""
def check_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if is_known_payment_service(domain):
        return True
    else:
        return False

"""
* @brief Получает возраст домена (в годах).
*
* Функция пытается с помощью модуля whois получить дату регистрации домена и
* вычислить, сколько лет прошло с момента регистрации до текущей даты.
*
* @param domain Строка с доменным именем (например, "example.com").
* @return float|None Возраст домена в годах (типа float). Если дата регистрации не найдена или произошла ошибка, возвращается None.

"""
def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        # Если creation_date — список, берём первый элемент
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        if creation_date:
            age = (datetime.datetime.now() - creation_date).days / 365
            return age
        else:
            return None
    except Exception as e:
        return None

"""
* @brief Проверяет, используется ли HTTPS в заданном URL.
*
* @param url Полный URL, например "http://example.com".
* @return (bool, str) Кортеж, где первый элемент — результат проверки (True/False),
* второй элемент — сообщение о проверке.
"""

def check_https(url):
    if url.startswith("https://"):
        return True, "Ссылка использует HTTPS."
    else:
        return False, "URL не использует HTTPS. Это может быть опасным."

"""
* @brief Проверяет длину домена, извлечённого из URL.
*
* Анализирует доменную часть ссылки. Если домен слишком короткий (менее 3 символов)
* или слишком длинный (более 253 символов), функция возвращает предупреждение.
*
* @param url Полный URL, например "https://subdomain.example.com/path".
* @return (bool, str) Кортеж, где первый элемент — результат проверки (True/False),
* второй элемент — сообщение о результате проверки.
"""

def check_domain_length(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    domain_length = len(domain)
    if domain_length < 3:
        return False, "Домен слишком короткий. Это может быть фишинг."
    elif domain_length > 253:
        return False, "Домен слишком длинный. Это может быть подозрительным."
    
    return True, "Домен имеет нормальную длину."
