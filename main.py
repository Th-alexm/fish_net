from check_basic import check_domain, check_https, get_domain_age
from check_rank import is_top_1_million, get_domain_authority
from urllib.parse import urlparse

def check_phishing(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Проверка домена на известность
    domain_check = check_domain(url)
    if not domain_check:
        return False, "Подозрительный домен."

    # Проверка на наличие https
    https_check, https_message = check_https(url)
    if not https_check:
        return False, https_message

    # Проверка возраста домена
    age = get_domain_age(domain)
    if age is not None and age < 1:  # Например, домен младше 1 года
        return False, "Возраст домена меньше 1 года. Это может быть фишинговый сайт."

    # Проверка Alexa Rank
    in_top_1m, alexa_message = is_top_1_million(domain)
    if not in_top_1m:
        return False, f"Alexa Rank: {alexa_message}"

    # Проверка Domain Authority
    da, da_message = get_domain_authority(domain)
    if da and da < 30:  # Примерное значение, можно корректировать
        return False, f"Domain Authority низкий: {da_message}"

    return True, "Ссылка безопасна."

