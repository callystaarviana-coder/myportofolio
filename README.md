Nama : Callysta Arviana 

NPM : 2506619045

Kelas : PBP A

### TUGAS INDIVIDU 1 
1. Dalam tugas 1 ini, saya tidak menggunakan elemen sematik seperti <section>, <article>, atau <aside> karena sejujurnya saya belum terlalu mengerti cara penggunaan yang benar sehingga rawan untuk melakukan kesalahan. Saya menggunakan <div> yang diberi class/ID. Saya tidak menggunakan beberapa elemen tersebut karena struktur web portofolio pada Tugas 1 menurut saya masih tergolong sederhana dan berfokus pada penataan visual saja. Penggunaan <div> sudah dapat untuk memenuhi kebutuhan tata letak halaman tanpa memengaruhi hasil render di browser.

2. awalnya saya bingung bagaimana cara cek tingkat respons pada kode yang saya buat, tetapi setelah bertanya pada kakak tingkat yang mengerti saya menjadi mengerti caranya. Awalnya, Elemen yang disusun ke samping di desktop seperti navigasi dan kartu proyek terlihat berantakan dan sesak saat dibuka di layar HP. Selain itu, ukuran teks dan padding yang pas di laptop terasa terlalu memakan tempat di ponsel. tetapi akhirnya dapat diselesaikan dengan beberapa cara yaitu, Mengubah susunan layout dari horizontal menjadi vertikal (menumpuk ke bawah) di layar HP menggunakan @media (max-width: 768px). Setelah itu menempatkan informasi paling penting (foto profil dan bio singkat) di posisi teratas, lalu diikuti oleh konten pendukung di bawahnya. Tahap terakhir, mengganti ukuran piksel statis (px) dengan unit relatif (% atau rem) agar elemen dan teks menyesuaikan lebar layar secara dinamis.

3. Karena website ini masih static web murni, konten seperti teks proyek dan bio harus ditulis manual secara lansung yang bisa dibilang hardcoded di dalam file HTML yang telah dibuat. Jika saya ingin menambah, mengubah, atau menghapus informasi proyek, saya harus membuka dan memodifikasi kode HTML-nya satu per satu. Selain itu, websitenya hanya bisa memberikan informasi ke pengunjung (membaca saja) tidak bisa berinteraksi aktif seperti mengirim pesan, memberikan komentar, atau mengisi formulir kontak.

Setelah belajar banyak hal dari tugas 1 ini, ada beberapa fungsionalitas Dinamis yang Ingin saya tambahkan, yaitu:

- Sistem Database (CRUD) untuk Proyek: Agar saya bisa menambah atau memperbarui daftar portofolio secara otomatis melalui basis data tanpa perlu menyentuh file HTML lagi.

- Formulir Kontak Interaktif: Agar pengunjung atau perekrut bisa langsung mengirimkan pesan yang tersimpan ke dalam database atau terkirim langsung ke email saya.

AI disclosure : AI memiliki peran yang cukup membantu saya untuk mengerti tugas yang diberikan karena ini merupakan pengalaman saya untuk menggunakan HTML, AI saya gunakan sebagai "guru les" yang menjawab pertantaan" fundamental disaat mengerjakan tugas seperti "tolong jelaskan pada saya keterkaitan index.html pada file lainnya" dan ketika program saya sempat error saya menggunakan AI dalam menjelaskan akar masalah yang ada sehingga saya mengerti masalah yang ada dan mencari solusi untuk program dapat di run  dengan harapan bahwa saya sudah mengerti fundamental dan dapat menyelesaikan masalah secara mandiri kedepannya. 

- diluar dari AI, justru saya lebih sering untuk meminta bantuan dari angkatan 24 yang pernah mengambil mata kuliah ini untuk menjelaskan saya materi yang digunakan dalam tugas 1 ini karena sering kali AI pun tidak dapat menyediakan penjelasan yang membuat saya untuk mengerti materi yang ada. 

### TUGAS INDIVIDU 2

