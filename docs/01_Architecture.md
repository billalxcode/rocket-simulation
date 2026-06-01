Sempurna! Data lengkap. Berikut arsitektur lengkapnya untuk Python stack:

---

## Arsitektur Rekomendasi: Python Rocket Simulation (Riset & Analisis Teknik)

### Filosofi Desain
> **Scientific Python Stack** — ikuti konvensi ekosistem sains Python. Setiap modul adalah pure Python package yang bisa di-import secara independen, dengan NumPy/SciPy sebagai tulang punggung numerik.

---

## Struktur Modul (Top-Level)

```
rocket-sim/
├── rocketsim/              → Main package
│   ├── core/               → Tipe data, konstanta, koordinat
│   ├── models/             → Model fisika (aero, propulsi, gravitasi)
│   ├── vehicle/            → Definisi roket & stage
│   ├── environment/        → Atmosfer, planet, ephemeris
│   ├── simulation/         → Integrator, orchestrator, event system
│   ├── io/                 → Parser YAML/JSON, exporter hasil
│   ├── analysis/           → Post-processing, plotting, laporan
│   └── viz/                → GUI desktop & web dashboard
│
├── notebooks/              → Jupyter notebooks contoh & validasi
├── data/                   → Database engine, atmosfer, ephemeris
├── tests/                  → Unit, integrasi, validasi vs referensi
├── docs/                   → Dokumentasi (Sphinx)
└── pyproject.toml          → Build & dependency management
```

---

## Detail Setiap Modul

---

### 1. `core/` — Fondasi & Primitif
**Tanggung jawab:** Semua tipe data fundamental, konstanta fisika, dan transformasi koordinat. **Nol dependency ke modul lain dalam package.**

```
core/
├── __init__.py
├── constants.py          → G, R_earth, g0, atm_sl, mu_earth/moon/sun
├── types.py              → dataclass StateVector, ForceVector, SimResult
├── coordinates.py        → ECI ↔ ECEF ↔ NED ↔ Body frame (pakai numpy)
├── quaternion.py         → Operasi quaternion untuk attitude
└── interfaces.py         → Abstract base class: IForceModel, IIntegrator,
                            IAtmosphere, IEnvironment
```

**`StateVector`** adalah dataclass yang dibawa seluruh pipeline:
```python
@dataclass
class StateVector:
    time: float           # s
    position: np.ndarray  # [x, y, z] ECI, meter
    velocity: np.ndarray  # [vx, vy, vz] ECI, m/s
    mass: float           # kg (berkurang seiring bahan bakar habis)
    attitude: np.ndarray  # quaternion [w, x, y, z]
    stage_index: int      # stage aktif saat ini
```

---

### 2. `models/` — Model Fisika
**Tanggung jawab:** Implementasi konkret tiap gaya fisika. Semua subclass dari `IForceModel` di `core/interfaces.py`.

```
models/
├── __init__.py
│
├── aerodynamics/
│   ├── __init__.py
│   ├── drag.py               → F_drag = 0.5 * rho * v² * Cd * A
│   ├── lift.py               → Lift dari fins, angle of attack
│   ├── mach.py               → Deteksi regime: subsonic/transonic/supersonic
│   └── coeff_table.py        → Interpolasi Cd vs Mach (scipy.interpolate)
│
├── propulsion/
│   ├── __init__.py
│   ├── thrust_curve.py       → Thrust(t) dari data engine, interpolasi
│   ├── mass_flow.py          → dm/dt = -thrust / (Isp * g0)
│   ├── nozzle.py             → Koreksi thrust vs tekanan ambient
│   └── engine_registry.py    → Load database engine dari YAML
│
└── gravity/
    ├── __init__.py
    ├── point_mass.py         → F = -GM * m / r³ * r_vec  (sederhana)
    ├── j2_perturbation.py    → Oblateness Bumi (penting untuk orbital)
    └── nbody.py              → Multi-body: Bumi + Bulan + Matahari
                                (pakai posisi dari ephemeris)
```

**Catatan:** `coeff_table.py` pakai `scipy.interpolate.interp1d` atau `CubicSpline` — jangan linear interpolation di sekitar Mach 1 karena diskontinuitas Cd sangat tajam.

---

### 3. `vehicle/` — Definisi Roket
**Tanggung jawab:** Representasi struktur roket dan logika multi-stage. Di-load dari YAML.

```
vehicle/
├── __init__.py
├── stage.py              → dataclass Stage: dry_mass, prop_mass,
│                           engine_id, fin_geometry
├── rocket.py             → class RocketVehicle: list of Stage,
│                           urutan separasi, payload
├── mass_properties.py    → Hitung CG & inertia tensor saat propellant
│                           berkurang (update tiap timestep)
├── separation_event.py   → Trigger separasi: burnout / altitude / time
└── builder.py            → Fluent API builder:
                            Rocket().add_stage(...).set_payload(...)
```

**Contoh builder API:**
```python
rocket = (RocketBuilder()
    .add_stage(name="booster", dry_mass=500, prop_mass=2000, engine="AeroTech_L1420")
    .add_stage(name="upper",   dry_mass=100, prop_mass=400,  engine="AeroTech_J570")
    .set_payload(mass=10)
    .build())
```

