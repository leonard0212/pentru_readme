# 📘 README – Etapa 4: Arhitectura Completă a Aplicației SIA bazată pe Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** [Nume Prenume]  
**Link Repository GitHub:** https://github.com/[user]/PCB-Deffects-Detector
**Data:** 03.12.2025
---

## Scopul Etapei 4

Această etapă corespunde punctului **5. Dezvoltarea arhitecturii aplicației software bazată pe RN** din lista de 9 etape.

**Obiectiv:** Livrarea unui SCHELET COMPLET și FUNCȚIONAL al întregului Sistem cu Inteligență Artificială (SIA) pentru detecția defectelor pe plăci electronice (PCB).

---

## Livrabile Obligatorii

### 1. Tabelul Nevoie Reală → Soluție SIA → Modul Software

| **Nevoie reală concretă** | **Cum o rezolvă SIA-ul vostru** | **Modul software responsabil** |
|---------------------------|--------------------------------|--------------------------------|
| Reducerea timpului de inspecție manuală a PCB-urilor (actual 30s/placă) | Automatizarea detecției vizuale și clasificare instantaneă (< 500ms) a defectelor | **Neural Network (YOLOv8)** + **Camera Manager** |
| Identificarea precisă a defectelor microscopice (scurtcircuite, componente lipsă) | Analiză de imagine cu rezoluție înaltă și bounding box detection cu acuratețe > 90% | **AI Inference Module** + **Image Preprocessing** |
| Oprirea automată a liniei de producție la detectarea unui defect critic | Comunicare serială cu conveiorul pentru oprire imediată la semnalul de defect | **Serial Comm Manager** + **Main Control Loop** |
| Trasabilitatea producției și jurnalizarea defectelor | Salvarea automată a log-urilor și imaginilor cu defecte pentru analiză ulterioară | **Data Logging / UI Module** |

---

### 2. Contribuția Voastră Originală la Setul de Date – MINIM 40% din Totalul Observațiilor Finale

### Contribuția originală la setul de date:

**Total observații finale:** 2500 imagini (1500 Publice + 1000 Originale)
**Observații originale:** 1000 imagini (40%)

**Tipul contribuției:**
[ ] Date generate prin simulare fizică
[X] Date achiziționate cu senzori proprii
[X] Etichetare/adnotare manuală
[ ] Date sintetice prin metode avansate  

**Descriere detaliată:**
Am construit un setup experimental constând dintr-un stand fix cu iluminare controlată (inel LED) și o cameră web HD montată perpendicular pe planul de inspecție. Am achiziționat 1000 de imagini cu diverse plăci PCB (Arduino Uno, ESP32, plăci custom), simulând defecte reale:
1. **Componente lipsă:** Am dezlipit temporar condensatori și rezistori.
2. **Scurtcircuite:** Am creat punți de fludor intenționate între pini.
3. **Întreruperi:** Am mascat trasee sau am folosit plăci rebutate.

Toate cele 1000 de imagini au fost adnotate manual folosind **Roboflow/LabelImg**, desenând bounding boxes pentru clasele: `missing_component`, `short_circuit`, `open_circuit`. Această contribuție este esențială deoarece dataset-urile publice (ex: PCB-Defect-Dataset) nu conțineau variațiile de iluminare specifice mediului meu de testare.

**Locația codului:** `AOI_System/src/camera.py` (folosit pentru captură)
**Locația datelor:** `data/generated/`
**Dovezi:**
- Setup experimental: `docs/acquisition_setup.jpg`
- Exemplu adnotare: `docs/annotation_example.png`

---

### 3. Diagrama State Machine a Întregului Sistem

Diagrama este salvată în: `docs/state_machine.png`

### Justificarea State Machine-ului ales:

Am ales o arhitectură de tip **Event-Driven Control Loop** (Buclă de control bazată pe evenimente) specifică sistemelor AOI (Automated Optical Inspection).