1. Saat awal mencoba alur ini, saya sempat merasa prosesnya terlalu panjang hanya untuk memuat satu halaman, tetapi saya baru menyadari pentingnya konsep pemisahan tugas di Django. Alurnya berjalan ketika pengguna mengakses alamat /skills/ di browser. Permintaan ini pertama kali disaring oleh urls.py proyek sebagai gerbang utama untuk diteruskan ke urls.py aplikasi main menggunakan fungsi include. Selanjutnya, urls.py aplikasi memetakan path tersebut ke fungsi view show_skills. Di sinilah view bertindak sebagai penghubung logika; ia meminta data ke model Skill menggunakan Skill.objects.all(), lalu model mengambil data fisik dari basis data SQLite. Setelah data diterima kembali oleh view, data tersebut dikemas ke dalam variabel context dan diteruskan ke template skills.html lewat fungsi render. Template kemudian menyusun data dinamis tersebut menggunakan perulangan HTML, hingga akhirnya Django mengirimkan dokumen web yang utuh kembali ke browser pengguna. Alur ini membuat saya paham bahwa setiap file memiliki tanggung jawab yang terisolasi sehingga kode tidak menumpuk di satu tempat.

2. Menyambung refleksi saya di Tugas 1 mengenai repotnya menulis data secara hardcoded di HTML, tugas 2 ini memberikan solusi nyata melalui pemisahan data dan tampilan. Dampaknya terhadap pemeliharaan aplikasi sangat terasa karena jika saya ingin menambah daftar skill baru atau memperbarui tingkat kemahiran, saya cukup mengelolanya melalui basis data tanpa perlu menyentuh file HTML lagi. Hal ini meminimalkan risiko merusak susunan tata letak CSS yang sudah saya rapikan sebelumnya hanya karena salah mengedit tag. Sementara dari sisi pengembangan aplikasi, data yang tersimpan di model bersifat dinamis dan terstruktur, sehingga aplikasi menjadi jauh lebih siap jika ke depannya saya ingin menambahkan fungsionalitas baru seperti formulir input data interaktif atau fitur pencarian.

3. Awalnya saya sempat bingung mengapa harus ada dua perintah terminal yang berbeda untuk urusan migrasi basis data. Refleksi yang saya dapatkan adalah keduanya bekerja dalam dua tahap yang berbeda: makemigrations bertugas mencatat rancangan perubahan pada models.py ke dalam berkas instruksi migrasi (seperti 0002_skill.py) tanpa menyentuh tabel fisik, sedangkan migrate adalah eksekutor yang benar-benar menerapkan berkas instruksi tersebut ke dalam basis data SQLite.

Contoh nyata yang saya alami adalah saat membuat model baru Skill pada tugas ini. Karena tabel Skill belum ada di database, saya wajib menjalankan makemigrations terlebih dahulu untuk menyiapkan cetak birunya, baru menjalankan migrate agar tabelnya benar-benar tercipta. Contoh lain adalah jika nantinya saya ingin menambahkan field baru seperti link sertifikat atau menghapus field yang sudah ada di model Skill; kedua perintah tersebut tetap harus dijalankan berurutan agar skema tabel pada database selalu sinkron dengan kode model yang saya buat.

AI disclosure : Saya menggunakan chatgpt dan gemini untuk menjelaskan maksud soal dan membantu memecahkan masalah. Ketika saya sedang sendiri dan tidak dibantu oleh siapa siapa AI yang membantu saya untuk mengerti dan mengajarkan saya "basic-basic" dari permintaan soal karena walaupun sudah berusaha belajar jujur saja saya masih sangat bingung terkadang sehingga perlu di bantu dan di jelaskan ulang oleh AI tentang permintaan soal karena beberapa kali terjadi error yang tidak saya mengerti juga. 


### TUGAS INDIVIDU 3

