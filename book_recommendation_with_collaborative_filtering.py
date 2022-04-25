# -*- coding: utf-8 -*-
"""Book Recommendation With Collaborative Filtering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WXBgJ0vSrZcXkp6fHCn2YfqNGHfI92K0

# **Sistem rekomendasi buku berdasarkan preferensi pengguna dan rating yang diberikan pengguna sebelumnya**

# **1. Mengimpor pustaka/modul python yang dibutuhkan**
"""

# Library ini merupakan salah satu perkembangan scikit-learn yang berfokus pada pembangunan dan analisa sistem rekomendasi
!pip install surprise

# Libraries for data preparation & visualization
import numpy as np
import pandas as pd
import gzip
import seaborn as sns
import re
import random
import zipfile,os
# Ignore printing warnings for general readability
import warnings 
warnings.filterwarnings("ignore")

# pip install scikit-surprise
# Importing libraries for model building & evaluation
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from surprise import Reader, Dataset, SVD
from surprise.model_selection import train_test_split, cross_validate, GridSearchCV
from surprise import accuracy

"""## **2.1 Menyiapkan kredensial akun Kaggle**"""

# Membuat folder .kaggle di dalam folder root
!rm -rf ~/.kaggle && mkdir ~/.kaggle/

# Menyalin berkas kaggle.json pada direktori aktif saat ini ke folder .kaggle
!mv kaggle.json ~/.kaggle/kaggle.json
!chmod 600 ~/.kaggle/kaggle.json

"""## **2.2 Mengunduh dan Menyiapkan Dataset**"""

# Mengunduh dataset menggunakan Kaggle CLI
!kaggle datasets download -d arashnic/book-recommendation-dataset

# Mengekstrak berkas zip ke direktori aktif saat ini
!unzip /content/book-recommendation-dataset.zip

"""# **3. Pemahaman Data (*Data Understanding*)**

## **3.2 *Exploratory Data Analysis* (EDA)**

### **3.2.1 Books**

karakteristik data buku
"""

books = pd.read_csv('Books.csv')
books

books.info()

print('Total ISBN:', len(books.ISBN.unique()))
print('Total judul:', len(books['Book-Title'].unique()))
print('Total pengarang:', len(books['Book-Author'].unique()))
print('Total penerbit:', len(books['Publisher'].unique()))

"""### **3.2.2 Rating**

karakteristik data rating
"""

ratings = pd.read_csv('Ratings.csv')
ratings

ratings.info()

ratings['Book-Rating'].describe().T

print('Total pengguna:', len(ratings['User-ID'].unique()))
print('Total buku:', len(ratings['ISBN'].unique()))
print('Total rating yang diterima:', len(ratings))

# plot
with sns.axes_style('darkgrid'):
    g = sns.catplot("Book-Rating", data=ratings, aspect=2.0, kind='count')
    g.set_ylabels("Jumlah total peringkat")

"""banyak buku yang masih memiliki rating 0, maka data tersebut dapat dihapus dengan tujuan mengurangi bias pada proses analisis

### **3.2.3 Users**

karakteristik data user
"""

users = pd.read_csv('Users.csv')
users

"""Perlu dilakukan handling missing value pada kolom age dalam proses data preparation."""

users.info()

"""# **4. Persiapan Data (*Data Preparation*)**

### **4.1 Books**

menyeleksi fitur yang diperlukan
"""

buku = books[['ISBN', 'Book-Title','Book-Author', 'Publisher']]
buku.head()

# cek missing value
buku.isnull().sum()

# mengisi data kosong pada publisher dan author
buku.loc[:,'Book-Author'] = buku['Book-Author'].fillna('Unknown')
buku.loc[:,'Publisher'] = buku['Publisher'].fillna('Unknown')
buku.isnull().sum()

"""### **4.2 Ratings**

menyeleksi fitur yang diperlukan
"""

rating = ratings
rating.isnull().sum()

print('Jumlah rating 0 :', rating['Book-Rating'].eq(0).sum())
rating.shape

# menghapus data rating 0

rating = rating[ratings['Book-Rating']>0]
rating.shape

# plot
with sns.axes_style('darkgrid'):
    g = sns.catplot("Book-Rating", data=ratings, aspect=1.5, kind='count')
    g.set_ylabels("Total number of ratings")

"""### **4.2 Users**

menyeleksi fitur yang diperlukan
"""

user = users
user.isnull().sum()

# mengisi missing value dengan moduse dari Age
user['Age'] = user['Age'].fillna(user['Age'].mode())
user.isnull().sum()

user['Age'].hist(bins=100)

# menggabungkan data buku dan rating
rating_buku = pd.merge(rating, buku, on=['ISBN'],)
rating_buku.head()

