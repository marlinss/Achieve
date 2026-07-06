Achieve

## Araçlar

| Script | Rozet | Ne yapar |
|--------|-------|----------|
| `pull_shark.py` | Pull Shark | Döngüde branch açar, dosyayı değiştirir, PR açar ve merge eder |
| `pair_extraordinaire.py` | Pair Extraordinaire | Aynısını yapar ama commit'lere `Co-authored-by` ekler |



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

..................................................