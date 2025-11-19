# google_global_ping_plus.py
import csv, time, random
import requests
from urllib.parse import quote
from pathlib import Path

DELAY_BASE = 0.35          # istek arası taban gecikme
RETRIES = 2                # her endpoint için retry sayısı
TIMEOUT = 10
SAVE_CSV = "ping_results.csv"

# Basit random masaüstü UA havuzu
UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
]

# TLD havuzu (kısaltılmış örnek; genişletebilirsin)
TLDS = [
    "com", "tr", "de", "fr", "nl", "co.uk", "it", "es", "ru", "pl", "com.br",
    "ca", "com.au", "co.in", "co.jp", "co.id", "sg", "com.mx", "ch", "be",
    "se", "no", "dk", "fi", "pt", "gr", "cz", "hu", "ro", "bg", "ie", "lv",
    "lt", "ee", "kz", "za"
]

# Çeşitli redirector uçları (param adları farklı olabilir)
ENDPOINT_PATTERNS = [
    # klasik web yönlendirmesi
    "https://www.google.{tld}/url?q=",
    # image context (bazı bölgelerde çalışır)
    "https://www.google.{tld}/url?sa=i&url=",
    # clients1 varyantı (görüntünde var)
    "https://clients1.google.{tld}/url?q=",
    # custom search engine
    "https://cse.google.{tld}/url?sa=t&url=",
    # istersen aç: images.* (bazı bölgelerde /imgres veya farklı param ister)
    # "https://images.google.{tld}/url?sa=i&url=",
]

def read_urls(file_path="urls.txt"):
    p = Path(file_path)
    if not p.exists():
        print(f"[HATA] {file_path} bulunamadı.")
        return []
    urls = []
    for line in p.read_text(encoding="utf-8").splitlines():
        u = line.strip()
        if not u:
            continue
        urls.append(u)
    return urls

def ping_once(sess: requests.Session, full_url: str):
    try:
        r = sess.get(full_url, timeout=TIMEOUT, allow_redirects=False)
        return True, r.status_code
    except requests.RequestException as e:
        return False, str(e)

def backoff_sleep(attempt: int):
    # küçük jitter’lı backoff
    time.sleep(DELAY_BASE * (attempt + 1) + random.uniform(0, 0.2))

def main():
    targets = read_urls("urls.txt")
    if not targets:
        return

    # Log dosyası
    csv_file = open(SAVE_CSV, "w", newline="", encoding="utf-8")
    writer = csv.writer(csv_file)
    writer.writerow(["target", "endpoint", "tld", "status", "info"])

    total = ok = fail = 0
    sess = requests.Session()

    for i, url in enumerate(targets, 1):
        enc = quote(url, safe="")
        print(f"\n=== [{i}/{len(targets)}] TARGET: {url} ===")
        random.shuffle(TLDS)  # dağılımı random yap

        for tld in TLDS:
            # UA ve Accept-Language’i TLD’ye göre hafifçe değiştir
            sess.headers.update({
                "User-Agent": random.choice(UAS),
                "Accept-Language": "en-US,en;q=0.9,tr-TR;q=0.8",
            })

            for pat in ENDPOINT_PATTERNS:
                full = pat.format(tld=tld) + enc
                total += 1

                # retries
                success = False
                info_msg = ""
                for attempt in range(RETRIES + 1):
                    ok1, info = ping_once(sess, full)
                    if ok1:
                        success = True
                        info_msg = str(info)
                        break
                    else:
                        info_msg = str(info)
                        backoff_sleep(attempt)

                if success:
                    ok += 1
                    print(f"  ✓ {full} -> {info_msg}")
                    writer.writerow([url, pat, tld, "OK", info_msg])
                else:
                    fail += 1
                    print(f"  ✗ {full} -> {info_msg}")
                    writer.writerow([url, pat, tld, "FAIL", info_msg])

                # temel delay + jitter
                time.sleep(DELAY_BASE + random.uniform(0, 0.15))

    csv_file.close()
    print("\n" + "="*64)
    print(f"İŞLEM TAMAM — Toplam ping denemesi: {total} | Başarılı: {ok} | Başarısız: {fail}")
    print(f"Pinglenen Google endpoint sayısı: {total}")
    print("Başka emriniz var mıdır Batı Bey?")

if __name__ == "__main__":
    main()