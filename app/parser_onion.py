import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector
from bs4 import BeautifulSoup

# Адрес SOCKS-прокси Tor / Tor SOCKS proxy address
TOR_SOCKS_PROXY = "socks5://127.0.0.1:9050"

# Список .onion-сайтов для парсинга / List of .onion sites to parse
ONION_URLS = [
    "http://expyuzz4wqqyqhjn.onion",
    "http://msydqstlz2kzerdg.onion"
]

async def fetch_onion_page(session, url):
    """
    Получает страницу .onion и извлекает её заголовок
    Fetches an .onion page and extracts its title
    """
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                title = soup.title.string if soup.title else "No title"
                print(f"[✓] Onion page title: {title}")
                return {"url": url, "title": title}
            else:
                print(f"[!] Failed: {url} ({response.status})")
                return None
    except Exception as e:
        print(f"[!] Exception on {url}: {e}")
        return None

async def parse_onion_forum_async(limit=3):
    """
    Асинхронно парсит список .onion-страниц
    Asynchronously parses a list of .onion pages
    """
    results = []
    urls = ONION_URLS[:limit]

    # Устанавливаем Tor-прокси / Using Tor proxy
    connector = ProxyConnector.from_url(TOR_SOCKS_PROXY)
    async with aiohttp.ClientSession(connector=connector) as session:
        for url in urls:
            page = await fetch_onion_page(session, url)
            await asyncio.sleep(2)  # Пауза между запросами / Delay between requests
            if page:
                results.append(page)

    return results

def parse_onion_forum(limit=3):  # ← ОБЯЗАТЕЛЕН / REQUIRED for sync compatibility
    """
    Запуск асинхронного парсера в синхронном режиме
    Runs the async parser in a synchronous wrapper
    """
    return asyncio.run(parse_onion_forum_async(limit))

# Пример ручного запуска / Example of manual run
if __name__ == "__main__":
    data = parse_onion_forum(2)
    print(data)
