import requests
from bs4 import BeautifulSoup
import re

# Обновленный список публичных paste-сайтов (без капчи)
# Updated list of public paste sites (no captcha required)
SOURCES = [
    "https://pastebin.com/archive",
    "https://controlc.com/archive/",
    "https://cl1p.net/",
    "https://paste2.org/",
    "https://justpaste.it/latest",
    "https://www.pastefs.com/",
    "https://paste.ofcode.org/",
    "https://dpaste.org/",
    "https://paste.ee/",
    "https://throwbin.io/",
    "https://snipplr.com/",
    "https://p.ip.fi/",
    "https://hastebin.com/",
    "https://paste.debian.net/",
    "https://0paste.com/",
    "https://www.toptal.com/developers/hastebin/",
    "https://paste.mozilla.org/",
    "https://pastes.io/",
    "https://paste.re/",
    "https://paste.fedoraproject.org/",
    "https://paste.centos.org/",
    "https://paste.rs/",
    "https://dpaste.com/",
    "https://paste.wireshark.org/",
    "https://paste.april.org/",
    "https://paste.tbee-clan.de/",
    "https://paste.jp/",
    "https://paste.org.ru/",
    "https://kpaste.net/archive"
]

def clean_html_text(html):
    """
    Удаляет HTML-теги и возвращает только текст
    Cleans HTML tags and returns plain text
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n", strip=True)

# Компилируем расширенные шаблоны регулярных выражений
# Compile extended regex patterns for credential detection

# 1. Разделители-символы (двоеточие, точка с запятой и т.д.)
# 1. Symbol-based separators (colon, semicolon, etc.)
pattern_punct = re.compile(
    r'((?:[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+|[A-Za-z0-9_.-]{3,}))'
    r'[^A-Za-z0-9\n\r]{0,10}?'
    r'(?::|;|\||,|=)'
    r'[^A-Za-z0-9\n\r]{0,10}?'
    r'([^\s\n\r]{4,})'
)

# 2. Разделитель-пробел (если логин и пароль разделены пробелом)
# 2. Space separator (when login and password are separated by space)
pattern_space = re.compile(
    r'((?:[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+|[A-Za-z0-9_.-]{3,}))'
    r'\s+'
    r'([^\s\n\r:;|,=]{4,})'
)

def find_pastes(query="email password", limit=5):
    """
    Ищет утечки на публичных paste-сайтах по ключевым словам.
    Searches public paste sites for leaked credentials based on query.
    """
    print(f"[INFO] Поиск по публичным источникам: {query}")
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for source in SOURCES:
        try:
            response = requests.get(source, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)
            print(f"[DEBUG] [{source}] Найдено {len(links)} ссылок.")
            count = 0

            for a in links:
                if count >= limit:
                    break
                href = a["href"]

                # Формирование полного URL пасты / Construct full paste URL
                if href.startswith("/") and not source.endswith(href):
                    paste_url = source.rstrip("/") + href
                elif href.startswith("http"):
                    paste_url = href
                else:
                    paste_url = source.rstrip("/") + "/" + href

                try:
                    paste_resp = requests.get(paste_url, headers=headers, timeout=10)
                    raw_text = clean_html_text(paste_resp.text)

                    # Поиск всех комбинаций логин:пароль / Search all login:password patterns
                    matches = pattern_punct.findall(raw_text) + pattern_space.findall(raw_text)

                    if matches:
                        creds = list(set(f"{login}:{pwd}" for login, pwd in matches))
                        print(f"[DEBUG] Найдено {len(creds)} пар учетных данных в {paste_url}")
                        results.append({"url": paste_url, "credentials": creds})
                        count += 1
                except Exception as e:
                    print(f"[WARN] Не удалось извлечь текст пасты: {paste_url} — {e}")
        except Exception as e:
            print(f"[ERROR] Ошибка при получении архивов {source}: {e}")

    return results
