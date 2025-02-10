from check_basic import check_domain, check_https, get_domain_age
from check_rank import is_top_1_million, get_domain_authority
from check_additional import check_suspicious_characters, check_subdomains, check_ssl, check_google_safe_browsing
from db import insert_result, get_result
from urllib.parse import urlparse

def check_phishing(url):
    # Сначала проверяем в базе данных, есть ли уже результат для данного домена
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    db_result = get_result(domain)
    if db_result:
        return db_result['result'], db_result['message']  # Если результат найден, возвращаем его
    
    # Если результата нет в базе, проводим проверку
    domain_check = check_domain(url)
    if not domain_check:
        result = "Подозрительный домен."
        insert_result(domain, 'unsafe', result)
        return False, result

    https_check, https_message = check_https(url)
    if not https_check:
        insert_result(domain, 'unsafe', https_message)
        return False, https_message

    age = get_domain_age(domain)
    if age is not None and age < 1:
        result = "Возраст домена меньше 1 года. Это может быть фишинговый сайт."
        insert_result(domain, 'unsafe', result)
        return False, result

    in_top_1m, alexa_message = is_top_1_million(domain)
    if not in_top_1m:
        result = f"Alexa Rank: {alexa_message}"
        insert_result(domain, 'unsafe', result)
        return False, result

    da, da_message = get_domain_authority(domain)
    if da and da < 30:
        result = f"Domain Authority низкий: {da_message}"
        insert_result(domain, 'unsafe', result)
        return False, result

    # Новые проверки
    suspicious_characters_check, characters_message = check_suspicious_characters(domain)
    if not suspicious_characters_check:
        insert_result(domain, 'unsafe', characters_message)
        return False, characters_message

    subdomains_check, subdomains_message = check_subdomains(url)
    if not subdomains_check:
        insert_result(domain, 'unsafe', subdomains_message)
        return False, subdomains_message

    ssl_check, ssl_message = check_ssl(url)
    if not ssl_check:
        insert_result(domain, 'unsafe', ssl_message)
        return False, ssl_message

    safe_browsing_check, safe_browsing_message = check_google_safe_browsing(url)
    if not safe_browsing_check:
        insert_result(domain, 'unsafe', safe_browsing_message)
        return False, safe_browsing_message

    # Если все проверки пройдены успешно, сохраняем в базу и возвращаем положительный результат
    result = "Ссылка безопасна."
    insert_result(domain, 'safe', result)
    return True, result
