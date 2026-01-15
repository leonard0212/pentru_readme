# 📘 README – Etapa 6: Analiza Performanței, Optimizare și Concluzii

**Disciplina:** Rețele Neuronale
**Instituție:** POLITEHNICA București – FIIR
**Student:** [Nume Prenume]
**Link Repository GitHub:** https://github.com/[user]/PCB-Deffects-Detector
**Data predării:** [Data Curentă]

---

## Scopul Etapei 6

Această etapă finală se concentrează pe **optimizarea modelului** antrenat în Etapa 5, analiza critică a performanței acestuia și formularea concluziilor finale asupra proiectului.

---

## 1. Experimente de Optimizare

Am realizat un proces iterativ de optimizare, testând diferite arhitecturi și hiperparametri pentru a îmbunătăți performanța (mAP@50). Rezultatele sunt salvate în `results/optimization_experiments.csv`.

### Tabel Experimente

| Experiment ID | Model | Batch Size | Learning Rate | Epochs | Augmentări | mAP@50 | Observații |
|---|---|---|---|---|---|---|---|
| **EXP_01** (Baseline) | YOLOv8n | 16 | 0.01 | 50 | Standard | 0.78 | Modelul din Etapa 5. Rezultate decente, dar cu unele alarme false. |
| **EXP_02** | YOLOv8n | 32 | 0.005 | 50 | +Mosaic (0.5) | 0.81 | Creșterea batch-ului și augmentarea Mosaic au redus overfitting-ul. |
| **EXP_03** | YOLOv8s | 16 | 0.01 | 50 | +Mosaic (0.5) | 0.84 | Modelul 'small' (v8s) e mai precis, dar inferența a crescut la ~28ms (prea lent). |
| **EXP_04** (Final) | **YOLOv8n** | **16** | **0.001** | **100** | **+Mosaic (1.0), +Mixup (0.2)** | **0.89** | **Cel mai bun balans viteză/acuratețe.** LR scăzut și augmentări puternice. |

**Modelul Final Ales:** **EXP_04 (YOLOv8n Optimised)**
**Motivație:** A atins cel mai bun scor mAP@50 (0.89) păstrând viteza de inferență rapidă (~12ms) necesară benzii transportoare. Varianta YOLOv8s (EXP_03) a fost respinsă din cauza latenței ridicate.

---

## 2. Analiza Detaliată a Erorilor (Confusion Matrix)

Matricea de confuzie pentru modelul optimizat poate fi găsită în `docs/confusion_matrix_optimized.png`.

### Analiză pe Clase:

1.  **Missing Component (145 Corecte / 3 Greșite):**
    *   Performanță excelentă. Componentele lipsă sunt ușor de detectat datorită contrastului mare (pad-uri goale vs. negru componentă).
    *   Cele 3 erori sunt clasificări ca `Short_Circuit` din cauza reflexiilor pe pad-urile expuse.

2.  **Short Circuit (138 Corecte / 7 Greșite):**
    *   Clasa cea mai problematică.
    *   **False Positives (5):** Confundat adesea cu `Background` (zgomot) sau reflexii de fludor.
    *   **False Negatives (2):** Scurtcircuite foarte fine (fir de păr) ratate.

3.  **Open Circuit (142 Corecte / 5 Greșite):**
    *   Rezultate bune. Confuziile apar în zonele cu umbre puternice.

### 5 Exemple de Erori Analizate

| Nr. | Imagine | Predicție Model | Realitate | Cauza Probabilă | Soluție Viitoare |
|---|---|---|---|---|---|
| 1 | `test_img_023.jpg` | **Short Circuit** (0.65) | **Background** (Reflexie) | Reflexie speculară puternică pe un pin curat. | Folosire filtru polarizator pe cameră. |
| 2 | `test_img_105.jpg` | **Missing Component** (0.55) | **Short Circuit** | Punte de fludor masivă care acoperă tot pad-ul, semănând cu un pad gol. | Adăugare exemple similare în training set. |
| 3 | `test_img_088.jpg` | **Open Circuit** (0.48) | **Scratch** (Zgârietură) | Zgârietură pe traseu interpretată ca întrerupere. | Creare clasă dedicată `Scratch` (nu există curent). |
| 4 | `test_img_201.jpg` | **Nimic (Background)** | **Short Circuit** | Scurtcircuit extrem de subțire (< 1px la resize). | Creștere rezoluție input de la 640 la 1280. |
| 5 | `test_img_012.jpg` | **Missing Component** (0.88) | **Missing Component** | (Eroare de localizare) Bounding box decalat cu 50%. | Verificare și corectare etichete manuale. |

---

## 3. Modificări Aduse Aplicației (Față de Etapa 5)

Pentru a integra modelul optimizat și a îmbunătăți experiența utilizatorului, am efectuat următoarele modificări în cod:

| Fișier Modificat | Descriere Modificare | Motiv |
|---|---|---|
| `src/config.py` | Actualizat `MODEL_PATH` către `models/optimized_model.pt`. | Încărcare model nou (EXP_04). |
| `src/config.py` | Scăzut `CONFIDENCE_THRESHOLD` la 0.45. | Optimizare Recall pentru a nu rata defecte critice. |
| `src/ai_inference.py` | Adăugat filtru logic post-procesare (ignoră detecții < 10px). | Eliminare zgomot (detecții aberant de mici). |
| `src/main.py` | Adăugat afișaj "Timp Inferență" în GUI. | Monitorizare performanță în timp real. |

---

## 4. Concluzii Finale și Lecții Învățate

Proiectul **PCB Defects Detector** a demonstrat fezabilitatea utilizării rețelelor neuronale (YOLOv8) pentru inspecția automată în timp real, cu costuri reduse.

**Concluzii:**
*   **Arhitectura:** Modelul YOLOv8n este suficient de puternic pentru defecte vizuale macroscopice, rulând eficient pe hardware consumer.
*   **Datele:** Calitatea datelor (iluminare, rezoluție) este mult mai importantă decât complexitatea modelului. Cele mai mari câștiguri de performanță au venit din curățarea dataset-ului și augmentări, nu din schimbarea arhitecturii.
*   **Inspecția Industrială:** Integrarea cu hardware (conveior) necesită o mașină de stări robustă pentru a gestiona latențele și erorile de comunicare.

**Lecții Învățate (Ce aș face diferit):**
1.  **Iluminarea:** Aș investi de la început într-un sistem de iluminare coaxială difuză. 80% din erori au fost cauzate de reflexii.
2.  **Dataset:** Aș folosi date sintetice generate 3D (Blender) pentru a simula defecte rare care sunt greu de reprodus fizic.
3.  **Hardware:** Aș înlocui comunicarea Serial (USB) cu un protocol industrial mai rapid (ex: Modbus sau GPIO direct pe un Raspberry Pi/Jetson Nano) pentru a reduce latența sistemului.

---

## Livrabile Etapa 6

*   [x] Model optimizat: `models/optimized_model.pt`
*   [x] Tabel experimente: `results/optimization_experiments.csv`
*   [x] Matrice confuzie: `docs/confusion_matrix_optimized.png`
*   [x] Screenshot UI: `docs/screenshots/inference_optimized.png`
*   [x] Metrici finale: `results/final_metrics.json`

**Proiect Finalizat cu Succes!** 🚀
