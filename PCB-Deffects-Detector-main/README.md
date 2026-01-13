# PCB Defects Detector (AOI System)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![YOLOv8](https://img.shields.io/badge/AI-YOLOv8-green)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

**PCB Defects Detector** este un sistem complet de **Inspecție Optică Automată (AOI)** destinat identificării defectelor de fabricație pe plăcile de circuite imprimate (PCB). Proiectul integrează viziunea computerizată (Computer Vision), inteligența artificială (Deep Learning) și controlul hardware industrial (conveior).

---

## 🚀 Funcționalități Principale

- **Detecție în Timp Real:** Utilizează algoritmul **YOLOv8** pentru a identifica și clasifica defectele instantaneu (< 500ms).
- **Tipuri de Defecte:** Detectează automat:
  - 🔍 **Missing Component** (Componente lipsă)
  - ⚡ **Short Circuit** (Scurtcircuite / Punți de fludor)
  - 🛑 **Open Circuit** (Trasee întrerupte)
- **Control Hardware:** Comunică prin port serial cu un **Arduino** pentru a controla o bandă transportoare (Start/Stop automat la detecție).
- **Interfață Grafică (GUI):** Aplicație desktop prietenoasă construită cu **Tkinter**, ce afișează fluxul video live, bounding box-urile AI și log-ul de evenimente.
- **Jurnalizare:** Salvează automat imagini cu defectele detectate și generează rapoarte text.

---

## 🛠️ Arhitectura Sistemului

Sistemul este împărțit în 3 module principale:

1.  **Vision & AI Module:**
    -   Achiziție imagini (Camera Web / IP Camera).
    -   Procesare și inferență folosind modelul antrenat YOLOv8 (`trained_model.pt`).
2.  **Control Module (Hardware Interface):**
    -   Gestionarea comunicării seriale cu microcontroller-ul Arduino.
    -   Comenzi: `'S'` (Start), `'O'` (Opresște), citire senzori obstacol.
3.  **User Interface (UI):**
    -   Vizualizare rezultate și control manual operator.

---

## 📦 Instalare

### 1. Prerequisites
- Python 3.8 sau mai nou.
- Un webcam sau o cameră conectată la PC.
- (Opțional) Arduino conectat pe USB pentru controlul benzii.

### 2. Clonare Repository
```bash
git clone https://github.com/user/PCB-Deffects-Detector.git
cd PCB-Deffects-Detector
```

### 3. Instalare Dependențe
```bash
pip install -r requirements.txt
```
*(Asigurați-vă că aveți instalat `ultralytics`, `opencv-python`, `pyserial`, `pillow`, `tk`)*

---

## 🖥️ Utilizare

1.  **Conectare Hardware:**
    -   Verificați portul COM al Arduino în `AOI_System/src/config.py`.
    -   Asigurați-vă că aveți camera conectată.

2.  **Pornire Aplicație:**
    ```bash
    cd AOI_System/src
    python main.py
    ```

3.  **Flux de Lucru:**
    -   Aplicația va porni și va afișează feed-ul video.
    -   Apăsați **START BANDĂ** pentru a porni conveiorul.
    -   Când o placă este detectată (senzor Arduino) sau vizualizată de AI, sistemul va analiza imaginea.
    -   Dacă se găsește un defect, banda se oprește și eroarea este logată.

---

## 📂 Structură Proiect

```
PCB-Deffects-Detector-main/
├── AOI_System/
│   ├── config/          # Fișiere de configurare
│   ├── data/            # Dataset (imagini raw/processed)
│   ├── docs/            # Documentație și diagrame
│   ├── models/          # Modele AI (.pt, .h5)
│   ├── src/             # Cod sursă Python
│   │   ├── ai_inference.py  # Logica de detecție
│   │   ├── camera.py        # Driver cameră
│   │   ├── main.py          # Entry point și GUI
│   │   └── serial_comm.py   # Driver Serial
│   └── requirements.txt
├── conveior_firmware.ino # Codul pentru Arduino
└── README.md             # Acest fișier
```

---

## 🤖 Tehnologii Folosite

-   **Limbaj:** Python 3
-   **Deep Learning:** Ultralytics YOLOv8 (PyTorch)
-   **Image Processing:** OpenCV
-   **GUI:** Tkinter
-   **Hardware:** Arduino (C++), Serial Communication

---

## 📝 Licență

Acest proiect este licențiat sub [MIT License](LICENSE).
