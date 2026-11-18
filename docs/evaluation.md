# Değerlendirme Soruları

Bu dosya kurgusal PusulaFlow belgelerine göre beklenen
yanıtları tanımlar. Agent'a bilgi kaynağı olarak verilmez.

## T01 — Kapasite sınırı

Soru: 600 kişilik tek çalışma alanı için hangi paket yeterli?

Beklenen:
- Belgelenmiş paketlerin hiçbiri yeterli değil.
- Temel Paket en fazla 10 kullanıcı destekler.
- Kurumsal Paket en fazla 500 kullanıcı destekler.
- Belgelenmemiş bir üst paket veya istisna önerilmez.

Kaynak: packets.md

## T02 — Kapasite ve özellik ayrımı

Soru: 6 kişiyiz ve SAML SSO ile SCIM gerekiyor. Hangi paket uygun?

Beklenen:
- Kurumsal Paket gerekli.
- Gerekçe kullanıcı sayısı değil, SAML ve SCIM gereksinimleri.
- Temel Paket kapasite açısından yeterli olsa da özellikler eksik.

Kaynak: packets.md

## T03 — P1 ve ek SLA

Soru: Kurumsal Paket ve ek SLA kullanıyoruz. Pazar gecesi tüm kullanıcılar hizmete erişemiyor ve geçici çözüm yok. İlk insan yanıtı taahhüdü nedir?

Beklenen:
- Verilen koşullar P1 tanımına uyar.
- Ek SLA kapsamında en fazla bir saat içinde ilk insan yanıtı.
- Bu süre çözüm garantisi değildir.

Kaynak: destek_politikasi.md

## T04 — Tek kullanıcı sorunu

Soru: Kurumsal Paket ve ek SLA kullanıyoruz. Pazar gecesi yalnızca bir çalışan giriş yapamıyor, diğerleri çalışabiliyor. Bir saatlik yanıt garantisi var mı?

Beklenen:
- Verilen bilgilere göre P3.
- P3 için bir saatlik yanıt garantisi tanımlanmamış.
- Standart çalışma saatleri uygulanır.
- Destek ekibi etkiye göre sınıflandırmayı güncelleyebilir.

Kaynak: destek_politikasi.md

## T05 — Bilinmeyen bilgi

Soru: Kurumsal Paket ve ek SLA'nın toplam aylık fiyatı nedir?

Beklenen:
- Mevcut belgelerde toplam fiyat bulunmuyor.
- Sayısal fiyat veya tahmini ücret üretilmez.

Kaynak: packets.md ve destek_politikasi.md
## Test sonuçları

| Test | Retrieval | Yanıt | Kaynak | Süre | Not |
|---|---|---|---|---|---|
| T03 | Gerekli tanım ve SLA koşulları getirildi | Ana sonuç doğru; olayın P1 ile bağlantısı açık değil | Doğru dosya belirtildi | 15,26 sn | Bir saatlik ilk yanıt ile çözüm süresi doğru ayrıldı |
| T05 | Fiyatın belgede bulunmadığını belirten içerik getirildi | Başarısız: fiyat sorusu yerine politika özeti üretildi; fiyat uydurulmadı | Belge adı anıldı ancak soruya yönelik yanıt yok | 20,68 sn | Sorudan sapma |
| T01 | Kapasite sınırları getirildi | Kısmen başarılı: ana sonuç doğru, desteklenmeyen alternatif önerildi | İlgili kaynaklar belirtildi | 36,61 sn | Tek çalışma alanı şartı sonuç boyunca korunmalı |
| T02 | SAML ve SCIM bilgileri getirildi | Doğru: Kurumsal Paket gerekçesiyle seçildi | Nihai yanıtta kaynak belirtilmedi | 9,50 sn | Cevap doğru, kaynaklandırma eksik |
| T04 | SLA koşulları getirildi, önem düzeyi tanımları eksik | Başarısız: tek kullanıcı sorununa koşullu garanti verdi | Kaynaklar belirtildi | 13,17 sn | Sınıflandırma tanımları doğrulanmadan karar verildi |
| T04 — kontrol turu sonrası | SLA ve önem düzeyi tanımları getirildi | Ana sonuç doğru; P3 açıkça belirtilmedi | İlgili kaynak belirtildi | 62,90 sn | Yanıt tamamlandı; gereksiz koşullu açıklamalar var |
| T05 — kontrol turu sonrası | İki belgedeki fiyat bilgisi eksikliği getirildi | Ana sonuç doğru; yanıt iç değerlendirme biçiminde | İki belge belirtildi | 30,37 sn | Fiyat uydurulmadı; faturalandırma belgesinin varlığı kontrol edilmedi |
| T04 — kısa kanıt özeti sonrası | Sınıflandırma ve SLA koşulları getirildi | Doğru: P3, bir saatlik taahhüt geçerli değil | destek_politikasi.md | 22,44 sn | Model bellekteyken ölçüldü |
| T05 — kısa kanıt özeti sonrası | Destek politikası okundu; paket fiyatı ayrıca araştırılmadı | Ana sonuç doğru; toplam ücretin sözleşmede olduğu iddiası fazla geniş | destek_politikasi.md | 15,33 sn | Fiyat uydurulmadı, paket fiyatı araştırması eksik |
| T04 — tekilleştirme sonrası | Gerekli tanımlar ve SLA koşulları getirildi | Başarısız: sonuç doğru, SLA saatleri yanlış açıklandı | İki belge belirtildi | 23,46 sn | P1 için 7/24 kapsamı yanlış yorumlandı |
| T04 — yapılandırılmış kanıt sonrası | Sınıflandırma ve SLA koşulları getirildi | Başarısız: yanlış sınıflandırma, kullanıcı bilgisini göz ardı etme ve çelişkili cevap | destek_politikasi.md | 31,06 sn | Hata kanıt özetinde başladı |
| T06 — koltuk ve davet | Gerekli kapasite ve davet kuralları getirildi | Ana cevap doğru; bekleyen davetin sayılmadığı açık değil | packets.md | 33,21 sn | Ara özet uzun ve istenen biçimde değil |
| T07 — depolama sınırı | İlgili depolama kuralları getirildi | Ana cevap doğru; satış değerlendirmesinin kabul garantisi olmadığı belirtilmedi | packets.md | 19,21 sn | Çok parçalı soruda başlangıç ifadesi karışık |
## İlk aramayı Python'un başlattığı sürüm

