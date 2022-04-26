# Sistem Rekomendasi Buku Berdasarkan Preferensi Pengguna dan Rating Yang Diberikan Pengguna Sebelumnya

# Project Overview
Sistem rekomendasi mengacu pada sistem yang mampu memprediksi preferensi masa depan dari sekumpulan item untuk pengguna, dan merekomendasikan item teratas. Salah satu alasan utama mengapa kita memerlukan sistem pemberi rekomendasi dalam masyarakat modern adalah bahwa orang memiliki terlalu banyak pilihan untuk digunakan karena prevalensi Internet. Dulu, orang biasa berbelanja di toko fisik, di mana barang yang tersedia terbatas. Misalnya, jumlah film yang dapat ditempatkan di toko Blockbuster tergantung pada ukuran toko itu. Sebaliknya, saat ini, Internet memungkinkan orang untuk mengakses sumber daya yang melimpah secara online. Netflix, misalnya, memiliki banyak koleksi film. Meskipun jumlah informasi yang tersedia meningkat, masalah baru muncul karena orang mengalami kesulitan memilih item yang benar-benar ingin mereka lihat. Di sinilah sistem pemberi rekomendasi masuk. Artikel ini akan memberi Anda pengenalan singkat tentang dua cara umum untuk membangun sistem pemberi rekomendasi, Collaborative Filtering dan Singular Value Decomposition.

# Problem Statements
* Bagaimana mengolah data buku, user, dan rating untuk digunakan sebagai informasi dalam sistem rekomendasi?
* Bagaimana cara membuat sistem rekomendasi buku ?

# Tujuan
* Mengetahui cara mengolah data buku, user, dan rating untuk digunakan pada sistem rekomendasi.
* Mengetahui cara membuat sistem rekomendasi buku.

# Solution approach

