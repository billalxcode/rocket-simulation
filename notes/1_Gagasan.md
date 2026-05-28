# Gagasan Utama Simulasi
Prinsi dasarnya sangat sederhana:
$$ \sum{F} = ma $$

Artinya, roket akan mengalami percepatan sesuai gaya total yang bekerja padanya. Jika gaya dorong lebih besar daripada berat dan hambatan udara, roket naik. Jika tidak, roket turun.

# Variabel Keadaan Roket
Dalam simulasi dasar, biasanya kita simpan 3 hal utama:
$$ h(t), v(t), m(t) $$

Di mana:
- $h(t)$ = ketinggian roket terhadap tanah
- $v(t)$ = kecepatan roket
- $m(t)$ = massa roket pada waktu $t$

Waktu ditulis sebagai $t$

# Persamaan Gerak Dasar
## Hubungan posisi dan kecepatan
Kecepatan adalah turunan dari posisi:

$$ \frac{dh}{dt} = v $$

Artinya, perubahan ketinggian per detik sama dengan kecepatan

## Hubungan kecepatan dan percepatan
Percepatan adalah turunan dari kecepatan

$$ \frac{dv}{dt} = a $$

Artinya, perubahan kecepatan per detik sama dengan percepatan.

## Hubungan massa dan laju konsumsi bahan bakar
Jika roket sedang menyala, massanya berkurang:
$$ \frac{dm}{dt} = -\dot{m} $$

Tanda minus artinya massa berkurang

# Gaya-gaya bekerja pada roket
Dalam simulasi dasar, biasanya ada 3 gaya utama:

## Gaya Dorong Mesin
Ditulis sebagai:
$$ T $$

Ini adalah gaya dari mesin roket yang mendorong roket ke atas.

## Gaya Hambatan Udara
Ditulis sebagai:
$$ D = \frac{1}{2}pv^2C_dA $$

Ini gaya yang melawan gerak roket.
Jika roket naik, drag arahnya ke bawah.
Jika roket turun, drag arahnya ke atas.

# Persamaan Percepatan Roket
Jika kita ambil arah ke atas sebagai positif, maka:

$$ \dot{m}\frac{dv}{dt} = T - mg - D $$

Jadi:
$$ \frac{dv}{dt} = \frac{T - mg - D}{m} $$

Ini adalah inti simulasi roket dasar.
Jika roket tidak memasukan hambatan udara, maka persamaannya menjadi lebih sederhana:

$$ \frac{dv}{dt} = \frac{T - mg}{m} $$

# Persamaan Gaya Dorong Mesin
Salah satu bentuk umum `thrust` adalah:
$$ T = \dot{m}v_e + (P_e - P_a)A_c $$

Tetapi sering untuk simulasi dasar, sering pakai bentuk sederhana:
$$ T = konstan $$

Atau
$$
T =
\begin{cases}
T_0, & \text{jika mesin aktif} \\
0, & \text{jika mesin mati}
\end{cases}
$$

Jika simulasi sederhana, maka `thrust` nya konstan selama durasi pembakaran.

# Persamaan Massa Roket
Massa roket berubah karena bahan bakar habis.
Jika laju konsumsi bahan bakar konstan:

$$ m(t) = m_0 - \dot{m}t $$

selama mesin menyala.
Lebih umum, bisa ditulis sebagai:

$$
m(t) = 
\begin{cases}
m_0 - \dot{m}t, 0 \leq{t} \leq{t_b} \\
m_f, t \gt{t_b}
\end{cases}
$$

Dengan:
- $m_0$ = massa awal roket
- $m_f$ = massa setelah bahan bakar habis
- $t_b$ = waktu bakar mesin

# Model Paling Sederhana: tanpa drag
Jika ingin membuat model yang mudah dipahami, cukup dengan:

$$ \frac{dh}{dt} = v $$
$$ \frac{dv}{dt} = \frac{T - mg}{m} $$
$$ \frac{dm}{dt} = -\dot{m} $$

untuk saat mesin aktif.
Lalu saat mesin mati:
$$ T = 0 $$

sehingga:
$$ \frac{dv}{dt} = -g $$

Jika tanpa drag, roket setelah mesin mati hanya dipengaruhi gravitasi.

# Model lebih realistis, dengan drag udara
Jika roket bergerak ke atas, drag arahnya ke bawah.
Jika arah atas dianggap positif, maka:

$$ \frac{dv}{dt} = \frac{T - mg - D}{m} $$

dengan:
$$ D = \frac{1}{2}pv^2C_dA $$

Kadang perlu hati-hati dengan arah drag, karean drag selalu melawan arah gerak.
Cara yang lebih rapi adalah:
$$ D = \frac{1}{2}pC_dAv|v| $$

Bentuk $v|v|$ membuat tanda drag otomatis benar:
- Jika $v \gt 0$ (naik), drag negatif.
- Jika $v \lt 0$ (turun), drag positif

# Jika Menggunakan Rumus Roket Klasik
Terdapat persamaan terkenal bernama `Tsiolkovsky Roket Equation`

$$ \Delta{v} = v_eln(\frac{m_0}{m_f}) $$

Ini memberi tahu seberapa besar perubahan kecepatan total yang bisa dicapai roket dari propelan tertentu.
Namun untuk simulasi waktu ke waktu, persamaan ini bukan satu-satunya yang dipakai. Biasanya simulasi numerik tetap memakai:

$$ m\frac{dv}{dt} = T - mg - D $$

Rumus $\Delta{v}$ lebih cocok untuk estimasi kemampuan roket secara global.
