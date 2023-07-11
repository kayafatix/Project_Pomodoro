# Pomodoro-Project-

### CLASS LOGIN AND SING_UP ###
Bu kodlar, PyQt5 kütüphanesi kullanılarak bir kullanıcı giriş ekranı oluşturmayı amaçlayan bir sınıf tanımlar. İşlevleri aşağıdaki gibi açıklanabilir:

### __init__(self) metodu: 

Sınıfın başlatıcı metodudur. Öncelikle, QDialog sınıfının başlatıcı metodu çağrılır ve üst sınıfın özelliklerini alır. Ardından, loadUi fonksiyonu kullanılarak "UI//login.ui" dosyasındaki kullanıcı arayüzü yüklenir. Daha sonra, "signUpButton" ve "loginButton" adlı düğmelerin tıklanma olaylarına ilgili işlevler bağlanır. Hata mesajı metin kutuları (errorTextLogin ve errorTextSignUp) boş olarak ayarlanır. Son olarak, self.db adında bir veritabanı bağlantısı nesnesi oluşturulur ve None olarak ayarlanır.

### go_main_menu(self) metodu: 

Ana menüye geçmek için kullanılır. MainMenuUI sınıfından bir örnek oluşturulur ve bu örnek widget'e eklenir. Ardından, mevcut widget'in indeksi bir artırılarak ana menüye geçiş sağlanır.

### sign_up_button(self) metodu: 

Kayıt olma düğmesine tıklandığında çağrılır. Kullanıcının girdiği isim ve e-posta bilgileri alınır. Eğer isim veya e-posta alanı boş ise hata mesajı metin kutusuna ilgili uyarı yazısı yazılır. Aksi takdirde, e-posta alanında "@" sembolü varsa, sqlite3 modülü kullanılarak "pomodoro.db" adlı veritabanıyla bağlantı kurulur. Kayıtlı kullanıcıların e-posta adreslerini kontrol etmek için bir sorgu çalıştırılır ve sonuçlar bir diziye eklenir. Eğer kullanıcının girdiği e-posta adresi bu dizide varsa, hata mesajı metin kutusuna "The user 'e-posta adresi' is already exist." şeklinde bir uyarı yazılır. Aksi takdirde, yeni kullanıcı veritabanına eklenir, veritabanı işlemleri onaylanır ve hata mesajı metin kutusuna "The user 'e-posta adresi' has been successfully registered." şeklinde bir bilgilendirme yazılır. Son olarak, giriş alanları temizlenir.

#### login_button(self) metodu:

 Giriş düğmesine tıklandığında çağrılır. "pomodoro.db" veritabanıyla bağlantı kurulur. Kullanıcının girdiği e-posta adresi (self.login) alınır. Tüm kullanıcıları içeren bir sorgu çalıştırılır ve sonuçlar üzerinde döngüye girilir. Eğer giriş alanı boş ise veya içinde "@" sembolü yoksa, hata mesajı metin kutusuna "For login please enter a valid email address!" şeklinde bir uyarı yazılır. Eğer giriş alanı, veritabanındaki kullanıcılardan biriyle eşleşiyorsa, go_main_menu() metoduna gidilir ve döngü kırılır. Aksi takdirde, hata mesajı metin kutusuna "Sorry, your email address is not registered!" şeklinde bir uyarı yazılır.

Kodların geri kalan kısmı açıklanmadığı için, tam olarak neler yapıldığına dair bir yorum yapılamaz.




