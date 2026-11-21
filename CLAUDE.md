# Vitrion (Smart Glass) · Proje hafızası

Bu dosya, gelecekteki Claude oturumlarının projeyi baştan anlatmaya gerek kalmadan devam edebilmesi
için tutulur. Yeni bir karar alındığında buraya eklenmeli. Depo **public** olduğu için buraya kişisel
bilgi, şifre, müşteri adı veya gizli iş bilgisi yazılmaz.

## Proje özeti
- **Smart Glass** (marka adayı: **Vitrion**): atık camı endüstriyel su filtrasyonu için granül filtre
  medyasına dönüştüren, filtre performansını sensörlerle ölçen ve dijital arayüzde izleyen CleanTech /
  WaterTech girişimi. 5 ortaklı öğrenci ekibi.
- Üç bileşen: (1) geri kazanılmış cam filtre medyası (ilk deneme tane boyu 0,5–1 mm, kesin değil),
  (2) sensörlü ölçüm, (3) kayıt, görselleştirme ve öngörücü bakım yazılımı.
- Birincil hedef: fabrikalar ve büyük sanayi kuruluşlarının su filtrasyon süreçleri (B2B).
- Geçmiş: Şişecam "Geleceğe İlerleyen Kadınlar" ideathonu (En Güçlü İş Modeli ödülü), Habitat
  Derneği GENU hızlandırma programı, Demo Day'de UNICEF'e sunum (Kasım 2026).

## Dürüstlük kuralı (çok önemli)
Proje dosyası bilgileri üç statüde ayırır: MEVCUT / PLANLANAN / DOĞRULANACAK. Arayüz ve sunumlarda:
- Simülasyon verisi her zaman **"temsili"** diye etiketlenir.
- "%95 tahmin doğruluğu", kesin kalan ömür, çalışan otomatik geri yıkama, cam medyanın kumdan üstün
  olduğu gibi iddialar **doğrulanmış sonuç gibi yazılmaz**. Bunlar geliştirme hedefidir.
- Bulanıklık azalması mikroorganizma veya kimyasal giderimini kanıtlamaz.

## Sensörler ve donanım (ilk prototip önerisi)
| Etiket | Ölçüm | Prototip | Pilot alternatifi |
|---|---|---|---|
| PT-in, PT-out | Giriş/çıkış basıncı (ΔP = P1 − P2) | 2× DFRobot SEN0257 (0–1,6 MPa, 0,5–4,5 V) | 4–20 mA transmitter (ör. ATEK BCT22) |
| FT | Debi, toplam hacim | 1× YF-S201 (çıkış hattında) | Darbe çıkışlı mekanik sayaç DN15/DN20 |
| TU-in, TU-out | Bulanıklık | 2× DFRobot SEN0189 + akış hücresi | RS485/Modbus IP68 NTU probu |

- ESP32 + ADS1115 (16 bit ADC). 5 V analog sinyaller ESP32'ye doğrudan bağlanmaz (gerilim bölücü).
- Bağlantı koparsa microSD'ye yerel kayıt. Elektronik ön bütçe ≈ 13.734 TL (canlı teklif değil;
  pompa, kolon, cam medya, işçilik hariç).

## Hesaplamalar
- ΔP = P_giriş − P_çıkış
- **Debiye göre düzeltilmiş ΔP** = ΔP × Q_nominal / Q (farklı debideki ΔP farkı tıkanma sayılmaz;
  eşikler ve tahmin bu değeri kullanır).
- Tıkanma % = (ΔP_düz − ΔP_temiz) / (ΔP_alarm − ΔP_temiz) × 100
- Bulanıklık azalması % = (T_giriş − T_çıkış) / T_giriş × 100 (T_giriş > 0)
- Tahmin: son geri yıkamadan sonraki en fazla 120 dakikalık ΔP_düz'e doğrusal regresyon.
  Güven: n < 40 veya R² < 0,5 → düşük; R² < 0,8 → orta; değilse yüksek. Düşük güvende öngörü
  bildirimi gönderilmez.

## Bildirim kuralları (arayüzde uygulanan)
- Uyarı / alarm için ardışık 3 ölçüm şartı; seviye düşüşünde 0,03 bar histerezis.
- 15 dakika onaylanmayan alarm vardiya şefine eskale edilir.
- Öngörü bildirimi: alarma tahmini süre < 2 saat.
- Rol × seviye × kanal matrisi: Operatör, Bakım ekibi, Vardiya şefi, Tesis müdürü;
  Öngörü, Uyarı, Alarm, Sensör hatası; Panel, E-posta, SMS, Günlük özet.
- Panel geri yıkamayı uzaktan **başlatmaz**, sadece bakım kaydı açar.

## Sistem mimarisi
Sensörler → ESP32 (5 sn örnekleme, 1 dk ortalama, microSD tampon) → MQTT (TLS, QoS 1) →
Python veri alma/doğrulama → zaman serisi DB (pilot: SQLite/CSV, tesis: TimescaleDB) →
kural ve tahmin motoru → panel + bildirim servisi (e-posta, SMS, Teams) → SCADA/PLC (Modbus TCP / OPC UA).
MQTT konuları: `vitrion/{tesis}/{hat}/{filtre}/telemetri|durum|olay`, `vitrion/{tesis}/cihaz/{esp32_id}/saglik`.

