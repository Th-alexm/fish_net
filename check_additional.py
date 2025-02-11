"""
* @file check_additional.py
* @brief Набор функций для проверки URL на фишинг.
*
* В этом файле описаны функции, которые выполняют различные проверки:
* - Проверка на подозрительные символы в домене.
* - Проверка на подозрительные поддомены.
* - Проверка наличия (валидности) SSL-сертификата.
* - Проверка URL с помощью Google Safe Browsing API.
"""
import re
import ssl
import socket
from urllib.parse import urlparse
import requests

"""
* @brief Проверяет домен на наличие подозрительных символов.
*
* Данная функция ищет:
* - Наличие цифр в домене.
* - Наличие нескольких дефисов подряд.
*
* @param domain Доменная часть URL (строка).
* @return Кортеж: (bool, str).
*   - bool — результат проверки (True, если всё в порядке).
*   - str — описание результата или причина, по которой домен считается подозрительным.
"""
def check_suspicious_characters(domain):
    if re.search(r'\d', domain):  # Проверяем наличие цифр в домене
        return False, "Домен содержит цифры, что может быть подозрительно."
    if re.search(r'[-]{2,}', domain):  #Проверяем наличие нескольких дефисов подряд
        return False, "Домен содержит несколько дефисов подряд, что может быть подозрительно."
    return True, "Домен не содержит подозрительных символов."

"""
* @brief Проверяет наличие подозрительных поддоменов в URL.
*
* Функция извлекает все поддомены (всё, что до доменной части вида example.com) и проверяет их количество.
* Если поддоменов более 2, это может указывать на попытку скрыть истинный домен.
*
* @param url Полный URL (строка).
* @return Кортеж: (bool, str).
*   - bool — результат проверки (True, если поддомены в порядке).
*   - str — сообщение о результате проверки.
"""

def check_subdomains(url):
    parsed_url = urlparse(url)
    subdomains = parsed_url.netloc.split(".")[:-2]  #Извлекаем поддомены
    if len(subdomains) > 2:  #Если поддоменов больше 2-х
        return False, "Слишком много поддоменов, это может быть фишинг."
    return True, "Поддомены в порядке."

"""
* @brief Проверяет URL с помощью Google Safe Browsing API.
*
* Использует POST-запрос к Google Safe Browsing API (v4), передавая URL для проверки. 
* Если API вернёт ответ, означающий, что URL зарегистрирован в системе Google Safe Browsing,
* то функция верн
* @brief Проверяет наличие и валидность SSL-сертификата у сайта.
*
* Функция пытается установить SSL-соединение на порт 443. Если соединение установить не удаётся,
* сертификат может отсутствовать или быть недействительным.
*
* @param url Полный URL (строка).
* @return Кортеж: (bool, str).
*   - bool — результат проверки (True, если SSL-сертификат действителен).
*   - str — сообщение о результате проверки.
"""

def check_ssl(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc
    try:
        ssl_info = ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=hostname)
        ssl_info.connect((hostname, 443))
        ssl_info.close()
        return True, "SSL-сертификат действителен."
    except Exception as e:
        return False, "SSL-сертификат недействителен."

"""
* @brief Проверяет URL с помощью Google Safe Browsing API.
*
* Использует POST-запрос к Google Safe Browsing API (v4), передавая URL для проверки. 
* Если URL обнаружен в базе вредоносных или фишинговых сайтов, возвращается негативный результат.
*
* Внимание: необходимо указать действительный ключ API в переменной `api_key`.
*
* @param url Полный URL (строка).
* @return Кортеж: (bool, str).
*   - bool — результат проверки (True, если сайт не обнаружен в списке опасных).
*   - str — сообщение о результате проверки.
"""
def check_google_safe_browsing(url):
    api_key = 'YOUR_GOOGLE_API_KEY'
    endpoint = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}'
    body = {
        'client': {
            'clientId': 'yourCompany',
            'clientVersion': '1.0.0'
        },
        'threatInfo': {
            'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING'],
            'platformTypes': ['ANY_PLATFORM'],
            'urlInfo': {
                'urls': [url]
            }
        }
    }
    response = requests.post(endpoint, json=body)
    data = response.json()
    if 'matches' in data:
        return False, "Этот сайт находится в черном списке Google Safe Browsing."
    return True, "Этот сайт безопасен по версии Google Safe Browsing."
