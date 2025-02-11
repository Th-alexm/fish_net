"""
* @file main.py
* @brief Основной модуль, содержащий функцию для проверки ссылки на фишинг.
*
* Модуль импортирует несколько функций из вспомогательных модулей:
* - check_basic (проверка домена, HTTPS, возраста домена)
* - check_rank (проверка Alexa Rank и Domain Authority)
* - check_additional (дополнительные проверки: подозрительные символы, поддомены, SSL, Google Safe Browsing)
* - db (функции для работы с базой данных)
* - logger (логирование результатов)
*
* В конце создаёт таблицу в БД (через create_db) и предоставляет основную функцию @ref check_phishing для использования.
"""

from check_basic import check_domain, check_https, get_domain_age
from check_rank import is_top_1_million, get_domain_authority
from check_additional import check_suspicious_characters, check_subdomains, check_ssl, check_google_safe_browsing
from db import insert_result, get_result, create_db
from logger import log_check
from urllib.parse import urlparse

#Инициализируем базу данных (если не существует).
create_db()

"""
* @brief Проверяет URL на фишинг, используя различные критерии.
*
* 1. Сначала проверяет, есть ли результат в базе данных (кэш).  
*    - Если найден, возвращается сохранённый результат.  
*    - При этом результат логируется (через @ref log_check).
* 2. Если результата нет, проводится серия проверок:
*    - Проверка домена (@ref check_domain).
*    - Проверка HTTPS (@ref check_https).
*    - Проверка возраста домена (@ref get_domain_age).
*    - Проверка Alexa Rank (@ref is_top_1_million).
*    - Проверка Domain Authority (@ref get_domain_authority).
*    - Проверка подозрительных символов (@ref check_suspicious_characters).
*    - Проверка поддоменов (@ref check_subdomains).
*    - Проверка SSL-сертификата (@ref check_ssl).
*    - Проверка Google Safe Browsing (@ref check_google_safe_browsing).
* 3. В случае, если любая из проверок не пройдена, результат считается "unsafe".
* 4. При успешном прохождении всех проверок сохраняется запись как "safe".
*
* Все результаты, включая ошибки, записываются в базу через @ref insert_result и логируются через @ref log_check.
*
* @param url Строка, содержащая полный URL для проверки (например, "https://example.com").
* @return (bool, str)
*   - bool: True, если ссылка безопасна, False в остальных случаях.
*   - str: Сообщение с описанием результата проверки или ошибкой.

"""
def check_phishing(url):
    # Сначала проверяем в базе данных, есть ли уже результат для данного домена
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    db_result = get_result(domain)
    if db_result:
        log_check(domain, db_result['result'], db_result['message'])  # Логируем найденный результат
        return db_result['result'], db_result['message']  

    # Если результата нет в базе, проводим проверку
    try:
        # 1. Проверка домена
        domain_check = check_domain(url)
        if not domain_check:
            result = "Подозрительный домен."
            insert_result(domain, 'unsafe', result)
            log_check(domain, 'unsafe', result)
            return False, result

        # 2. Проверка HTTPS
        https_check, https_message = check_https(url)
        if not https_check:
            insert_result(domain, 'unsafe', https_message)
            log_check(domain, 'unsafe', https_message)
            return False, https_message

        # 3. Проверка возраста домена
        age = get_domain_age(domain)
        if age is not None and age < 1:
            result = "Возраст домена меньше 1 года. Это может быть фишинговый сайт."
            insert_result(domain, 'unsafe', result)
            log_check(domain, 'unsafe', result)
            return False, result

        # 4. Проверка Alexa Rank (топ 1 млн)
        in_top_1m, alexa_message = is_top_1_million(domain)
        if not in_top_1m:
            result = f"Alexa Rank: {alexa_message}"
            insert_result(domain, 'unsafe', result)
            log_check(domain, 'unsafe', result)
            return False, result

        # 5. Проверка Domain Authority
        da, da_message = get_domain_authority(domain)
        if da and da < 30:
            result = f"Domain Authority низкий: {da_message}"
            insert_result(domain, 'unsafe', result)
            log_check(domain, 'unsafe', result)
            return False, result

        # 6. Проверка подозрительных символов
        suspicious_characters_check, characters_message = check_suspicious_characters(domain)
        if not suspicious_characters_check:
            insert_result(domain, 'unsafe', characters_message)
            log_check(domain, 'unsafe', characters_message)
            return False, characters_message

        # 7. Проверка поддоменов
        subdomains_check, subdomains_message = check_subdomains(url)
        if not subdomains_check:
            insert_result(domain, 'unsafe', subdomains_message)
            log_check(domain, 'unsafe', subdomains_message)
            return False, subdomains_message

        # 8. Проверка SSL-сертификата
        ssl_check, ssl_message = check_ssl(url)
        if not ssl_check:
            insert_result(domain, 'unsafe', ssl_message)
            log_check(domain, 'unsafe', ssl_message)
            return False, ssl_message

        # 9. Проверка Google Safe Browsing
        safe_browsing_check, safe_browsing_message = check_google_safe_browsing(url)
        if not safe_browsing_check:
            insert_result(domain, 'unsafe', safe_browsing_message)
            log_check(domain, 'unsafe', safe_browsing_message)
            return False, safe_browsing_message

        # Если все проверки пройдены успешно
        result = "Ссылка безопасна."
        insert_result(domain, 'safe', result)
        log_check(domain, 'safe', result)
        return True, result
    except Exception as e:
        error_message = f"Ошибка при проверке домена {domain}: {str(e)}"
        log_check(domain, 'error', error_message)
        return False, error_message