## Marka kimliği
- Logo: "N" biçiminde zikzak çizgi, dalgaya dönüşüp kesikli çizgili bir damla ile biter;
  kelime işareti küçük harf **vitrion**, yuvarlak tek kalınlıkta harfler, "i" noktaları damla.
- Renk paleti (ekibin seçtiği):
  - Prusya mavisi `#103A57` (ana koyu, yan menü)
  - Teal mavi `#307B8E` (vurgu, butonlar)
  - Pastel mavi `#A9D3C5`
  - Açık gümüş `#CEE5D6`
  - Mughal yeşili `#366B2B` (arayüzde "normal" durumu)
- Durum renkleri ayrı: uyarı `#B7790F`, alarm `#B3362C`.
- Yazı tipleri: başlık/logo Comfortaa, gövde IBM Plex Sans, sayısal etiketler IBM Plex Mono.
- Ekibin logo renk alternatifleri sayfasında 8 seçenek vardı (Grey Blue/Dark Azure, Spring Meadow/Teal
  Waters, Aquamarine, Deep Blue/Ocean City, Cool Jade/Sky Aqua, Caribbean/Linen, Delft Blue/Pistachio,
  Metalik gri); nihai seçim henüz bildirilmedi.

## Depodaki dosyalar
- `app.py` — ilk Streamlit ΔP demosu (ekibin eski çalışması; henüz marka renklerine taşınmadı).
  E-posta şifresini arayüzden alıyor; ileride bildirim servisine taşınmalı.
- `web/index.html` — tek dosyalık, bağımlılıksız izleme arayüzü (asıl kaynak).
- `docs/index.html` — GitHub Pages yayın kopyası. **`web/index.html` değişince bu da güncellenmeli**
  (`cp web/index.html docs/index.html`).
- `docs/vitrion-demo-qr.png` — GitHub Pages linkine QR; `docs/vitrion-demo-qr-claude.png` — claude.ai linkine QR.
- `tools/make_qr.py` — marka renklerinde QR üretir: `python tools/make_qr.py <URL> <çıktı.png>`.
- `requirements.txt` (uygulama), `requirements-dev.txt` (qrcode).

### Arayüz görünümleri (`web/index.html`, hash yönlendirme)
`#genel` tesis genel bakış (4 hat, 8 filtre kartı, yatak kesiti animasyonu) · `#filtre-f-102` filtre
detayı · `#bildirimler` · `#bakim` · `#sensorler` · `#raporlar` (vardiya raporu + cam/kum
karşılaştırması) · `#ayarlar` (eşikler + bildirim matrisi) · `#mimari` (veri akışı + "neyi neden ekledik").
Demo filtreleri: F-101/102 cam, F-103 referans kum (L1 proses suyu); F-201/202 (L2 soğutma kulesi);
F-301 (L3 kazan besleme); F-401 (TU-out sensör arızası örneği)/402 (L4 atıksu geri kazanım).

## Yayın linkleri
- GitHub Pages: https://esrainan120-ctrl.github.io/vitrion/ (Settings → Pages → main, /docs). Depo adı `ideathon-ai-app` → `vitrion` olarak değiştirildi; eski Pages adresi yönlenmez.
- claude.ai artifact (sahibine özel, Share ile açılır): https://claude.ai/artifact/XxcZ6TpgyNu9WrWv3e3Xak

## Bulut ortamı
- Claude Code ortamı: `ideathon-ai-app` (kişisel). Kurulum betiği `requirements.txt` ve
  `requirements-dev.txt` kurar. Değişkenler: `STREAMLIT_SERVER_HEADLESS=true`,
  `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`. Ek ağ adresi ve gizli anahtar yok.

## Açık işler / sonraki adımlar
- `app.py` Streamlit uygulamasını aynı tasarıma ve renklere taşımak; ESP32'den gerçek veri almak
  (seri port veya MQTT).
- Gerçek eşikleri saha/kontrollü testten sonra belirlemek.
- Bildirimler için HTTPS tabanlı servis seçmek (SendGrid, Twilio, Telegram vb.); anahtarlar koda
  veya bu dosyaya değil ortamın gizli anahtarlarına konur.
- Logo için nihai renk seçeneği gelince arayüzü güncellemek.

## Karar geçmişi (19 Kasım 2026 oturumu)
1. Proje dosyası okundu; mevcut `app.py` incelendi.
2. Fabrika ihtiyaçlarına göre izleme arayüzü tasarlandı (`web/index.html`), marka renkleri uygulandı,
   eklenen her özelliğin gerekçesi `#mimari` sayfasındaki tabloya yazıldı.
3. claude.ai linki ve QR kod üretildi; ardından herkesin girişsiz açabilmesi için GitHub Pages'e geçildi
   ve QR yeni linke göre yeniden üretildi.
4. Bulut ortamı `ideathon-ai-app` oluşturuldu (kullanıcı onayıyla).
5. Claude GitHub App depoya kuruldu; PR #1 `main`'e birleştirildi.
6. Bu hafıza dosyası eklendi.