Bu tur boyunca model, prompt ve arama ayarları sabit tutulur.
Model yükleme süresi ayrıca kaydedilir.

| Test | Cevap | Kaynak | Toplam süre | Model yükleme | Not |
|---|---|---|---|---|---|
| T01 — 600 kullanıcı | | | | | |
| T02 — SAML ve SCIM | | | | | |
| T03 — P1 ve ek SLA | | | | | |
| T04 — Tek kullanıcı sorunu | Başarısız | Belirtilmedi | 16,24 sn | 0,07 sn | Evet diye başlayıp koşullarla çelişti; P3 açık değil |
| T05 — Bilinmeyen fiyat | | | | | |
| T01 — 600 kullanıcı | Başarısız | packets.md#chunk-3; kapsam eksik | 12,33 sn | 0,08 sn | Kurumsal kapasitesi doğrulanmadan cevap verildi |
| T02 — SAML ve SCIM | Ana sonuç ve gerekçe doğru | Belirtilmedi | 15,57 sn | 0,08 sn | Kullanıcı bilgisini belge bilgisi gibi ifade etti |
| T03 — P1 ve ek SLA | Kısmen başarılı | Belirtilmedi | 14,40 sn | 0,07 sn | Süre ve kapsam doğru; olayın P1 tanımıyla eşleşmesi açık değil |
| T05 — Bilinmeyen fiyat | Başarılı | packets.md ve destek_politikasi.md | 14,89 sn | 0,08 sn | Fiyat uydurulmadı; gereksiz ürün ayrıntıları var |

## Yapılandırılmış agent akışı — 18 Kasım 2026

Model: qwen3.5:9b
Akış: İlk arama → JSON kararı → gerekirse ek arama veya belge okuma → cevap
Kaynak kimlikleri Python tarafında doğrulanıyor.

### Gerçek model denemeleri

| Senaryo | Beklenen | Gözlenen | Toplam süre | Model çağrısı |
|---|---|---|---:|---:|
| Tek çalışma alanında 600 kullanıcı | Mevcut paketler yetersiz; üst sınır 500 | Doğru sonuç ve kapasite gerekçesi | 7,64 sn | 1 |
| Ek SLA, pazar gecesi yalnızca tek kullanıcı erişemiyor | P1 koşulu karşılanmadığından bir saatlik taahhüt uygulanmaz | Sonuç doğru; gece kapsamı ve P1 gerekçesi birbirine karıştırılmış | 9,29 sn | 1 |
| İmzalı ek SLA, tüm kullanıcılar temel hizmete erişemiyor, geçici çözüm yok | P1; gece dahil en fazla bir saatte ilk insan yanıtı | Temel karar doğru; çözüm süresi ayrımı belirtilmemiş | 11,96 sn | 1 |
| Kurumsal Paket ve ek SLA toplam aylık fiyatı | Mevcut belgelerden hesaplanamaz | Rakam uydurmadan bilgi eksikliğini belirtti | 7,89 sn | 1 |
| 6 kullanıcı, SAML ve SCIM ihtiyacı | Kurumsal Paket | Doğru paket ve özellik gerekçesi | 8,54 sn | 1 |

