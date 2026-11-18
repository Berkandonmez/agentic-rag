# Agentic RAG — PusulaFlow

Kurgusal şirket belgeleri üzerinde çalışan yerel bir Türkçe RAG öğrenme projesi.
Belgeler demo verisidir; gerçek bir şirketin hizmet koşullarını temsil etmez.

Sistem, BM25 ve vektör aramasını birleştirir. Agent gerektiğinde ek arama
yapar veya tam belgeyi okur; ardından getirilen kaynaklardan yararlanarak
cevap üretir.

Kaynak kimlikleri ve cevap biçimi kontrol edilir. Bu kontroller, cevabın
anlam bakımından doğru olduğunu garanti etmez.

## Kurulum ve çalıştırma

Proje Python 3.14, PostgreSQL 17 ve pgvector 0.8.7 kullanılarak
geliştirilmiştir. Paket yapılandırması Python 3.14 veya üzerini gerektirir.

Ollama kurulu ve çalışır durumda olmalıdır.

Aşağıdaki komutlar proje kökünde PowerShell üzerinden çalıştırılır.

### 1. Python ortamı

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
```

Geliştirme kurulumu, `src/pusulaflow/` altındaki paketi bu Python ortamına
tanıtır. Bağımlılıklar `requirements.txt` dosyasından alınır.

Komutlarda sanal ortamın Python dosyası doğrudan kullanıldığı için ortamı
ayrıca etkinleştirmek zorunlu değildir.

### 2. Ollama modelleri

```powershell
ollama pull qwen3.5:9b
ollama pull embeddinggemma:300m
```

- `qwen3.5:9b`: Karar ve cevap üretmek için kullanılan sohbet modeli.
- `embeddinggemma:300m`: Belgeleri ve sorguları vektöre dönüştüren model.

Sohbet modelini değiştirmek tek başına belgeleri yeniden indekslemeyi
gerektirmez. Embedding modelini değiştirmek ise mevcut vektörlerle
uyumluluğun değerlendirilmesini ve yeniden indekslemeyi gerektirir.

### 3. PostgreSQL hazırlığı

PostgreSQL sunucusuna pgvector uzantısını kurun.
Python'daki `pgvector` paketi sunucu uzantısını kurmaz.

Kurulum adımları:
[pgvector resmî belgeleri](https://github.com/pgvector/pgvector#installation)

Proje için boş bir veritabanı oluşturun:

```sql
CREATE DATABASE agentic_rag;
```

### 4. Bağlantı ayarları

`.env.example` dosyasını `.env` adıyla kopyalayın:

```powershell
Copy-Item .env.example .env
```

Dosyayı kendi bağlantı bilgilerinizle doldurun:

```dotenv
PGHOST=localhost
PGPORT=5432
PGDATABASE=agentic_rag
PGUSER=postgres
PGPASSWORD=
```

Gerçek parolanızı Git'e eklemeyin.

Ortamda önceden tanımlı bağlantı değişkenleri, `.env` dosyasındaki
değerlerden önceliklidir.

Bu geliştirme kurulumunda `postgres` kullanıcısı kullanılmaktadır.
Üretim ortamı için ayrı kullanıcı ve yetkilendirme düzenlemesi gerekir.

### 5. Veritabanı şeması

```powershell
.\.venv\Scripts\python.exe scripts/migrate.py
```

Bu komut boş veritabanında tabloları ve başlangıç indeks kaydını oluşturur.
pgvector uzantısını etkinleştirebilen ve tablo oluşturabilen bir kullanıcı
gerektirir.

Uygulanmış migration'lar tekrar çalıştırılmaz. Dosyaların checksum
değerleri migration geçmişinde saklanır; uygulanmış bir dosya
değiştirilirse hata verilir.

`--baseline`, daha önce elle oluşturulmuş ve yapısı doğrulanmış
veritabanları içindir. Yeni kurulumda kullanılmaz.

Migration komutu uygulamanın her açılışında çalıştırılmak zorunda değildir;
yeni migration dosyaları olduğunda uygulanır.

### 6. Belgeleri indeksleme

Markdown belgelerini `data/` klasörüne koyup çalıştırın:

```powershell
.\.venv\Scripts\python.exe scripts/index_documents.py
```

Yeni ve içeriği değişen parçaların embedding'leri üretilerek kaydedilir.
Değişmeyen parçalar için yeniden embedding üretilmez.
Kaynaklardan kaldırılan parçaların kayıtları temizlenir.

Belgeleri ekledikten, değiştirdikten veya kaldırdıktan sonra bu komutu
yeniden çalıştırın.

Kaynaklardan hiç parça yüklenemezken veritabanında kayıt bulunuyorsa,
bütün indeksi yanlışlıkla silmemek için işlem durdurulur.

### 7. Soru-cevap uygulaması

```powershell
.\.venv\Scripts\python.exe main.py
```

Çıkmak için `/exit` yazın.

Uygulama başlangıçta embedding modeli adı ve kaynak tutarlılığı
kontrollerini yapar. Kayıtlı parça metinlerini yükleyerek BM25 indeksini
hazırlar. Belge embedding'leri yeniden üretilmez.

## Klasör yapısı ve dosyaların görevleri

Uygulama kodu `src/pusulaflow/` altında bulunur.
`pyproject.toml`, paket kurulumunu ve `requirements.txt` üzerinden
bağımlılıkları tanımlar.

Paket importları `pusulaflow` adıyla yapılır.

| Konum | Görev |
|---|---|
| main.py | Başlangıç kontrollerini yapar ve uygulamayı açar |
| pyproject.toml | Paket, Python sürümü ve kurulum yapılandırması |
| requirements.txt | Sabitlenmiş doğrudan Python bağımlılıkları |
| src/pusulaflow/config.py | Model, indeks adı, proje kökü ve çalışma ayarları |
| src/pusulaflow/documents.py | Markdown belgelerini yükler ve parçalar |
| src/pusulaflow/database.py | PostgreSQL bağlantısı, parça kayıtları ve vektör araması |
| src/pusulaflow/index_validation.py | Kaynaklarla kayıtlı parçaların tutarlılığını kontrol eder |
| src/pusulaflow/retrieval.py | BM25 ve PostgreSQL sonuçlarını RRF ile birleştirir |
| src/pusulaflow/tools.py | Arama, belge listeleme ve tam belge okuma araçları |
| src/pusulaflow/prompts.py | Kaynak kullanma ve cevap verme talimatları |
| src/pusulaflow/agent.py | Model kararlarını alır, araçları yürütür ve cevabı gösterir |
| src/pusulaflow/agent_protocol.py | search, read ve answer kararlarının şeması ve alan kontrolleri |
| src/pusulaflow/citation_validation.py | Kaynak kimliklerini toplama ve kaynak kontrol yardımcıları |
| src/pusulaflow/logging_config.py | Terminal ve boyutu sınırlı dosya logları |
| scripts/migrate.py | Migration dosyalarını uygular ve geçmişini takip eder |
| scripts/index_documents.py | Yeni/değişmiş parçaları indeksler, eski parçaları temizler |
| experiments/ | Manuel bağlantı, embedding, arama ve model denemeleri |
eins| tests/ | Model ve veritabanı çağrıları gerektirmeyen otomatik kontroller |
| migrations/ | Sıralı SQL şema ve başlangıç verisi dosyaları |
| data/ | RAG için okunacak Markdown bilgi kaynakları |
| docs/evaluation.md | Elle değerlendirilen sorular, beklentiler ve sonuçlar |
| .env.example | Bağlantı ayarlarının parolasız şablonu |

`.env`, `data/`, `migrations/` ve `logs/` proje kökünde bulunur.

Bu yollar `config.py` içindeki `PROJECT_ROOT` üzerinden hesaplanır;
terminalin çalışma klasörüne bağlı değildir. README'deki göreli komutlar
ise proje kökünden çalıştırılmalıdır.

### Otomatik testler

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Testler örnek veriler ve taklit model/araç cevaplarıyla kod davranışını
kontrol eder. Gerçek veritabanına veya modele çağrı yapmaz.

Kontroller; parçalama, kaynak değişikliklerinin tespiti, kaynak kimliği
doğrulaması ve agent kararlarının yürütülmesi gibi davranışları kapsar.

Testlerin geçmesi, gerçek modelin cevaplarının doğru olduğunu göstermez.

### Manuel denemeler

Yalnızca ihtiyaç duyulan denemeyi çalıştırın:

```powershell
.\.venv\Scripts\python.exe experiments/check_database.py
.\.venv\Scripts\python.exe experiments/check_embedding.py
.\.venv\Scripts\python.exe experiments/check_vector_search.py
.\.venv\Scripts\python.exe experiments/check_structured_answer.py
.\.venv\Scripts\python.exe experiments/check_tools_schema.py
```

`check_database.py` indeks kaydını okur.
`check_embedding.py`, modeli çağırarak vektör boyutunu kontrol eder.
`check_vector_search.py`, sabit örnek soruyla vektör aramasını sınar.
`check_tools_schema.py`, küçük bir deneme belgesiyle okuma ve cevap
kararlarını inceler.

`check_structured_answer.py`, koşul eşleştirmesi ve doğrudan kaynak
alıntıları içeren deneysel cevap biçimini sınar. Alıntıların getirilen
metinde bulunmasını kontrol eder; koşul eşleştirmesinin veya sonucun
doğruluğunu garanti etmez. Bu yaklaşım ana uygulamaya aktarılmamıştır.

Gereken servisler denemeye göre değişir. Bu denemeler otomatik test
komutunun parçası değildir.

`experiments/tempCodeRunnerFile.py`, editörün bıraktığı tek satırlık bir
deneme parçasıdır; bağımsız çalıştırılabilir bir komut değildir.
İçeriği ve adı korunmuştur.

## Çalışma akışı

### İndeksleme

```text
Markdown belgeleri
→ örtüşen parçalar
→ hash karşılaştırması
→ yeni/değişmiş parçaların embedding'leri
→ PostgreSQL'e kayıt
→ eski parçaların temizlenmesi
```

Hash, embedding üretiminde kullanılan metinden hesaplanır.
İndeksleme sırasında parça ve vektör sayıları ile vektör boyutu
kontrol edilir.

### Soru-cevap

```text
Başlangıç kontrolleri
→ kayıtlı parçaları yükleme
→ BM25 hazırlığı
→ kullanıcı sorusu
→ sorgu embedding'i
→ BM25 ve pgvector araması
→ RRF ile sıralamaları birleştirme
→ komşu parçaları ekleme
→ yapılandırılmış JSON kararı
→ araç işlemi veya cevap
```

İlk arama Python tarafından otomatik yapılır.

Modelin verebileceği kararlar:

- `search`: Eksik bilgi için yeni bir sorguyla arama yapmak.
- `read`: Bilinen bir belgenin tamamını okumak.
- `answer`: Cevabı ve kullanılan kaynak kimliklerini döndürmek.

Model `search` veya `read` kararı verirse Python kararı doğrular,
ilgili fonksiyonu çalıştırır ve sonucu modele gönderir.

`answer` kararında cevap alanlarının biçimi ve kaynak kimlikleri
kontrol edilerek cevap gösterilir. Cevabın anlam bakımından doğruluğu
otomatik olarak doğrulanmaz.

Kaynaklar yeterliyse ilk model çağrısında cevap verilebilir.
Zorunlu taslak veya kontrol turu yoktur.

Aynı arama sonucundaki tekrar eden parça kimlikleri tekilleştirilir.
Adım sınırına ulaşılırsa veya model kararı kontrolleri geçmezse
nihai cevap alınamayabilir.

## Veri modeli

- `rag_indexes`: Embedding modeli adı, vektör boyutu, girdi şablonları
  ve parçalama ayarları.
- `rag_chunks`: Parça metni, belge kimliği, sıra, kaynak yolu,
  içerik hash'i ve embedding vektörü.
- `rag_schema_migrations`: Uygulanan SQL dosyaları, checksum değerleri
  ve uygulanma zamanları.

Mevcut vektör sütunu `vector(768)` olarak tanımlıdır.
Farklı boyutta bir embedding modeline geçmek, veritabanı şemasının
ve indeksleme düzeninin uyarlanmasını gerektirir.

`rag_indexes` içindeki mantıksal indeks kaydı, HNSW gibi bir veritabanı
arama indeksiyle aynı şey değildir.

## Değerlendirme

`docs/evaluation.md`, soruları, beklenen cevapları ve elle incelenen
sonuçları içerir. Bu dosya agent'ın bilgi kaynağına dahil edilmez.

Değerlendirmede şu noktalar ayrı incelenir:

- Nihai sonucun doğruluğu.
- Gerekçenin doğruluğu ve yeterliliği.
- Kaynakların iddiaları desteklemesi.
- Getirilen kaynakların soruyu karşılaması.
- Yanıt süresi ve model çağrısı sayısı.

Doğru sonuçla birlikte yanlış gerekçe verilmesi tam başarı sayılmaz.
Geçerli kaynak kimliği de iddianın desteklendiğini tek başına göstermez.

Mevcut örnekler bütün sorular için başarı garantisi sağlamaz.
Genel bir doğruluk oranı henüz raporlanmamıştır.

## Mevcut sınırlar

- BM25 indeksi uygulama açılırken bellekte yeniden hazırlanır.
- Vektör araması şu anda tam tarama yapar; HNSW veya IVFFlat
  arama indeksi eklenmemiştir.
- Kaynak tutarlılığı başlangıçta kontrol edilir; uygulama açıkken
  yapılan dosya değişiklikleri otomatik izlenmez.
- Her soru yeni mesaj geçmişiyle başlar; sorular arasında sohbet
  hafızası yoktur.
- Kaynak kontrolü kimlik ve biçim kontrolüdür; iddiaların kaynak
  tarafından desteklendiğini veya cevabın doğru olduğunu garanti etmez.
- Model, doğru kaynaklar getirilmiş olsa bile koşulları yanlış
  eşleştirebilir veya kendi içinde çelişen cevap üretebilir.
- Birlikte gereken koşullar, istisnalar ve destek sınıflandırmaları,
  değerlendirme sırasında hata görülen alanlardır.
- Bir soru için en fazla 7 model çağrısı yapılır.
- Araç adları, parametreleri ve süreler terminale; kaynak içerikleri
  ve kararlar boyutu sınırlı `logs/app.log` dosyasına yazılır.
- Embedding modeli kontrolü etiket adına dayanır; aynı etiket
  altındaki ağırlık değişikliklerini tespit etmez.
- Sonuçlar ve süreler modele, donanıma ve getirilen bağlama bağlıdır.

Uygulama, kesin bir hak kazanma veya sözleşme kararı veren sistem
olarak değerlendirilmemelidir.

Modülleri import etmek belge embedding işlemini veya soru döngüsünü
başlatmaz.