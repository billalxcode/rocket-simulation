Dengan data yang ada di `Stage`, Anda sebenarnya sudah bisa menghasilkan cukup banyak parameter turunan yang dibutuhkan simulasi roket.

## Data Dasar

```python
dry_mass
propellant_mass

thrust_vacuum
thrust_sea_level

isp_vacuum
isp_sea_level
```

---

# 1. Wet Mass (Massa Saat Penuh)

Massa total sebelum peluncuran.

$$ m_{wet}=m_{dry}+m_{propellant} $$

Contoh:

```python
dry_mass = 500
propellant_mass = 2000

wet_mass = 2500 kg
```

---

# 2. Mass Ratio

Sangat penting untuk persamaan Tsiolkovsky.

$$ MR=\frac{m_{wet}}{m_{dry}} $$

Contoh:

```python
2500 / 500

MR = 5
```

---

# 3. Structural Ratio

Mengukur berapa banyak massa yang bukan propellant.

$$
\epsilon = \frac{m_{dry}}{m_{wet}}
$$

Contoh:

```python
500 / 2500

0.2
```

Artinya:

```text
20% struktur
80% propellant
```

---

# 4. Propellant Fraction

Kebalikan dari structural ratio.

$$
PF = \frac{m_{propellant}}{m_{wet}}
$$

Contoh:

```python
2000 / 2500

0.8
```

---

# 5. Delta-V Ideal

Formula paling penting.

$$ \Delta v=I_{sp}g_0\ln\left(\frac{m_{wet}}{m_{dry}}\right) $$

Biasanya pakai:

```python
isp_vacuum
```

karena setelah beberapa kilometer performa mesin mendekati vakum.

Contoh:

```python
Isp = 320
MR  = 5
```
$$
\Delta v = 320 \times 9.80665 \times \ln(5)
$$

≈

```text
5049 m/s
```

---

# 6. Mass Flow Rate

Ini yang akan dipakai setiap timestep.

Hubungan thrust dan Isp:

$$ \dot m=\frac{T}{I_{sp}g_0} $$

Contoh:

```python
T = 230000 N
Isp = 300 s
```

$$
\dot m = \frac{230000}
{300 \times 9.80665}
$$

≈

```text
78.2 kg/s
```

Artinya mesin membakar:

```text
78.2 kg propellant per detik
```

---

# 7. Burn Time

Jika mass flow konstan.

$$ t_{burn}=\frac{m_{propellant}}{\dot m} $$

Contoh:

```python
propellant = 2000 kg
mdot = 78.2 kg/s
```

```text
25.6 detik
```

---

# 8. Instantaneous Mass

Selama pembakaran.

$$ m(t)=m_{wet}-\dot m t $$

Selama:

```text
0 <= t <= burn_time
```

---

# 9. Instantaneous Acceleration

Tanpa drag dan gravitasi.

$$ a=\frac{T}{m} $$

Karena massa terus turun:

```text
massa turun
↓
a naik
```

Inilah alasan roket semakin cepat menjelang burnout.

---

# 10. Thrust-to-Weight Ratio (TWR)

Parameter paling sering dicek saat liftoff.

$$ TWR=\frac{T}{mg} $$

Biasanya:

```python
T = thrust_sea_level
m = wet_mass
g = 9.80665
```

Contoh:

```python
T = 230000
m = 2500
```

```text
TWR = 9.38
```

---

# 11. Net Liftoff Acceleration

Saat masih di launch pad.

$$ a=\frac{T-mg}{m} $$

Contoh:

```python
T = 230000
m = 2500
```

```text
a = 82.2 m/s²
```

---

# 12. Interpolasi Thrust Berdasarkan Tekanan

Karena Anda punya:

```python
thrust_vacuum
thrust_sea_level
```

Anda bisa menghitung thrust pada altitude berapa pun.

Interpolasi sederhana:

$$
T(h)
=

T_{sl}
+
\left(
T_{vac}
-

T_{sl}
\right)
\left(
1-\frac{P(h)}{P_0}
\right)
$$

dimana:

```python
P(h) = pressure atmosphere
P0   = 101325 Pa
```

---

# 13. Interpolasi Isp Berdasarkan Tekanan

Sama seperti thrust.

$$
Isp(h)
=

Isp_{sl}
+
(Isp_{vac}-Isp_{sl})
\left(
1-\frac{P(h)}{P_0}
\right)
$$

Ini cukup akurat untuk simulasi level RocketPy.

---

# 14. Propellant Remaining

Yang nanti dipakai event burnout.

$$
m_{prop}(t)
=
m_{prop,0}

\dot m t
$$

Jika:

```text
m_prop <= 0
```

maka:

```text
BURNOUT EVENT
```

---

# Menurut saya, untuk arsitektur yang Anda bangun, properti turunan yang layak langsung ditambahkan ke `Stage` adalah:

```python
@property
def wet_mass(self):
    ...

@property
def mass_ratio(self):
    ...

@property
def propellant_fraction(self):
    ...

@property
def burn_time(self):
    ...

@property
def mass_flow_rate(self):
    ...
```

Sedangkan yang **tidak perlu disimpan** dan sebaiknya dihitung oleh modul lain:

* Delta-V → `analysis/performance.py`
* TWR → `analysis/performance.py`
* Acceleration → `simulation/force_aggregator.py`
* Thrust(h) → `models/propulsion/nozzle.py`
* Isp(h) → `models/propulsion/nozzle.py`

Dengan begitu `vehicle/stage.py` tetap menjadi representasi data roket, bukan tempat menghitung seluruh fisika penerbangan.
