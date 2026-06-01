# Fuel System
Saat ini kita masih belum melakukan implementasi bahan bakar. Berikut gagasan mengenai sistem fuel mass tersebut.

Secara fisika, formulanya yaitu:
$$ M_{total} = m_{dry} + m_{fuel} $$

di mana:
- $m_{total}$ = massa total roket
- $m_{dry}$ = massa kosong roket
- $m_{fuel}$ = masa bahan bakar

# Massa bahan bakar
Berubah ketika
$$ m_{fuel}(t) $$

akan terus turun:
$$ m_{fuel,new} = m_{fuel} - \dot{m}\Delta{t} $$

# Logika ketika simulasi
## Cek apakah fuel masih ada
Jika:
$$ m_{fuel} \gt 0 $$

maka:
- masih aktif
- thrust aktif

## Kurangi fuel
$$ m_{fuel,new} = m_{fuel} - \dot{m}\Delta{t} $$

## Jika fuel habis
Jika:
$$ m_{fuel} \leq 0 $$

maka:
- thrust 0
- fuel_mass 0