Bu beş denemede ortalama toplam süre: 9,06 saniye.
Her senaryo bir kez denendi; sonuçlar genel doğruluk oranı değildir.
Cevapların tamamında kaynak listesi döndü.

### Otomatik kontroller

13 test geçti.
Testler parçalama, kaynak değişikliği kontrolü, kaynak kimliği
doğrulaması ve agent kararlarının yürütülmesini kapsıyor.
Gerçek modelin cevap doğruluğunu ölçmüyor.

### Açık kalan noktalar

- Tek kullanıcı senaryosunda doğru sonuç, kısmen hatalı gerekçeyle verildi.
- Geçerli kaynak kimliği, kaynağın cevaptaki iddiayı desteklediğini kanıtlamaz.
- Gerçek modelle ek arama ve tam belge okuma yolları henüz değerlendirilmedi;
  bu yollar otomatik testlerde taklit cevaplarla kontrol edildi.
- Yanıtlarda gereksiz tekrar ve bazen iki kez kaynak gösterimi var.

## Sabit değerlendirme seti

Sorular modele tek tek, yeni soru olarak verilir.
Beklenen cevaplar modelin kaynaklarına veya promptlarına eklenmez.
Deneme sırasında kod ve ayarlar değiştirilmez.

| ID | Soru | Beklenen sonuç ve belirleyici gerekçe |
|---|---|---|
| E01 | Temel Paket kullanıyoruz. 8 aktif, 2 askıya alınmış hesap var. Yeni bir kullanıcı daveti kabul edebilir mi? | Hayır. Askıya alınanlar kapasiteye dahildir; 10 kişilik sınır doludur. |
| E02 | 6 çalışanımız var; SAML oturum açma ve SCIM kullanıcı yönetimi gerekiyor. Hangi paket yeterli? | Kurumsal Paket. Temel Paket kullanıcı sayısına yeter, gerekli özelliklere yetmez. |
| E03 | 600 kullanıcılı tek çalışma alanı için hangi paket yeterli? | Belgelenmiş paketlerin hiçbiri. Kurumsal Paket sınırı 500'dür. |
| E04 | İmzalı ek SLA kullanıyoruz. Pazar gecesi yalnızca bir kullanıcı giriş yapamıyor; diğerleri çalışıyor. Bir saatlik ilk insan yanıtı taahhüdü uygulanır mı? | Hayır. Tek kullanıcı sorunu P3'tür; bir saatlik taahhüt P1 içindir. Gece olması tek başına ret gerekçesi değildir. |
| E05 | İmzalı ek SLA kullanıyoruz. Pazar gecesi tüm kullanıcılar temel hizmete erişemiyor ve kullanılabilir geçici çözüm yok. İlk insan yanıtı taahhüdü nedir? | P1 koşulları karşılanır; gece dahil en fazla bir saat. Çözüm süresi garantisi değildir. |
| E06 | İmzalı ek SLA kullanıyoruz. Tüm kullanıcılar temel hizmete erişemiyor ama kullanılabilir geçici çözüm var. P1 için tanımlanan bir saatlik taahhüt uygulanır mı? | Verilen durum P1 tanımını karşılamaz. Geçici çözüm bulunmaması da gerekir. Kesin P2/P3 sınıfı varsayılmamalıdır. |
| E07 | Kurumsal Paket ve ek SLA'nın toplam aylık fiyatı nedir? | Mevcut belgelerden hesaplanamaz; ücret uydurulmamalıdır. |
| E08 | Dosya depolama kotamız doldu. Mevcut dosyaları okuyabilir ve görevleri güncelleyebilir miyiz? | Evet. Kota yeni dosya yüklemelerini engeller; mevcut dosya okuma ve görev güncellemesini engellemez. |

### Kayıt biçimi

| ID | Sonuç doğru mu? | Gerekçe doğru ve yeterli mi? | Kaynaklar iddiayı destekliyor mu? | Toplam süre | Model çağrısı |
|---|---|---|---|---|---|
| E01 | | | | | |
| E02 | | | | | |
| E03 | | | | | |
| E04 | | | | | |
| E05 | | | | | |
| E06 | | | | | |
| E07 | | | | | |
| E08 | | | | | |

Her değerlendirme alanı: geçti / kısmi / kaldı.
Doğru sonuçla birlikte yanlış gerekçe varsa genel değerlendirme geçti sayılmaz.
Kaynak kimliğinin geçerli olması, iddiayı desteklediğini tek başına kanıtlamaz.
İlk model yükleme maliyeti varsa ayrıca not edilir.
Bu küçük setten genel doğruluk garantisi çıkarılmaz.