---

### 4. `environment/` — Kondisi Eksternal
**Tanggung jawab:** Semua kondisi luar yang mempengaruhi roket: atmosfer, planet, angin, ephemeris.

```
environment/
├── __init__.py
│
├── atmosphere/
│   ├── __init__.py
│   ├── interface.py          → IAtmosphere: density(alt), pressure(alt),
│   │                           temperature(alt), speed_of_sound(alt)
│   ├── isa1976.py            → International Standard Atmosphere
│   │                           (default, akurat hingga 86 km)
│   ├── nrlmsise00.py         → Model realistis hingga 1000 km
│   │                           (wrapper dari nrlmsise00 package)
│   └── factory.py            → Pilih model dari config
│
├── planet/
│   ├── planet.py             → dataclass Planet: GM, radius, J2, rot_rate
│   ├── earth.py              → Parameter Bumi (WGS84)
│   └── mars.py               → Parameter Mars (untuk interplanetary)
│
├── ephemeris/
│   ├── ephemeris.py          → Interface: posisi planet/bulan di waktu t
│   ├── spice_provider.py     → Wrapper NASA SPICE (via spiceypy)
│   └── table_provider.py     → Tabel sederhana jika tanpa SPICE
│
└── wind/
    ├── wind_model.py         → Interface IWindModel
    ├── constant_wind.py      → Untuk testing & sederhana
    └── profile_wind.py       → Wind vs altitude dari data YAML
```

---

### 5. `simulation/` — Jantung Simulasi
**Tanggung jawab:** Mengkoordinasikan semua model, menjalankan loop integrasi numerik, mendeteksi dan menangani event.

```
simulation/
├── __init__.py
│
├── integrators/
│   ├── __init__.py
│   ├── interface.py          → IIntegrator: step(state, dt) → state
│   ├── rk4.py                → Fixed-step RK4 (referensi & debugging)
│   ├── rk45.py               → Adaptive RK45 via scipy.integrate.solve_ivp
│   │                           (REKOMENDASI DEFAULT)
│   └── factory.py            → Pilih integrator dari config
│
├── engine.py                 → SimulationEngine: main loop, agregasi gaya,
│                               panggil integrator, emit events
├── config.py                 → dataclass SimConfig: dt, t_max, integrator,
│                               model flags, toleransi
├── event_system.py           → EventBus: register/emit/handle events
├── event_detector.py         → Zero-crossing detection: apogee, burnout,
│                               ground impact, stage separation trigger
├── force_aggregator.py       → Kumpulkan semua IForceModel, sum semua gaya
├── state_history.py          → Buffer StateVector tiap timestep →
│                               kembalikan sebagai pandas DataFrame
└── telemetry.py              → Real-time callback saat simulasi berjalan
                                (untuk GUI live update)
```

**Rekomendasi integrator:** Gunakan `scipy.integrate.solve_ivp` dengan method `RK45` sebagai default. Ini adaptive step — otomatis gunakan dt kecil saat liftoff/transonic, dt besar saat coasting — jauh lebih efisien dari fixed RK4.

**`force_aggregator.py`** adalah pola penting:
```python
class ForceAggregator:
    def __init__(self):
        self._models: list[IForceModel] = []

    def register(self, model: IForceModel):
        self._models.append(model)

    def total_force(self, state: StateVector, env) -> np.ndarray:
        return sum(m.compute(state, env) for m in self._models)
```
Dengan ini, menambah atau mencopot model fisika cukup satu baris tanpa ubah logika integrator.

---

### 6. `io/` — Data Layer
**Tanggung jawab:** Semua baca/tulis file. Modul lain **tidak boleh** langsung baca file YAML/JSON.

```
io/
├── __init__.py
│
├── parsers/
│   ├── vehicle_parser.py     → YAML → RocketVehicle (+ validasi schema)
│   ├── simconfig_parser.py   → YAML → SimConfig
│   ├── engine_parser.py      → YAML → EngineRegistry
│   └── validator.py          → jsonschema validasi file input
│
├── exporters/
│   ├── telemetry_exporter.py → DataFrame → JSON / CSV / YAML
│   ├── report_generator.py   → Results → PDF (via WeasyPrint / ReportLab)
│   └── kml_exporter.py       → Trajectory → KML (Google Earth)
│
└── schema/
    ├── vehicle.schema.json    → Schema validasi file roket
    └── simconfig.schema.json
```

---

### 7. `analysis/` — Post-Processing & Sains
**Tanggung jawab:** Semua analisis hasil simulasi. Ini yang paling sering dipakai di Jupyter Notebook.

```
analysis/
├── __init__.py
├── trajectory.py         → Hitung apogee, max-Q, burnout alt, range
├── performance.py        → Delta-V per stage, Isp efektif, mass fraction
├── stability.py          → Static margin, CP vs CG over time
├── plots.py              → Matplotlib/Plotly: altitude-time, velocity-time,
│                           trajectory 2D/3D, force breakdown
└── compare.py            → Bandingkan 2+ simulasi (misal vs RocketPy)
                            untuk validasi
```