1. Awalnya saya mengira form harus dibuat dengan menulis setiap input HTML secara manual. Setelah menggunakan ModelForm untuk Education, saya memahami bahwa Django bisa membuat field form berdasarkan model yang sudah ada, sekaligus membantu validasi dan penyimpanan data. Hal ini mengurangi pengulangan kode. Form yang sama juga bisa digunakan untuk mengedit data dengan memberikan instance dari data yang ingin diubah. Namun, aturan khusus seperti tahun selesai tidak boleh sebelum tahun masuk tetap perlu saya tambahkan sendiri.

Selain itu, {% csrf_token %} diperlukan pada form POST untuk membantu mencegah serangan CSRF, yaitu ketika situs lain mencoba membuat browser pengguna mengirim permintaan perubahan data tanpa persetujuannya. Django memeriksa token saat form dikirim dan menolak permintaan jika token tidak valid. Jadi, token ini melindungi proses pengiriman form, tetapi bukan pengganti login atau pemeriksaan hak akses.

2. Setelah membandingkan JSON dan XML, saya memahami bahwa JSON biasanya lebih ringkas karena menggunakan pasangan key dan value, sedangkan XML memakai tag pembuka dan penutup. JSON juga mendukung tipe data seperti teks, angka, dan boolean, sehingga cocok untuk data Education saya. Selain itu, JSON mudah diolah oleh JavaScript di frontend dan didukung banyak bahasa, termasuk Python. Hal ini membuat JSON praktis untuk aplikasi web modern, meskipun XML tetap berguna untuk kebutuhan sistem tertentu.

3. Ketika pengguna membuka /api/education/, Django mencocokkan URL tersebut lalu menjalankan get_education_json. Fungsi ini mengambil data Education dari database, kemudian serializers.serialize() mengubahnya menjadi JSON. Hasilnya dikirim melalui HttpResponse dengan content_type="application/json".

Serialization diperlukan karena hasil pengambilan data masih berupa QuerySet berisi object Django, sehingga perlu diubah menjadi format yang bisa dipahami aplikasi lain. Untuk menampilkan halaman Education, show_education memanggil fungsi JSON tersebut secara langsung, melakukan deserialisasi, lalu mengirim object hasilnya ke template melalui context. Dari proses ini saya memahami bagaimana data database diubah menjadi JSON dan diolah kembali untuk ditampilkan.

AI disclosure: Saya menggunakan ChatGPT dan Gemini untuk membantu memahami instruksi tugas dan konsep dasar yang masih membingungkan. Walaupun sudah mencoba belajar sendiri, terkadang saya membutuhkan penjelasan bertahap dan contoh kode agar lebih mengerti hubungan antara model, form, view, dan template.


### TUGAS INDIVIDU 4 

Saya menggunakan ChatGPT untuk membantu memahami materi autentikasi, otorisasi, session, cookie, dan relasi ManyToMany yang awalnya masih membingungkan bagi saya. Saya meminta penjelasan secara bertahap, terutama mengenai perbedaan pengguna biasa, Editor, dan superuser serta alasan pembatasan akses perlu diterapkan pada view dan template. Selain penjelasan konsep, AI memberikan contoh kode yang disesuaikan dengan fitur Education pada proyek saya sebagai bahan belajar yang dapat membuat saya semakin paham. Acuan utama pengerjaan saya adalah Tutorial 04 dan instruksi Tugas Individu 4 PBP. Dari proses ini, saya belajar bahwa keberhasilan menampilkan atau menyembunyikan tombol belum cukup untuk memastikan keamanan; hak akses tetap harus diperiksa di sisi server. Saya juga perlu memeriksa kembali saran AI karena kesesuaian kode bergantung pada struktur proyek dan konfigurasi yang digunakan.


### TUGAS INDIVIDU 5 

1. Debouncing adalah cara untuk menunda pemanggilan fungsi sampai pengguna berhenti melakukan suatu aktivitas selama waktu tertentu. Dalam fitur pencarian Education saya, pencarian dijalankan setelah pengguna berhenti mengetik selama 300 milidetik. Jika pengguna mengetik lagi sebelum waktu tersebut selesai, timer sebelumnya dibatalkan menggunakan clearTimeout,  lal waktu tunggunya dimulai kembali.

