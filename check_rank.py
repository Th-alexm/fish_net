"""
* @file seo_checks.py
* @brief Набор функций для проверки показателей SEO и популярности домена.
*
* В данном модуле представлены функции для:
* - Получения Alexa Rank домена.
* - Проверки, входит ли сайт в топ 1 млн по Alexa Rank.
* - Получения Domain Authority (DA) из Moz API.
"""

import requests
from base64 import b64encode
from bs4 import BeautifulSoup

"""
* @brief Получить Alexa Rank для указанного домена.
*
* Функция отправляет GET-запрос к "https://www.alexa.com/siteinfo/<domain>",
* парсит HTML-страницу и извлекает значение Alexa Rank, если оно присутствует.
*
* @param domain Строка, представляющая домен (например, "example.com").
* @return (int|None, str) Кортеж, где:
*   - int|None: числовое значение Alexa Rank или None, если не получилось извлечь.
*   - str: сообщение о результате операции.
"""

def get_alexa_rank(domain):
    url = f"https://www.alexa.com/siteinfo/{domain}"
    response = requests.get(url)

    if response.status_code != 200:
        return None, "Не удалось получить информацию с Alexa."

    soup = BeautifulSoup(response.text, 'html.parser')
    rank_tag = soup.find('div', {'class': 'rankmini'})  #Проверяем класс, содержащий данные

    if rank_tag:
        rank_text = rank_tag.text.strip().replace(",", "")
        try:
            return int(rank_text.split(' ')[0]), "Alexa Rank найден."
        except ValueError:
            return None, "Ошибка в извлечении Alexa Rank."
    else:
        return None, "Alexa Rank не найден."

"""
* @brief Проверяет, входит ли домен в топ 1 млн по Alexa Rank.
*
* Использует функцию @ref get_alexa_rank, чтобы получить Alexa Rank домена
* и проверяет, не превышает ли он 1,000,000.
*
* @param domain Строка с доменным именем (например, "example.com").
* @return (bool, str) Кортеж, где:
*   - bool: True, если домен входит в топ 1 млн, иначе False.
*   - str: сообщение о результате проверки.
"""

def is_top_1_million(domain):
    rank, message = get_alexa_rank(domain)
    if rank and rank <= 1000000:
        return True, f"Сайт в топ 1 млн Alexa: {rank}"
    else:
        return False, "Сайт не в топ 1 млн Alexa."

"""
* @brief Токены для доступа к Moz API (Domain Authority).
*
* @var MOZ_ACCESS_ID
* @var MOZ_SECRET_KEY
"""

MOZ_ACCESS_ID = 'your_access_id'
MOZ_SECRET_KEY = 'your_secret_key'

"""
* @brief Получить Domain Authority (DA) для домена через Moz API.
*
* Функция отправляет POST-запрос к "https://lsapi.seomoz.com/v2/url_metrics" с указанием домена
* и необходимым параметром 'domain_authority'. Для авторизации использует токены из
* переменных @ref MOZ_ACCESS_ID и @ref MOZ_SECRET_KEY.
*
* @param domain Строка с доменным именем (например, "example.com").
* @return (float|None, str) Кортеж, где:
*   - float|None: Значение Domain Authority или None, если не удалось получить.
*   - str: Сообщение о результате (ошибка или успех с указанием DA).
"""

def get_domain_authority(domain):
    url = "https://lsapi.seomoz.com/v2/url_metrics"
    headers = {
        "Authorization": f"Basic {b64encode(f'{MOZ_ACCESS_ID}:{MOZ_SECRET_KEY}'.encode()).decode()}"
    }

    params = {
        'urls': [f'http://{domain}'],
        'metrics': ['domain_authority']
    }

    response = requests.post(url, headers=headers, json=params)
    if response.status_code != 200:
        return None, "Ошибка при запросе к API Moz."

    data = response.json()
    try:
        da = data[0]['domain_authority']
        return da, f"Domain Authority для {domain}: {da}"
    except KeyError:
        return None, "Не удалось получить Domain Authority."
