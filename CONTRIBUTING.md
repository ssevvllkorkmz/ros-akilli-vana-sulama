# Katkı Kuralları

## Dallar
- `main` korumalıdır: doğrudan push yok, yalnızca PR ile birleştirme.
- Dal adı: `feature/<kisi>-<konu>` (ör. `feature/a-open-meteo-client`), hata için `fix/...`.

## Pull Request
- Her PR bir Issue'yu kapatır (`Closes #12`).
- En az **1 onay** (roller tablosundaki reviewer) ve **yeşil CI** olmadan birleştirilmez.
- PR açıklamasında: ne yapıldı, nasıl test edildi, varsa ekran görüntüsü.

## Commit mesajı
`<tür>(<paket>): <kısa açıklama>` — tür: `feat`, `fix`, `docs`, `test`, `refactor`, `ci`
Örnek: `feat(scheduler): pompa kapasitesi kısıtı eklendi`

## Haftalık akış
1. Pazartesi: Milestone'daki Issue'lar paylaşılır ve atanır.
2. Hafta içi: dal → PR → review → merge.
3. Cuma: `docs/haftalik/hafta-0N.md` raporu + `v0.N-haftaN` tag'i.

```bash
git tag -a v0.1-hafta1 -m "Hafta 1 teslimi"
git push origin v0.1-hafta1
```

## Kod
- Python 3, ROS Noetic (`rospy`). ROS'tan bağımsız hesap mantığı `src/<paket>/` altında saf
  Python modülünde tutulur, böylece `pytest` ile ROS kurmadan test edilebilir.
- `irrigation_msgs` değişikliği 4 kişinin onayını gerektirir.