Menurut saya, hal yang perlu diperhatikan adalah pencarian yang terasa langsung tidak berarti harus mengirim permintaan setiap kali satu huruf diketik. Misalnya, ketika mencari “Gonzaga”, tanpa debouncing browser bisa mengirim permintaan untuk setiap perubahan input, padahal pengguna belum selesai mengetik. Dengan debouncing, permintaan yang tidak diperlukan bisa dikurangi sehingga server tidak perlu berulang kali  memproses pencarian tersebut. Hasil pencarian tetap diperbarui tanpa reload halaman. Pada kode saya, tombol Cari dan Enter juga tetap bisa digunakan untuk langsung mencari tanpa menunggu timer.

2. await digunakan untuk menunggu hasil dari proses asynchronous sebelum melanjutkan baris berikutnya di dalam fungsi async. Pada halaman Education saya, fetch() mengirim permintaan  ke endpoint JSON dan mengembalikan Promise, yaitu object yang mewakili proses yang hasilnya belum tentu tersedia saat itu. Dengan await fetch(), variabel response baru digunakan setelah respona dari server diterima. Proses menunggu ini tidak membuat seluruh halaman berhenti bekerja.

Setelah itu, saya juga menggunakan await response.json() karena membaca isi respons menjadi data JavaScript merupakan proses asynchronous. Jadi, menerima respons dan membaca datanya adalah dua tahap yang berbeda. Jika await pada fetch() dihilangkan tetapi kode berikutnya tetap sama, variabel response masih berisi Promise, bukan object Response. Akibatnya, pem eriksaan response.ok tidak bekerja sesuai harapan dan response.json() tidak bisa langsung dipanggil pada Promise tersebut. Namun, fetch() sebenarnya tetap dapat digunakan tanpa await jika hasilnyH ditangani menggunakan .then(). Dari sini saya memahami bahwa yang diperlukan adalah menangani hasil proses asynchronous dengan benar, bukan sekadar menambahkan await pada setiap fungsi.

3. XSS atau Cross-Site Scripting adalah serangan ketika kode berbahaya dapat disisipkan ke halaman web dan dijalankan oleh browser pengguna. Contohnya, input yang seharusnya berisi deskripsi pendidikan  justru diisi dengan tag HTML yang memiliki onerror untuk menjalankan JavaScript. Jika input tersebut langsung dimasukkan ke innerHTML tanpa escaping, browser dapat membacanya sebagai bagian dari HTML dan menjalankan kode yang disisipkan.

Pada template Django, nilai variabel secara default sudah melalui autoescaping sehingga karakter seperti < dan > ditampilkan sebagai teks. Namun, ketika data diambil melalui AJAX lalu disusun menjadi HTML menggunakan JavaScript, perlindungan dari template Django  tersebut tidak otomatis diterapkan pada data yang baru dimasukkan. Jadi, AJAX sendiri bukan penyebab XSS, tetapi cara menampilkan datanya perlu lebih diperhatikan.

Pada bagiaJ Education saya, nilai teks dari JSON diproses menggunakan escapeHtml sebelum dimasukkan ke HTML. Untuk pesan error dan toast, saya menggunakan textContent agar isinya diperlakukan sebagai teks. Selain itu, input  institution, degree, dan description dibersihkan menggunakan strip_tags pada method clean_<field> di EducationForm. Saya memahami bahwa pembersihan di server ini tetap perlu disertai escaping saat  menampilkan data, karena strip_tags saja bukan jaminan bahwa su atu nilai aman untuk langsung dimasukkan ke HTML.

AI disclosure : saya menggunakan chatgpt untuk dapat benar benar menjelaskan materi karena menurut saya materi minggu ini merupakan yang paling sulit sejauh ini dan sejujurnya saja kesulitan memahami sehingga harus di jelaskan dari awal banget dengan chatgpt dan saya membuat latihan di folder lain untuk berlatih materi ini sebelum dituangkan ke dalam folder ini 
