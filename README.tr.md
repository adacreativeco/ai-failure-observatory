# AI Failure Observatory (Yapay Zeka Hata Gözlemevi)

🇺🇸 [English Documentation](README.md)

AI/LLM hata kalıplarını **ürün riski** perspektifinden analiz etmek ve kategorize etmek için geliştirilmiş sistematik bir çerçevedir.

## Bu Nedir?

Yapay zeka sistemleri (özellikle Büyük Dil Modelleri - LLM'ler) güçlüdür ancak kusursuz değildir. Halüsinasyon görebilirler, talimatlardan sapabilirler, bağlamı kaybedebilirler ve hatta kullanıcıları dolaylı olarak yönlendirebilirler. Bu depo şunları sağlar:

| Yetenek | Açıklama |
|---|---|
| **Taksonomi** | Yaygın yapay zeka hata modlarının yapılandırılmış bir sınıflandırması |
| **Tekrarlanabilir Evals** | Belirli hataları tetikleyen ve tespit eden bağımsız test senaryoları |
| **Sentetik Deneyler** | Analiz için kontrollü hata verileri üreten scriptler |
| **Risk Analizi** | Tespit edilen hatalardan kaynaklanan ürün risklerini puanlayan ve raporlayan araçlar |

Tüm bileşenler hafiftir, yerelde çalışır ve büyük ölçekli ML eğitimi gerektirmez.

## Hata Taksonomisi (Sınıflandırması)

```
AI Hata Taksonomisi
├── Çıktı Güvenilmezliği
│   ├── Halüsinasyonlar (Olgusal · Atıf · Parametrik)
│   └── Sahte Güven (Aşırı güvenli yanlış · Yetersiz güvenli doğru)
└── Etkileşim ve Kontrol Hataları
    ├── Manipülasyon (İkna Edici Yönlendirme · Aldatıcı Etkileşim)
    ├── Bağlam Kaybı (Kısa Süreli Bellek · Uzun Vadeli Sapma)
    ├── Özyinelemeli Akıl Yürütme Çöküşü
    └── Yönerge Sapması (Doğrudan Yoksayma · Yanlış Yorumlama · Kademeli Değişim)
```

Her hata türü bir tanım, ürün riski etkileri, önem düzeyi ve alt türler içerir. Tam referans için [`taxonomy/ai_failure_taxonomy.md`](taxonomy/ai_failure_taxonomy.md) dosyasına bakabilirsiniz.

## Kurulum

```bash
git clone https://github.com/adacreativeco/ai-failure-observatory.git
cd ai-failure-observatory

python -m venv venv
source venv/bin/activate   # Windows için: venv\Scripts\activate

pip install -r requirements.txt
```

## İnteraktif Web Arayüzü (Dashboard)

Yapay zeka hata taksonomisini görselleştirmek, tanısal değerlendirmeleri çalıştırmak ve özel girdileri incelemek için interaktif ve duyarlı bir web arayüzü mevcuttur:

```bash
python server.py --port 8088
```

Ardından tarayıcınızda `http://localhost:8088` adresini açın. Arayüz tamamen yerelde çalışır ve yalnızca Python standart kütüphanesini kullanır.

### Arayüz Önizlemesi

#### Risk Analizi Genel Bakış
![Risk Analizi Paneli](dashboard_screenshot.png)

#### Değerlendirme Test Çalıştırmaları
![Değerlendirme Testleri](evals_screenshot.png)

#### Canlı Yanıt Denetleyici
![İnteraktif Test Arayüzü](tester_screenshot.png)

## Hızlı Başlangıç (Komut Satırı)

### 1. Tüm Değerlendirme Testlerini Çalıştırın

```bash
python experiments/reproducible_evals/run_all_evals.py
```

Bu komut, simüle edilmiş LLM yanıtlarını kullanarak hata türü başına birer adet olmak üzere altı yerleşik testi yürütür ve bir özet yazdırır:

```
[PASS] test_hallucination_citation
[PASS] test_fake_confidence
[PASS] test_context_loss
[PASS] test_instruction_drift
[PASS] test_manipulation
[PASS] test_recursive_collapse

6/6 tests passed.
```

### 2. Sentetik Hata Verileri Üretin

```bash
python experiments/synthetic/generate_hallucination_data.py
python experiments/synthetic/generate_context_loss_data.py
python experiments/synthetic/generate_instruction_drift_data.py
```

Çıktılar `data/raw/` dizinine JSON dosyaları olarak kaydedilir.

### 3. Risk Raporu Oluşturun

```bash
python analysis/risk_analysis.py
```

`analysis/reports/risk_report.json` konumunda yapılandırılmış bir JSON raporu ve metin tabanlı bir özet üretir:

```
  hallucinations                   | #########        (score: 9, count: 15)
  manipulation                     | #########        (score: 9, count: 2)
  fake_confidence                  | ####             (score: 4, count: 11)
  instruction_drift                | ####             (score: 4, count: 6)
  context_loss                     | ##               (score: 2, count: 7)
  recursive_reasoning_collapse     | ##               (score: 2, count: 3)
```

### 4. Taksonomiyi Programatik Olarak İnceleyin

```python
from taxonomy.taxonomy_utils import load_taxonomy, get_failure_details

taxonomy = load_taxonomy()
print(get_failure_details("hallucinations"))
```

### 5. Özel Bir Yanıtı Analiz Edin

```python
from src.failure_analyzer import analyze_response

result = analyze_response(
    response="According to Dr. Smith's paper (Smith, 2023)...",
    prompt="Tell me about quantum computing.",
)
print(result["detected_failure"])  # örn: "hallucinations"
```

## Proje Yapısı

```
ai-failure-observatory/
├── data/
│   ├── raw/                        # Üretilen sentetik hata verileri (JSON)
│   └── processed/                  # Analiz için temizlenmiş/yapılandırılmış veriler
├── experiments/
│   ├── synthetic/                  # Sentetik hata üretme scriptleri
│   │   ├── generate_hallucination_data.py
│   │   ├── generate_context_loss_data.py
│   │   └── generate_instruction_drift_data.py
│   └── reproducible_evals/         # Bağımsız hata tespit testleri
│       ├── run_all_evals.py
│       ├── test_hallucination_citation.py
│       ├── test_fake_confidence.py
│       ├── test_context_loss.py
│       ├── test_instruction_drift.py
│       ├── test_manipulation.py
│       └── test_recursive_collapse.py
├── taxonomy/
│   ├── ai_failure_taxonomy.md      # Tam taksonomi tanımı (Markdown)
│   └── taxonomy_utils.py           # Taksonomiyi yüklemek/sorgulamak için araçlar
├── analysis/
│   ├── risk_analysis.py            # Risk puanlama ve rapor oluşturma
│   └── reports/                    # Oluşturulan risk raporları (JSON)
├── src/
│   ├── failure_analyzer.py         # Hevristik tabanlı hata tespit motoru
│   ├── eval_generator.py           # Değerlendirme senaryoları ve test paketi oluşturucu
│   └── utils.py                    # Ortak araçlar (G/Ç, metin analizi vb.)
├── notebooks/                      # İnceleme için isteğe bağlı Jupyter notebookları
├── README.md
└── requirements.txt
```

## Tasarım İlkeleri

- **Hafif (Lightweight)** — Tamamen saf Python, minimum bağımlılık gerektirir ve ML çerçevelerine ihtiyaç duymaz.
- **Yerel Çalışma** — Her şey makinenizde çalışır; yerleşik demolar için bulut API'lerine gerek yoktur.
- **Kavramsal Titizlik** — Her hata türü, ürün riski bağlamıyla birlikte kesin olarak tanımlanmıştır.
- **Tekrarlanabilir** — Her değerlendirme testi deterministik ve bağımsızdır.
- **Genişletilebilir** — Mevcut kalıpları izleyerek kolayca yeni hata türleri, dedektörler veya test senaryoları eklenebilir.

## Gözlemevinin Genişletilmesi

### Yeni Bir Hata Türü Ekleme

1. Bunu `taxonomy/ai_failure_taxonomy.md` dosyasında tanımlayın.
2. `taxonomy/taxonomy_utils.py` içindeki `TAXONOMY` sözlüğüne bir girdi ekleyin.
3. `src/failure_analyzer.py` içinde bir hevristik dedektör fonksiyonu yazın.
4. `src/eval_generator.py` içinde bir `EvalCase` oluşturun.
5. `experiments/reproducible_evals/` dizinine tekrarlanabilir bir test ekleyin.

### Canlı Bir LLM ile Entegre Etme

Değerlendirme scriptlerindeki `SIMULATED_LLM_RESPONSE` sabitlerini gerçek API çağrılarıyla (örn. OpenAI, Anthropic veya yerel modeller) değiştirin. Analiz hattı, gerçek yanıtlar üzerinde de tamamen aynı şekilde çalışacaktır.

## Gelecek Geliştirmeler

- Otomatik canlı değerlendirme için LLM API'leri ile entegrasyon
- Daha gelişmiş risk puanlama modelleri (bağlama duyarlı önem derecesi)
- `matplotlib` / `plotly` kullanan görselleştirme panoları
- Hata tespit doğruluğu için CI tabanlı regresyon testleri
- Topluluk tarafından katkıda bulunulan hata vaka çalışmaları

## Lisans

Apache Lisansı 2.0 - Telif Hakkı 2026 Ada Creative Co. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