**Stările principale sunt:**
1. **IDLE:** Sistemul așteaptă comenzi, banda este oprită.
2. **MOVING_CONVEYOR:** Banda transportoare este activă, așteptând ca senzorul IR să detecteze prezența unei plăci.
3. **OBSTACLE_DETECTED:** Senzorul Arduino trimite semnalul, banda se oprește automat pentru a stabiliza imaginea.
4. **ACQUIRE & INFERENCE:** Camera preia cadrul curent, iar modelul YOLO îl analizează.
5. **DECISION & LOG:** Dacă se detectează defect (`defect_found=True`), se loghează eroarea și se afișează bounding box-urile.
6. **ERROR/RECOVERY:** Gestionarea cazurilor în care camera nu răspunde sau conexiunea serială se pierde.

**Tranzițiile critice:**
- `MOVING` → `OBSTACLE_DETECTED`: Critică pentru poziționarea corectă a plăcii sub cameră.
- `INFERENCE` → `LOG`: Decizia de a valida sau respinge placa se face aici.

Această mașină de stări asigură că inferența AI se face doar pe imagini statice (fără motion blur), maximizând acuratețea detecției.

---

### 4. Scheletul Complet al celor 3 Module

Sistemul este implementat modular în Python, având ca punct central `main.py`.

#### **Modul 1: Data Logging / Acquisition & Hardware Interface**
- **Locație:** `AOI_System/src/camera.py` și `AOI_System/src/serial_comm.py`
- **Funcționalitate:**
  - `CameraManager` gestionează conexiunea cu camera web sau fluxul IP, permițând captura cadru cu cadru.
  - `SerialManager` comunică bidirecțional cu Arduino (COM port), trimițând comenzi de Start/Stop bandă și citind senzorii de prezență.
- **Status:** Funcțional. Comunică cu hardware-ul și preia imagini.

#### **Modul 2: Neural Network Module**
- **Locație:** `AOI_System/src/ai_inference.py`
- **Funcționalitate:**
  - Încapsulează modelul YOLOv8 folosind biblioteca `ultralytics`.
  - Metoda `predict(frame)` returnează imaginea adnotată și flag-ul boolean `defect_found`.
  - În această etapă, modelul este instanțiat (`pcb_model.pt`) și pregătit pentru inferență.
- **Status:** Funcțional. Modelul se încarcă și execută inferență (chiar dacă weights-urile nu sunt încă finale/optimale).

#### **Modul 3: Web Service / UI**
- **Locație:** `AOI_System/src/main.py`
- **Tehnologie:** Python Tkinter
- **Funcționalitate:**
  - Interfață grafică desktop pentru operator.
  - Afișează fluxul video live cu suprapunerea detecțiilor AI.
  - Panou de control pentru pornirea/oprirea manuală a conveiorului.
  - Jurnal (Log box) pentru afișarea text a evenimentelor și defectelor detectate.
- **Status:** Funcțional. Fereastra pornește, butoanele răspund la comenzi, video-ul rulează.

---

## Structura Repository-ului la Finalul Etapei 4

```
PCB-Deffects-Detector-main/
├── AOI_System/
│   ├── config/
│   │   └── config.py          # Parametri globali (Porturi, Thresholds)
│   ├── data/
│   │   ├── generated/         # Imaginile proprii (40%)
│   │   └── raw/               # Dataset public
│   ├── docs/
│   │   ├── state_machine.png  # Diagrama flux
│   │   └── screenshots/       # Dovezi UI
│   ├── models/
│   │   └── pcb_model.pt       # Modelul YOLO (definit)
│   ├── src/
│   │   ├── ai_inference.py    # Modul RN
│   │   ├── camera.py          # Modul Achiziție
│   │   ├── main.py            # Modul UI & Logică Principală
│   │   └── serial_comm.py     # Modul Hardware
│   └── requirements.txt       # Dependențe (ultralytics, opencv, pyserial)
├── README_Etapa4_Arhitectura_SIA_03.12.2025.md
└── README_Etapa5_Antrenare_RN.md
```

## Checklist Final
- [x] Tabelul Nevoie → Soluție completat.
- [x] Declarație contribuție 40% date originale justificată (setup propriu).
- [x] Diagrama State Machine justificată (Control Loop AOI).
- [x] Modulele `camera`, `serial`, `ai`, `ui` sunt implementate și interconectate.
- [x] Repository structurat corect.
