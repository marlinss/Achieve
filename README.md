# GitHub Achievement Unlocker

Bu proje, [XTUFE/GitHub-Achievement-Unlocker](https://github.com/XTUFE/GitHub-Achievement-Unlocker)
deposundaki araçları çalıştırmak için düzenlenmiş bir Python projesidir. GitHub'ın
kozmetik profil rozetlerinden **Pull Shark** ve **Pair Extraordinaire**'i, kendi
deponuzda otomatik olarak pull request açıp merge ederek açar.

> ⚠️ **Uyarı:** Bu araçlar yalnızca kozmetik rozetleri etkiler ve GitHub'ın
> katkı grafiğini/etkinliğini yapay olarak şişirir. Yalnızca **kendinize ait,
> kişisel (tercihen public) test depolarında** ve **kendi token'ınızla**
> kullanın. Otomasyon, GitHub'ın kabul edilebilir kullanım politikalarına
> tabidir; kullanım sizin sorumluluğunuzdadır.

## Araçlar

| Script | Rozet | Ne yapar |
|--------|-------|----------|
| `pull_shark.py` | Pull Shark | Döngüde branch açar, dosyayı değiştirir, PR açar ve merge eder |
| `pair_extraordinaire.py` | Pair Extraordinaire | Aynısını yapar ama commit'lere `Co-authored-by` ekler |

## Kurulum

```bash
# 1. Bağımlılıkları kurun
pip install -r requirements.txt

# 2. Yapılandırmayı hazırlayın
cp .env.example .env
# .env dosyasını kendi bilgilerinizle doldurun
```

### Token izinleri

[Fine-grained Personal Access Token](https://github.com/settings/tokens?type=beta)
oluşturun ve hedef depoya şu izinleri verin:

- **Contents:** Read and write
- **Pull requests:** Read and write

Token'ı `.env` dosyasındaki `GH_TOKEN` alanına yazın.

## Kullanım

### Pull Shark

```bash
python pull_shark.py
```

### Pair Extraordinaire

`.env` içinde `GH_COAUTHOR_NAME` ve `GH_COAUTHOR_EMAIL` alanlarını doldurun.
E-posta, gerçek bir GitHub hesabının **doğrulanmış** e-postası olmalı ve o hesap
depoya collaborator olarak eklenmiş olmalıdır.

```bash
python pair_extraordinaire.py
```

## Yapılandırma (`.env`)

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| `GH_TOKEN` | Fine-grained PAT | — |
| `GH_OWNER` | Depo sahibi kullanıcı adınız | — |
| `GH_REPO` | Hedef depo adı | — |
| `GH_FILENAME` | Değiştirilecek dosya | `README.md` |
| `GH_BASE_BRANCH` | PR'ların açılacağı temel branch | `main` |
| `GH_INTERVAL` | İterasyonlar arası bekleme (sn) | `10` |
| `GH_ITERATIONS` | Kaç PR açılacağı (`0` = sonsuz) | `5` |
| `GH_COAUTHOR_NAME` | (Pair) Co-author kullanıcı adı | — |
| `GH_COAUTHOR_EMAIL` | (Pair) Co-author doğrulanmış e-postası | — |

## Proje yapısı

```
.
├── config.py              # Ortak ayarlar + GitHub API yardımcıları
├── pull_shark.py          # Pull Shark unlocker
├── pair_extraordinaire.py # Pair Extraordinaire unlocker
├── requirements.txt
├── .env.example
└── README.md
```

## Nasıl çalışır

Her iterasyon GitHub REST API üzerinden şu adımları izler:

1. `POST /git/refs` — temel branch'ten yeni branch oluştur
2. `GET /contents/{file}` — dosyanın SHA'sını ve içeriğini al
3. `PUT /contents/{file}` — dosyaya bir karakter ekleyip commit et
   (Pair'de `Co-authored-by` trailer ile)
4. `POST /pulls` — pull request aç
5. `PUT /pulls/{n}/merge` — pull request'i merge et
.......