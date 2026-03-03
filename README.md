# VirusTotal vt-py — учебный скрипт (file/url scan)

Небольшой скрипт на Python, который обращается к VirusTotal API через **официальную библиотеку vt-py**:
- отправляет файл на проверку
- выводит **JSON-ответ** в консоль

---

## Требования
- Python **3.7+**
- API-ключ VirusTotal
---

## Установка
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows PowerShell

pip install -r requirements.txt
