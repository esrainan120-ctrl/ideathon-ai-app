# Vitrion · Akıllı Filtre İzleme (web demo)

`index.html` tek dosyalık, bağımlılıksız bir arayüz prototipidir. Tarayıcıda açmak yeterli.
Tüm veriler **temsili simülasyondur**; eşikler ve tahminler saha testiyle doğrulanmamıştır.

Görünümler: tesis genel bakış, filtre detayı (`#filtre-f-102`), bildirim merkezi, bakım kayıtları,
sensör sağlığı, raporlar (cam / kum karşılaştırması), eşik ve bildirim ayarları, sistem mimarisi.

QR kodu yeniden üretmek için:

    pip install -r requirements-dev.txt
    python tools/make_qr.py <URL> docs/vitrion-demo-qr.png
