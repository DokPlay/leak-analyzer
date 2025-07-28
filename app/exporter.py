def export_to_txt(data, filename="export.txt"):
    """
    Сохраняет данные в текстовый файл.
    Saves data to a text file.

    :param data: Список словарей или строк для экспорта
                 List of dictionaries or strings to export
    :param filename: Имя файла для записи
                     Output filename
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for item in data:
                if isinstance(item, dict):
                    # Извлекаем URL, если есть / Get URL if available
                    url = item.get("url", "—")
                    f.write(f"URL: {url}\n")
                    
                    # Если есть учетные данные / If credentials are present
                    if "credentials" in item:
                        f.write("Credentials:\n")
                        for cred in item["credentials"]:
                            f.write(f"  {cred}\n")
                    # Если есть email-адреса / If emails are present
                    elif "emails" in item:
                        f.write("Emails:\n")
                        for email in item["emails"]:
                            f.write(f"  {email}\n")
                    else:
                        # Записываем все остальные поля / Write all other fields
                        for key, value in item.items():
                            if key not in ("url", "credentials", "emails"):
                                f.write(f"{key}: {value}\n")

                    f.write("-" * 40 + "\n")
                else:
                    # Если элемент — просто строка / If item is just a string
                    f.write(str(item) + "\n")

        print(f"[✓] Данные успешно сохранены в {filename}")
        # Data successfully saved
    except Exception as e:
        print(f"[!] Ошибка при экспорте в файл: {e}")
        # Error while exporting to file
