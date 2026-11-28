# GitHub Repo Ayarları

Sorumlu: Kişi D (ayarları repo sahibi yapabilir, D yönlendirir).

## 1. Ekip üyelerini ekleme
**Settings → Collaborators → Add people** → 4 kişinin GitHub kullanıcı adı, rol: *Write*.

## 2. `main` dalını koruma
**Settings → Branches → Add branch ruleset** (veya *Add rule*):
- Branch name pattern: `main`
- ✅ Require a pull request before merging → Required approvals: **1**
- ✅ Require status checks to pass → `catkin` (CI işi ilk kez çalıştıktan sonra listede görünür)
- ✅ Do not allow bypassing the above settings (isteğe bağlı)

## 3. Milestone'lar
**Issues → Milestones → New milestone**

| Başlık | Bitiş tarihi |
|---|---|
| Hafta 1 | 4 Aralık 2026 |
| Hafta 2 | 11 Aralık 2026 |
| Hafta 3 | 18 Aralık 2026 |
| Hafta 4 | 25 Aralık 2026 |

## 4. Etiketler
**Issues → Labels**: `gorev`, `kisi-A`, `kisi-B`, `kisi-C`, `kisi-D`, `ortak`, `hata`

## 5. Proje panosu
**Projects → New project → Board**: sütunlar *Yapılacak / Devam ediyor / İncelemede / Bitti*.
Issue'ları panoya ekleyin; PR birleşince ilgili Issue otomatik kapanır (`Closes #N`).

## 6. Issue'ları açma
`docs/hafta1_gorevler.md` içindeki her madde bir Issue olur: başlık, sorumlu (Assignee),
etiket ve **Hafta 1** milestone'u.