**`compare.py`** penting untuk validasi — bisa load hasil RocketPy dan overlay dengan hasil simulasi ini untuk cross-check akurasi.

---

### 8. `viz/` — Visualisasi
**Tanggung jawab:** GUI desktop real-time dan web dashboard. Pisah dari `analysis/` karena dependency-nya berat dan opsional.

```
viz/
├── __init__.py
│
├── desktop/
│   ├── app.py                → PyQt6 / PySide6 main window
│   ├── gl_viewport.py        → OpenGL 3D globe + trajectory
│   │                           (via PyOpenGL atau VisPy)
│   ├── telemetry_panel.py    → Live altitude, velocity, acceleration
│   ├── stage_panel.py        → Status stage, propellant gauge
│   ├── plot_panel.py         → Matplotlib embedded, update real-time
│   └── sim_bridge.py         → Thread-safe bridge: sim thread ↔ GUI thread
│                               (pakai queue.Queue)
│
└── web/
    ├── app.py                → Dash (Plotly) atau Streamlit app
    ├── layout.py             → Layout halaman dashboard
    ├── callbacks.py          → Interaktivitas: upload YAML, run sim, plot
    └── globe.py              → Plotly 3D globe untuk trajectory
```

**Rekomendasi:** Untuk **desktop** pakai **PyQt6 + VisPy** (performa OpenGL bagus untuk 3D). Untuk **web dashboard** pakai **Dash** (lebih fleksibel untuk riset) atau **Streamlit** (lebih cepat dibuat).

`sim_bridge.py` wajib ada karena simulasi berjalan di background thread — tanpa bridge yang benar, GUI akan freeze.

---

## Dependency Graph Antar Modul

```
viz/desktop ──────────────────────────────────────┐
viz/web ───────────────────────────────────────┐  │
analysis ──────────────────────────────────┐   │  │
io ─────────────────────────────────────┐  │   │  │
                                        ↓  ↓   ↓  ↓
                                    [ simulation ]
                                     ↓    ↓    ↓
                              [models] [vehicle] [environment]
                                     ↓    ↓    ↓
                                      [ core ]
                                    (no deps)
```

**Aturan keras:** Dependency hanya boleh ke bawah. `core` tidak boleh import apapun dari package ini sendiri.

---

## Stack Library per Modul

| Modul             | Library Utama                           |
| ----------------- | --------------------------------------- |
| `core`            | `numpy`, `dataclasses`                  |
| `models/aero`     | `numpy`, `scipy.interpolate`            |
| `models/gravity`  | `numpy`, `spiceypy` (opsional)          |
| `environment/atm` | `numpy`, `nrlmsise00`                   |
| `simulation`      | `scipy.integrate`, `numpy`              |
| `io`              | `pyyaml`, `jsonschema`, `pandas`        |
| `analysis`        | `pandas`, `matplotlib`, `plotly`        |
| `viz/desktop`     | `PyQt6`, `vispy`                        |
| `viz/web`         | `dash` atau `streamlit`, `plotly`       |
| `tests`           | `pytest`, `hypothesis`, `numpy.testing` |

---

## Strategi Testing & Validasi

```
tests/
├── unit/
│   ├── test_core/            → Test StateVector, koordinat, quaternion
│   ├── test_models/          → Test tiap model fisika dengan input diketahui
│   ├── test_vehicle/         → Test stage separation logic
│   └── test_integrators/     → Test RK4 vs analytical solution sederhana
│
├── integration/
│   ├── test_full_flight/     → Sub-orbital end-to-end, cek apogee masuk akal
│   └── test_multistage/      → Pastikan separasi berjalan benar
│
└── validation/
    ├── vs_rocketpy/          → Jalankan kasus yang sama di RocketPy,
    │                           bandingkan trajectory & apogee
    └── vs_analytical/        → Kasus sederhana (tanpa drag) vs solusi
                                analitik Tsiolkovsky
```

**Validasi vs RocketPy** adalah cara paling solid untuk riset — jika hasil kedua software dalam toleransi 1-2%, model fisika dianggap valid.

---

## Ringkasan Pemisahan Tanggung Jawab

| Modul         | Satu kalimat tanggung jawab                               |
| ------------- | --------------------------------------------------------- |
| `core`        | Tipe data & matematika, tidak tahu apapun tentang roket   |
| `models`      | Hitung satu jenis gaya, tidak tahu tentang roket lainnya  |
| `vehicle`     | Struktur roket & stage, tidak tahu cara terbang           |
| `environment` | Kondisi luar (atmosfer, planet), tidak tahu tentang roket |
| `simulation`  | Koordinasi semua model, jalankan loop waktu               |
| `io`          | Baca/tulis file saja, tidak tahu cara simulasi            |
| `analysis`    | Olah hasil simulasi untuk insight sains                   |
| `viz`         | Tampilkan data, tidak hitung apapun                       |

---

MVP yang disarankan: mulai dari `core` → `models` → `vehicle` → `simulation` → `io`, bisa langsung dipakai via Jupyter Notebook. Tambahkan `viz` dan `analysis` setelahnya. Mau lanjut ke implementasi modul pertama?