"""# **5. Modelling**

## **5.1 Popularity based recommendation**

merekomendasikan buku paling populer berdasarkan rata rata rating dan jumlah rating yang diterima

### **5.1.1 berdasarkan rata-rata rating**
"""

rata_rating_buku = rating_buku.groupby('ISBN')['Book-Rating'].mean().sort_values(ascending=False)
rata_rating_buku

"""terdapat lebih dari 20000 buku yang memiliki rating tertinggi, sehingga kita tidak bisa merekomendasikan 10 buku terbaik hanya berdasarkan rata-rata rating saja"""

rata_rating_buku.hist(bins=100)

rata_rating_buku.head(10).plot(kind='bar')

"""### **5.1.2 berdasarkan jumlah peringkat yang diterima** 

# diperlukan informasi lain untuk merekomendasikan buku terbaik, disini akan digunakan jumlah rating yang diterima tiap buku
"""

# recommend dari rating yang diterima
buku_populer = rating_buku.groupby('ISBN')['Book-Rating'].count().sort_values(ascending=False)
buku_populer

buku_populer.hist(bins=100)

buku_populer.head(10).sort_values().plot(kind='bar', title='Rating Terbanyak yang Diterima per Buku')

"""### **5.1.3 Weighted rating**


digunakan untuk menggabungkan kedua informasi yaitu berdasarkan rata-rata rating dan jumlah rating diterima, kemudian akan dipilih 10 produk


"""

rekomen_populer = pd.concat([rata_rating_buku, buku_populer],
                                   axis=1, join='inner',
                                   keys=['Average Rating', 'Rating Received'])

v = rekomen_populer['Rating Received'] # jumlah rating diterima
R = rekomen_populer['Average Rating'] # rata-rata rating per produk
C = rekomen_populer['Average Rating'].mean() # rata-rata rating seluruh produk
m = rekomen_populer['Rating Received'].quantile(0.75) # minimal jumlah rating yang diterima

rekomen_populer['Weighted Rating'] = ((R*v)+(C*m))/(v+m)
rekomen_populer = rekomen_populer.sort_values('Weighted Rating', ascending=False)
rekomen_populer.head(10)

# hasil rekomendasi

judul_populer = pd.merge(rekomen_populer, books[['ISBN', 'Book-Title']],
                         on='ISBN')
judul_populer = judul_populer[['Weighted Rating', 'Book-Title']]
judul_populer = judul_populer.drop_duplicates('Book-Title').set_index('Book-Title')
judul_populer.head(10)

"""## **5.2 Collaborative filtering (model based) recommendation**

Merekomendasikan buku lain kepada user yang memberi rating buku
"""

rating_user = rating_buku
rating_user

"""### **Label encoding**

encoder User ID dan Book Title
"""

le = LabelEncoder()
rating_user['UserID'] = le.fit_transform(rating_user['User-ID'])
rating_user['TitleID'] = le.fit_transform(rating_user['Book-Title'])
rating_user.drop('User-ID', axis=1, inplace=True)
rating_user

"""## **6. Pengembangan Model**

Mentraining data user buku dengan model SVD dari library surprise dan mengevaluasi dengan 10-fold cross validation menggunakan matriks RMSE dan MAE.

Validasi silang 10 kali lipat akan melakukan prosedur pemasangan sebanyak sepuluh kali, dengan masing-masing pemasangan dilakukan pada set pelatihan yang terdiri dari 90% dari total set pelatihan yang dipilih secara acak, dengan 10% sisanya digunakan sebagai set penahan untuk validasi.

10 fold CV adalah salah satu K fold CV yang direkomendasikan untuk pemilihan model terbaik karena cenderung memberikan estimasi akurasi yang kurang bias dibandingkan dengan CV biasa, leave-one-out CV dan bootstrap.
"""

reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(rating_user[['UserID', 'TitleID', 'Book-Rating']],
                            reader)
svd = SVD(verbose=False, n_epochs=10)
cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=10, verbose=True)

"""## **Merekomendasikan buku berdasarkan riwayat rating user**

prediksi rating buku dengan model SVD
"""

def user_recommendation(userid):
    user = rating_user[['ISBN', 'Book-Title', 'Book-Author', 'Publisher', 'TitleID']]
    user = user.reset_index()
    # getting full dataset
    data = Dataset.load_from_df(rating_user[['UserID','TitleID','Book-Rating']], reader)
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    user['Estimate_Score'] = user['TitleID'].apply(lambda x: svd.predict(userid, x).est)
    user = user.drop(['index','TitleID'], axis = 1)
    user = user.sort_values('Estimate_Score' , ascending = False)
    counts1 = user['Estimate_Score'].value_counts()
    user = user[user['Estimate_Score'].isin(counts1[counts1 == 1].index)]
    return user.head(10)

# mencari user yang menyukai buku David Copperfield sebagai contoh
rating_user[rating_user['Book-Title'].str.contains('David Copperfield')]