Solusi yang dapat dilakukan untuk memenuhi tujuan dari proyek ini diantaranya :
* Pra-pemrosesan data 
  Dalam hal ini akan dilakukan analisis karakteristik dari ketiga data (books, users, ratings) sebelum masuk ke dalam tahap *preparation*
  * *books*
  
    ![image](https://user-images.githubusercontent.com/79253590/138228844-f7fb87b9-5b1d-4b9b-ad79-1acc98e8527a.png)
  
  * *ratings*
    
    ![image](https://user-images.githubusercontent.com/79253590/138228932-31f9dbdf-aeb0-4d80-a1ef-310dd552f253.png)
    
  * *users*
    
    ![image](https://user-images.githubusercontent.com/79253590/138229003-7cc2bfe1-f351-48b7-86d7-a132ef44db2c.png)
    
* Persiapan data

  Dalam hal ini akan dilakukan seleksi fitur-fitur yang diperlukan.
  * *books* : mengisi data kosong pada publisher dan author
  * *ratings* : menghapus data dengan rating 0
  * *users* : mengisi *missing value* menggunakan modus *Age*
  
*  Solusi yang diberikan bergantung dengan hasil rekomendasi yang ingin dicapai dan data yang dimiliki, yaitu : 

   *  *Popularity based recommendation* 
      
      Sistem rekomendasi berdasarkan Popularitas bekerja dengan tren. Ini pada dasarnya menggunakan item yang sedang tren saat ini. Misalnya, jika ada produk yang biasanya dibeli oleh setiap pengguna baru, maka ada kemungkinan produk tersebut akan menyarankan item tersebut kepada pengguna yang baru saja mendaftar [[3]](https://medium.com/the-owl/recommender-systems-f62ad843f70c). Teknik yang akan digunakan adalah *weighted rating*. Teknik ini dapat berguna untuk merekomendasikan buku kepada seluruh pengguna baik yang belum memiliki riwayat transaksi maupun yang sudah.
      
   *  *Model-Based Collaborative filtering Recommendation*
      
      Merekomendasikan buku berdasarkan riwayat transaksi (rating) pengguna untuk memprediksi dan menghitung rating yang akan diberikan pengguna pada buku lain menggunakan model machine learning SVD. Algoritma berbasis matrix factorization ini dipopulerkan oleh Simon Funk pada Netflix Prize. Kekurangan dari collaborative filtering tidak bisa merekomendasikan item yang tidak memiliki riwayat transaksi.

   *  *Singular Value Decomposition*
  
      Salah satu cara untuk menangani masalah skalabilitas dan sparsity yang dibuat oleh Collaborative Filtering (CF) adalah dengan memanfaatkan model faktor laten untuk menangkap kesamaan antara pengguna dan item. Pada dasarnya, jika ingin mengubah masalah rekomendasi menjadi masalah optimasi. Kita dapat melihatnya sebagai seberapa baik kita dalam memprediksi peringkat untuk item yang diberikan pengguna. Salah satu metrik umum adalah Root Mean Square Error (RMSE). Semakin rendah RMSE, semakin baik kinerjanya. Karena tidak mengetahui peringkat untuk item yang tidak terlihat, tentunya akan mengabaikannya untuk sementara. Yaitu, hanya meminimalkan RMSE pada entri yang diketahui dalam matriks utilitas. Untuk mencapai RMSE minimal, Singular Value Decomposition (SVD) diadopsi seperti yang ditunjukkan pada rumus di bawah ini.
      
      
      ![image]![rumus svd](https://user-images.githubusercontent.com/79253590/165235426-16bed6b9-a2fc-4a7d-8d4e-28bfe1f708c9.png)
      
      
     X menunjukkan matriks utilitas, danU adalah matriks singular kiri, yang mewakili hubungan antara pengguna dan faktor laten. S adalah matriks diagonal yang menggambarkan kekuatan setiap faktor laten, sedangkan transpos V adalah matriks singular kanan, yang menunjukkan kesamaan antara item dan faktor laten. Secara default, jumlah faktor laten adalah 100. Faktor laten ini mampu menangkap preferensi peringkat item pengguna yang diketahui & dalam prosesnya mampu memprediksi peringkat perkiraan untuk semua pasangan item pengguna di mana pengguna belum menilai item.
SVD mengurangi dimensi matriks utilitas dengan mengekstrak faktor latennya. Pada dasarnya, memetakan setiap pengguna dan setiap item ke dalam ruang laten dengan dimensi r. Oleh karena itu, ini membantu kita dalam lebih memahami hubungan antara pengguna dan item karena mereka dapat dibandingkan secara langsung.
SVD memiliki properti besar yang memiliki minimal rekonstruksi Sum of Square Error (SSE) dan oleh karena itu, ini juga biasa digunakan dalam pengurangan dimensi. Rumus di bawah ini menggantikan X dengan A, dan S dengan Σ. 


      ![image]![rumus sse](https://user-images.githubusercontent.com/79253590/165235515-eff3e815-9508-4ded-995a-08ea8d70af97.png)
      

    Ternyata RMSE dan SSE terkait secara monoton. Artinya semakin rendah SSE, semakin rendah RMSE. Dengan sifat nyaman SVD yang meminimalkan SSE, kita tahu bahwa itu juga meminimalkan RMSE. Jadi, SVD adalah alat yang hebat untuk masalah pengoptimalan ini. Untuk memprediksi item yang tidak terlihat untuk pengguna, kita cukup mengalikan U, Σ, dan T.
    
    SVD berhasil menangani masalah skalabilitas dan sparsity yang ditimbulkan oleh CF. Namun, SVD bukan tanpa flaw. Kelemahan utama dari SVD adalah tidak ada sedikit penjelasan tentang alasan untuk merekomendasikan suatu item kepada pengguna. Ini bisa menjadi masalah besar jika pengguna ingin tahu mengapa item tertentu direkomendasikan untuk mereka.

   *  *k-Fold Cross-Validation*
   
    Validasi silang adalah prosedur pengambilan sampel ulang yang digunakan untuk mengevaluasi model pembelajaran mesin pada sampel data terbatas.
Prosedur ini memiliki parameter tunggal yang disebut k yang mengacu pada jumlah grup yang akan dibagi menjadi sampel data tertentu. Dengan demikian, prosedur ini sering disebut k-fold cross-validation. Ketika nilai spesifik untuk k dipilih, nilai tersebut dapat digunakan sebagai pengganti k dalam referensi ke model, seperti k=10 menjadi validasi silang 10 kali lipat.
    
    Validasi silang terutama digunakan dalam pembelajaran mesin terapan untuk memperkirakan keterampilan model pembelajaran mesin pada data yang tidak terlihat. Yaitu, menggunakan sampel terbatas untuk memperkirakan bagaimana model diharapkan tampil secara umum ketika digunakan untuk membuat prediksi pada data yang tidak digunakan selama pelatihan model.
    
    
# Data Preparation

Dalam tahap  ini akan dilakukan proses transformasi pada data sehingga menjadi bentuk yang cocok untuk proses pemodelan. Ada beberapa tahapan yang dilakukan pada data preparation, antara lain :

* *Handling Missing Value*
  
  Proses mengolah missing value (ex: data umur yang null, data rating 0) dengan menghapus atau mengganti data tersebut dengan value lain.
  
* *Encoding* 
  
   Melakukan encoding data UserID dan Book Title agar dapat dibaca model dengan baik.
   
   
# Data Understanding

![image](https://user-images.githubusercontent.com/79253590/138232232-5c0e24cd-af12-4d65-9fd1-c9fcd7cd082f.png)

Tabel dibawah ini merupakan informasi dari dataset yang digunakan :
|           Jenis         |  Keterangan |
| ----------------------- | ----------- |
|           Sumber        | [Kaggle Dataset : Book Recommendation Dataset](https://www.kaggle.com/arashnic/book-recommendation-dataset)|
|         Usability       | 10.0 |
|          Lisensi        | CC0: Public Domain |
| Jenis dan Ukuran Berkas | zip (107MB) |

Dalam dataset tersebut berisi 3 file csv, yaitu:

* *Books* 
  
  Berisi informasi buku: 
  * *Book-Title*: judul
  * *Book-Author*: penulis
  * *Year-Of-Publication*: Tahun terbit
  * *Publisher*: Penerbit
  * *Image-URL-S*, *Image-URL-M, Image-URL-L* : link sampul buku
  
* *Ratings*
  
  Berisi informasi rating buku dari user
  * *Book-Rating*: rating buku 
  
* *Users*
  
  Berisi informasi user
  * *UserID*: identitas unik user berupa integer agar user anonymous
  * *Location*: lokasi tempat tinggal use
  * *Age*: umur user
 
 
 # Modelling

   * *Popularity based recommendation* 
      
      Digunakan untuk menggabungkan informasi rata-rata rating dan jumlah rating yang diterima per buku dengan menerapkan *weighted rating*, kemudian memilih 10 produk terbaik . Berikut rumus dari *weighted rating* :
      
      *Weighted Rating* = (Rv + Cm) / (v + m), 
      keterangan :
      * v adalah jumlah rating diterima per buku 
      * R adalah rata-rata rating per buku
      * C adalah rata-rata rating seluruh buku
      * m adalah minimal jumlah rating yang diterima. 
      
      ![image](https://user-images.githubusercontent.com/79253590/138235856-811f8ac7-2233-4ac9-a3f0-59e4e96527b2.png)
      
      Plot hasil rekomendasi dengan menerapkan *weighted rating* sebagai berikut:
      
      ![image](https://user-images.githubusercontent.com/79253590/138238337-6f7a03f5-38d0-45cb-8181-afcff0c6863f.png)
      
      
    * *Model-Based Collaborative filtering Recommendation*
      
      Akan dilakukan *training data user* buku dengan model SVD dari library Surprise yang selanjutnya 10 buku dengan prediksi rating tertinggi akan diurutkan.
      Hasil rekomendasinya sebagai berikut:
      
      ![image](https://user-images.githubusercontent.com/79253590/138238871-364eb510-d58d-4097-a957-4c58acce83f3.png)
      
  
# Evaluasi
untuk hasil evaluasi dari model SVD menggunakan metode *k-fold cross validation*. Metode ini adalah salah satu dari jenis pengujian *cross validation* yang berfungsi untuk menilai kinerja proses sebuah metode algoritme dengan membagi sampel data secara acak dan mengelompokkan data tersebut sebanyak nilai *K fold*. Dimana data training adalah K-1 fold dan sisanya digunakan sebagai data testing. Kemudian hasil testing dihitung dengan matriks:

1. *Mean Absolute Error* (MAE)
    
    Merepresentasikan rata-rata perbedaan mutlak antara nilai aktual dan prediksi pada dataset. MAE mengukur rata-rata residu dalam dataset. MAE lebih intuitif dalam memberikan rata-rata error dari keseluruhan data.
    
    ![image]![mae](https://user-images.githubusercontent.com/79253590/165236793-ed34e7a7-df3c-426c-b667-f78a2af82457.png)
    
2. *Root Mean Squared Error* (RMSE)

    Cara menghitungnya yaitu dengan mengkuadratkan error (prediksi – observasi) dibagi dengan jumlah data (= rata-rata), lalu diakarkan. 
    
    ![image]![rmse](https://user-images.githubusercontent.com/79253590/165237041-38e5aa9e-81d8-4f35-94ca-d690b4f1f8e4.png)

# Kesimpulan
 
  Dalam proses analisis kali ini, data user buku akan di training dengan model SVD dari library surprise dan mengevaluasi dengan 10-fold cross validation menggunakan matriks RMSE dan MAE. Validasi silang 10 kali lipat akan melakukan prosedur pemasangan sebanyak sepuluh kali, dengan masing-masing pemasangan dilakukan pada set pelatihan yang terdiri dari 90% dari total set pelatihan yang dipilih secara acak, dengan 10% sisanya digunakan sebagai set penahan untuk validasi. 10 fold CV adalah salah satu K fold CV yang direkomendasikan untuk pemilihan model terbaik karena cenderung memberikan estimasi akurasi yang kurang bias dibandingkan dengan CV biasa, leave-one-out CV dan bootstrap.
Hasil dari perhitungannya adalah sebagai berikut:


  ![image]![hasil](https://user-images.githubusercontent.com/79253590/165237102-07458703-4712-4ced-a3c8-a31095a5cac6.png)
  

  Dalam perhitungan ini, diperoleh nilai rata-rata *Mean Absolute Error* (MAE) sebesar 1.63 dan nilai rata-rata *Root Mean Squared Error* (RMSE) sebesar 1.26 . Sehingga dapat kita buat kesimpulan bahwa pada model ini nilai error nya cukup kecil sehingga menandakan model tersebut sudah baik. Hal ini dibuktikan juga dengan hasil rekomendasi buku yang cukup baik dan sesuai kategorinya.

# Saran
  Dalam kasus dengan pengguna baru atau item baru di mana sedikit yang diketahui tentang preferensi peringkat, metode collaborative filtering mungkin bukan metode pilihan untuk menghasilkan rekomendasi. Metode Content based filtering mungkin lebih tepat. Seringkali, pendekatan hibrida diambil untuk membangun rekomendasi waktu nyata menggunakan berbagai pendekatan berbeda di industri! Proyek ini dapat diperpanjang untuk membangun sistem rekomendasi hybrid di masa depan.
  
# Referensi
[1] https://medium.com/rahasak/collaborative-filtering-based-book-recommendation-system-with-spark-ml-and-scala-1e5980ceba5e

[2] https://medium.com/hackernoon/introduction-to-recommender-system-part-1-collaborative-filtering-singular-value-decomposition-44c9659c5e75

[3] https://medium.com/the-owl/recommender-systems-f62ad843f70c

[4] https://jonathan-hui.medium.com/machine-learning-singular-value-decomposition-svd-principal-component-analysis-pca-1d45e885e491

[5] https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html?highlight=label%20encoder#sklearn.preprocessing.LabelEncoder

[6] https://machinelearningmastery.com/k-fold-cross-validation/
 
