# PusulaFlow Paketleri

Belge kimliği: PKT-001
Sürüm: 1.0
Geçerlilik tarihi: 2026-11-01
Belge sahibi: Ürün Operasyonları
Veri niteliği: Demo için oluşturulmuş kurgusal şirket verisi

## Ürün hakkında

PusulaFlow, şirketlerin projelerini, görevlerini ve ekip içi iş
akışlarını yönetmek için kullandığı bulut tabanlı bir platformdur.
Çalışma alanlarında projeler, görev panoları, dosyalar ve kullanıcı
yetkileri birlikte yönetilir.

Bu belge Temel ve Kurumsal paketlerin özelliklerini açıklar.
Destek hizmetlerinin çalışma saatleri ve yanıt süresi taahhütleri
ayrı destek politikası belgesinde tanımlanır. Veri yerleşimi ve
yedekleme ayrıntıları için güvenlik belgesine başvurulmalıdır.

## Kullanıcı kapasitesi nasıl hesaplanır?

Kullanıcı kapasitesi, bir çalışma alanındaki aktif ve askıya
alınmış hesapların toplamıdır. Askıya alma işlemi lisans koltuğunu
serbest bırakmaz. Kullanıcı hesabı çalışma alanından kaldırıldığında
ilgili koltuk yeniden kullanılabilir.

Gönderilmiş fakat henüz kabul edilmemiş davetler kapasiteye dahil
değildir. Davet kabul edilirken boş koltuk bulunması gerekir.
Kapasite doluysa davet kabul işlemi tamamlanamaz.

Her paket sınırı tek bir çalışma alanı için geçerlidir. Birden fazla
çalışma alanındaki kapasiteler birleştirilemez. Aynı kişinin iki ayrı
çalışma alanına eklenmesi, her alanda ayrı bir koltuk kullanır.

## Temel Paket

Temel Paket, küçük ekiplerin görev ve proje takibi için sunulur.
Bir çalışma alanında en fazla 10 kullanıcı desteklenir. Toplam
dosya depolama kapasitesi çalışma alanı başına 20 GB'dır; bu miktar
kullanıcı başına verilen bir alan değildir.

Paket; görev panoları, proje takvimi, dosya ekleri ve standart
aktivite geçmişini içerir. Çalışma alanı yöneticileri kullanıcı
ekleyebilir, kullanıcı kaldırabilir ve proje erişimlerini
düzenleyebilir.

Temel Paket'te e-posta ve parola ile oturum açılır. SAML tabanlı
tek oturum açma ve SCIM üzerinden otomatik kullanıcı yönetimi bu
pakete dahil değildir. Destek kanalı e-postadır. Telefon desteği
Temel Paket kapsamında sunulmaz.

Temel Paket için kullanıcı sınırını artıran ek koltuk satın alımı
bulunmaz. On kullanıcı sınırını aşacak ekiplerin paket değişikliği
yapması gerekir.

## Kurumsal Paket

Kurumsal Paket, merkezi erişim yönetimine ihtiyaç duyan daha büyük
ekipler için sunulur. Bir çalışma alanında en fazla 500 kullanıcı
desteklenir. Toplam depolama kapasitesi çalışma alanı başına 1 TB'dır.

Kurumsal Paket, Temel Paket özelliklerine ek olarak SAML tabanlı
tek oturum açma, SCIM kullanıcı sağlama, özel rol tanımları ve
denetim kayıtlarını dışa aktarma özelliklerini içerir.

Destek kanalları öncelikli e-posta ve telefondur. Öncelikli destek
ifadesi tek başına belirli bir sürede yanıt veya çözüm garantisi
anlamına gelmez. Yanıt süresi taahhüdü için ayrıca imzalanmış bir
SLA gerekir. Telefon desteği de otomatik olarak yedi gün yirmi dört
saat hizmet verildiği anlamına gelmez.

Kurumsal Paket için bu belgede tanımlanan kapasite 500 kullanıcıdır.
Altı yüz kullanıcı gerektiren tek bir çalışma alanı bu sınırın
dışındadır. Belgelenmiş bir üst paket veya kapasite istisnası
bulunmadığından, asistan böyle bir seçeneğin mevcut olduğunu
varsaymamalıdır.

## Depolama sınırları

Dosya depolama kapasitesine projelere yüklenen ekler dahildir.
Metin biçimindeki görev açıklamaları depolama kotasına dahil değildir.
Kotanın dolması yeni dosya yüklemelerini engeller; mevcut dosyaların
okunmasını veya görevlerin güncellenmesini engellemez.

Ek depolama satın alımı bu standart paketlerin kapsamında
tanımlanmamıştır. Standart koşullar dışındaki talepler satış ekibi
tarafından ayrıca değerlendirilir; değerlendirme yapılması talebin
kabul edileceği anlamına gelmez.

## Paket seçimi ve değişiklik

Paket önerilirken kullanıcı sayısının yanında SSO, kullanıcı
otomasyonu, depolama ve destek kanalı ihtiyaçları değerlendirilmelidir.


Paket değişikliği çalışma alanı sahibi tarafından başlatılır.
Kurumsal Paket'ten Temel Paket'e geçebilmek için kullanıcı sayısı
10'u, kullanılan depolama ise 20 GB'ı aşmamalıdır. SAML SSO ve SCIM
entegrasyonlarının kapatılması da gerekir.

Ücretler, ödeme dönemleri ve paket değişikliğinin faturaya etkisi
bu belgede yer almaz. Bu konular için faturalandırma belgesine
başvurulmalıdır.