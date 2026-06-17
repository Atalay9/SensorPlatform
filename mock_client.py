import time
import random
import requests

# API Yapılandırması
API_URL = "http://127.0.0.1:8000/devices/SN-9942A/telemetry/"
INTERVAL_SECONDS = 10

print("Mock Client Servisi Başlatıldı. Veri gönderimi bekleniyor...")

while True:
    try:
        # 15 ile 90 desibel arasında rastgele ses seviyesi üret
        mock_volume = round(random.uniform(15.0, 90.0), 2)
        payload = {"volume": mock_volume}

        # API'ye POST isteği atılıyor
        response = requests.post(API_URL, json=payload)

        if response.status_code == 201:
            print(f"Başarılı: Ses Seviyesi {mock_volume} dB gönderildi.")
        else:
            print(f"HATA: API {response.status_code} kodu döndü. Mesaj: {response.text}")

    except requests.exceptions.ConnectionError:
        print("HATA: API sunucusuna ulaşılamadı. Uvicorn açık mı?")

    time.sleep(INTERVAL_SECONDS)