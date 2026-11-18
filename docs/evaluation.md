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

## Sabit değerlendirme seti — 19 Kasım 2026

### Çalıştırma koşulları

- Sohbet modeli: qwen3.5:9b
- Embedding modeli: embeddinggemma:300m
- num_ctx: 8192
- num_predict: 1024
- temperature: 0
- Ana uygulamada think: false
- Kayıtlı parça sayısı: 14
- Soru sayısı: 8
- Her soru yeni mesaj geçmişiyle işlendi.
- Soruların Türkçe karakterleri kontrol edildi.
- Çalıştırma boyunca ayarlar değiştirilmedi.

### Sonuçlar

| ID | Sonuç ve gerekçe değerlendirmesi | Genel değerlendirme | Toplam süre | Model çağrısı |
|---|---|---|---:|---:|
| E01 | Aktif ve askıdaki hesapları birlikte saydı; kapasite doluluğunu doğru uyguladı. | Geçti | 11,72 sn | 1 |
| E02 | Kurumsal Paket seçimi ve özellik açıklaması doğru. İlk cümlede seçimi 6 çalışan bulunmasına bağlaması özensiz. | Kısmi | 6,89 sn | 1 |
| E03 | Mevcut paketlerin yetersiz olduğunu ve 500 kullanıcı üst sınırını doğru belirtti. | Geçti | 6,79 sn | 1 |
| E04 | “Uygulanmaz” sonucu doğru; tek kullanıcı sorununu P1/P2/P3 olarak belirsizleştirdi ve imzalı SLA bilgisine rağmen standart saatleri gerekçeye karıştırdı. | Kaldı | 17,40 sn | 1 |
| E05 | Bir saatlik taahhüdü söyledi; ardından kapsamı hafta içiyle sınırlayıp pazar gecesi için garanti bulunmadığını ileri sürdü. Cevap çelişkili. | Kaldı | 12,61 sn | 1 |
| E06 | Geçici çözüm nedeniyle P1 koşulunun sağlanmadığını doğru açıkladı; yeterli dayanak olmadan kesin P2 sınıflandırması ekledi. | Kaldı | 10,76 sn | 1 |
| E07 | Mevcut belgelerden toplam fiyatın hesaplanamayacağını doğru söyledi; sözleşme ve faturalandırma yönlendirmelerini genelleştirdi. | Kısmi | 8,13 sn | 1 |
| E08 | Kotanın yalnızca yeni yüklemeleri engellediğini, okuma ve görev güncellemesini engellemediğini doğru söyledi. | Geçti | 6,34 sn | 1 |

### Süre ölçümleri

- Sekiz sorunun toplam süresi: 80,64 saniye.
- Soru başına ortalama toplam süre: 10,08 saniye.
- En kısa toplam süre: 6,34 saniye.
- En uzun toplam süre: 17,40 saniye.
- Ortalama sorgu embedding süresi: 2,28 saniye.
- Ortalama LLM çağrısı süresi: 7,79 saniye.
- Model yükleme süreleri 0,07–0,26 saniye arasındadır.
  Bu çalıştırma, modelin ilk yükleme maliyetini temsil etmez.

### Yorum

Bu sekiz örnekte 3 cevap geçti, 2 cevap kısmi değerlendirildi,
3 cevap ise hatalı veya desteklenmeyen gerekçeler içerdiği için kaldı.

Bu sonuçlar genel bir doğruluk oranı değildir. Değerlendirme küçük,
önceden bilinen bir soru seti üzerinde, tek çalıştırmaya dayanır.

Kaynak kimlikleri döndürüldü; ancak bu kayıt tek başına bütün
iddiaların kaynaklar tarafından desteklendiğini kanıtlamaz.

Doğrudan özellik ve kapasite soruları daha başarılıdır.
Birlikte gereken koşullar, sınıflandırmalar ve istisnalar hata
görülen alanlardır.


## Cevap uzunluğu sınırı denemesi — 19 Kasım 2026

Amaç: Nihai cevap alanına 600 karakter sınırı koyarak üretim
süresini azaltmak ve cevapların yeterliliğini karşılaştırmak.

Model, promptlar ve arama ayarları değiştirilmedi.

| Ölçüm | Sınırsız cevap | 600 karakter sınırı |
|---|---:|---:|
| Ortalama toplam süre | 10,08 sn | 7,27 sn |
| Sekiz sorunun toplam süresi | 80,64 sn | 58,14 sn |

### Gözlemler

- E01, E04 ve E05 cevapları cümle tamamlanmadan sona erdi.
- Çıktılar geçerli JSON biçimindeydi ve bitiş nedeni `stop` idi.
  Bu durum, cevap metninin tamamlanmış olduğunu göstermedi.
- E04, E05 ve E06'daki anlam ve gerekçe hataları devam etti.
- Embedding ve girdi işleme süreleri de değiştiği için süre
  farkının tamamı karakter sınırına bağlanamaz.

### Karar

Değişiklik kabul edilmedi. Daha kısa süreye rağmen yarım cevaplar
oluştuğu ve doğruluk iyileşmesi gösterilmediği için 600 karakter
sınırı kaldırıldı.

Sınıra ait iki test kaldırıldı; kalan 13 otomatik test geçti.

Ham çıktı: [600 karakter sınırı denemesi](evaluation-run-d1648913.txt)

## Ölçülen sonuçlar

qwen3.5:9b ile sekiz soruluk sabit değerlendirme seti çalıştırıldı.
Her soru yeni mesaj geçmişiyle, aynı model ve arama ayarlarıyla işlendi.

| Ölçüm | Sonuç |
|---|---:|
| Soru sayısı | 8 |
| Ortalama toplam yanıt süresi | 10,08 sn |
| En kısa yanıt süresi | 6,34 sn |
| En uzun yanıt süresi | 17,40 sn |
| Soru başına model çağrısı | 1 |

Model, bu çalıştırmada büyük ölçüde bellekteydi; süreler ilk model
yükleme maliyetini temsil etmez.

Kapasite ve özellik sorularında doğru cevaplar elde edildi.
Koşul eşleştirme, sınıflandırma ve istisna yorumlamada hatalar görüldü.
Bu küçük soru setinden genel bir doğruluk oranı çıkarılmamıştır.

600 karakterlik cevap sınırı denemesinde ortalama süre 7,27 saniyeye
düştü; ancak yarım cevaplar oluştu ve anlam hataları devam etti.
Girdi işleme ve embedding süreleri de değiştiğinden farkın tamamı
karakter sınırına bağlanamaz. Değişiklik geri alındı.

- [Ayrıntılı değerlendirme](docs/evaluation.md)
- [Başlangıç ölçümünün ham çıktısı](docs/evaluation-run-1f696ce3.txt)
- [Reddedilen karakter sınırı denemesinin ham çıktısı](docs/evaluation-run-d1648913.txt)
## Ayrı ortamda paket kurulumu kontrolü — 19 Kasım 2026

GitHub deposu ayrı bir klasöre klonlandı. Yeni bir Python sanal
ortamında `pip install -e .` ile kurulum tamamlandı ve 13 otomatik
test geçti. Kontrol aynı bilgisayarda yapıldı; veritabanı kurulumu,
migration, indeksleme ve gerçek model çağrısı kapsam dışında kaldı.