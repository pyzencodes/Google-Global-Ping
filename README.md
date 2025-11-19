[![GitHub stars](https://img.shields.io/github/stars/pyzencodes/Google-Global-Ping?style=flat-square)](https://github.com/pyzencodes/Google-Global-Ping/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/pyzencodes/Google-Global-Ping?style=flat-square)](https://github.com/pyzencodes/Google-Global-Ping/issues)
![Python version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/license-Private%20Use-red?style=flat-square)


---

````markdown
# Google Global Ping Plus

Private utility script that performs multi-TLD ping requests to various Google redirect endpoints using randomized headers and delay logic.  
Used for testing global response coverage for a list of URLs.

> ⚠️ Private internal tool — do **NOT** share publicly.

---

## 📝 Overview

- Reads target URLs from `urls.txt`
- Sends requests over multiple Google domains (**TLD rotation**)
- Uses random User-Agent and variable delays per request
- Retries requests with simple backoff
- Saves results into `ping_results.csv` (status logs)
- Console output shows OK / FAIL per endpoint

---

## ⚙️ Setup

### Requirements
- Python **3.8+**
- `requests` module

Install dependency:
```bash
pip install requests
````

### Required files

* `google_global_ping_plus.py` (this script)
* `urls.txt` → list of URLs (one per line)

Example `urls.txt`:

```
https://example.com
https://domain.com/page
```

---

## ▶️ Usage

Run:

```bash
python google_global_ping_plus.py
```

Results:

```
ping_results.csv   # request logs with statuses
console output     # real-time OK / FAIL feedback
```

---

## 📂 Output Example (CSV)

| target                                     | endpoint            | tld | status | info |
| ------------------------------------------ | ------------------- | --- | ------ | ---- |
| [https://example.com](https://example.com) | google.{tld}/url?q= | com | OK     | 302  |

---

## ⚠️ Notes

* Only intended for internal testing and research
* Not designed for automation at large scale
* Respect network limits and legal usage policies

---

```

## License

Google Global Ping Plus is provided for internal testing and research only.  
All rights reserved. You may not reuse, modify, redistribute, or offer this tool as a service without explicit permission from the author.

