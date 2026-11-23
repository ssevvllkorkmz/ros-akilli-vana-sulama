# Tarımsal Su Yönetimi İçin ROS Tabanlı Akıllı Vana Kontrol Sistemi

Bu depo, BIL417 Robot Programlama dersi kapsamında geliştirilen dağıtık ve kestirimsel akıllı vana kontrol sisteminin ROS Noetic paketini (`akilli_vana`) içerir.

## 1. İlk Kurulum (Sadece İlk Seferde Yapılır)
Projeyi kendi Ubuntu bilgisayarınızdaki `catkin_ws` çalışma alanına indirmek için terminali açın ve şu komutları sırayla çalıştırın:

```bash
cd ~/catkin_ws/src
git clone [https://github.com/ssevvllkorkmz/ros-akilli-vana-sulama.git](https://github.com/ssevvllkorkmz/ros-akilli-vana-sulama.git) akilli_vana
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

## 2. Çalışmaya Başlamadan Önce (Güncel Kodları Çekme)
Diğer ekip arkadaşlarının yaptığı son değişiklikleri bilgisayarınıza almak için kod yazmaya başlamadan önce mutlaka şu komutu çalıştırın:

```bash
cd ~/catkin_ws/src/akilli_vana
git pull origin main
```

## 3. Yaptığınız Değişiklikleri GitHub'a Yükleme (Commit & Push)
Kendi modülünüzde kod ekledikten veya düzenledikten sonra değişiklikleri depoya göndermek için şu adımları izleyin:

1. Paket klasörüne girin ve değişen dosyaları kontrol edin:
   ```bash
   cd ~/catkin_ws/src/akilli_vana
   git status
   ```
2. Değişiklikleri hazırlayın ve açıklayıcı bir mesajla kaydedin (`commit`):
   ```bash
   git add .
   git commit -m "Modül adı: Yapılan değişikliğin kısa açıklaması"
   ```
   *(Örnek: `git commit -m "Karar Motoru: Open-Meteo API yagis kontrolu eklendi"`)*
3. Kaydettiğiniz değişiklikleri GitHub'a gönderin (`push`):
   ```bash
   git push origin main
   ```

> **Önemli Not:** İlk kez `git push` yaparken terminal şifre sorduğunda normal GitHub hesap şifreniz çalışmaz. GitHub hesabınızdan **Settings > Developer settings > Personal access tokens > Tokens (classic)** yolundan `repo` yetkili bir token üretip şifre kısmına o kodu yapıştırmalısınız.
