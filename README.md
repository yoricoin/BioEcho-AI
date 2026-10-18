# 🌿 BioEcho AI - Surveillance & Suivi de la Biodiversité à Grande Échelle

Plateforme multimodale combinant **Vision par Ordinateur** et **Bioacoustique** pour l'observation, le suivi et la préservation de la biodiversité à grande échelle.

Pour le cadre théorique complet, les métriques et l'architecture globale, voir :
👉 **[CADRAGE_PROJET_BIODIVERSITE.md](file:///c:/Users/tahaa/OneDrive/Documentos/9rayya3.0/ECOBIGPROJECT/CADRAGE_PROJET_BIODIVERSITE.md)**

---

## 📌 État d'avancement du projet

### ✅ Jalon 1 : Socle Technique, Données & Moteurs Validés (Terminé)
1. **Environnement virtuel & Dépendances :**
   - Environnement virtuel Python 3.12 configuré (`venv/`).
   - Dépendances scientifiques installées : `librosa`, `soundfile`, `matplotlib`, `numpy`, `pandas`, `scipy`, `scikit-learn`, `fastapi`, `pillow`, `opencv-python`.
   - `.gitignore` configuré pour exclure le `venv` et les gros artefacts.
2. **Jeu d'échantillons multimodal authentique :**
   - 🎙️ **4 enregistrements bioacoustiques réels (WAV)** du benchmark mondial ESC-50 (`data/samples/audio/`) : oiseaux chanteurs, grand corbeau, grillons nocturnes et bruit du vent.
   - 📷 **5 photographies certifiées de pièges photos** (`data/samples/images/`) : loup gris d'Eurasie, lynx boréal (statut VU), cerf élaphe, renard roux et contrôle forêt vide.
   - 📄 **Registre spatio-temporel complet** (`data/samples/metadata.json`) : coordonnées GPS, biome, tranches horaires et statuts UICN.
3. **Moteur d'indices écologiques scientifique (`src/ecology/metrics.py`) :**
   - Richesse spécifique ($S$), Indice de diversité de Shannon ($H'$), Équitabilité de Pielou ($J'$), Indice de Simpson ($1-D$).
   - Analyse des rythmes circadiens (Aube, Jour, Crépuscule, Nuit).
   - Détection des alertes d'espèces menacées selon l'UICN.
4. **Pipeline bioacoustique (`src/audio/processor.py`) :**
   - Transformation des signaux sonores 1D en **Spectrogrammes Mel 2D (dB)**.
   - Calcul des centroïdes spectraux (753 Hz pour le vent jusqu'à 8 694 Hz pour les grillons).
   - Export automatique des spectrogrammes dans `data/samples/spectrograms/`.

---

## 📁 Arborescence du Projet

```text
ECOBIGPROJECT/
├── data/
│   └── samples/
│       ├── audio/              # Fichiers audio .wav réels
│       ├── images/             # Photos authentiques de faune
│       ├── spectrograms/       # Spectrogrammes Mel générés (.png)
│       └── metadata.json       # Métadonnées écologiques & GPS
├── src/
│   ├── audio/
│   │   ├── __init__.py
│   │   └── processor.py        # Générateur de spectrogrammes Mel
│   ├── data/
│   │   ├── __init__.py
│   │   └── download_samples.py # Script d'acquisition des données
│   ├── ecology/
│   │   ├── __init__.py
│   │   └── metrics.py          # Calcul des indices écologiques (Shannon, etc.)
│   ├── vision/                 # (Prévu pour la prochaine séance)
│   └── api/                    # (Prévu pour connecter le Dashboard)
├── web/                        # (Prévu : Interface de restitution & carte)
├── .gitignore
├── requirements.txt
├── README.md
└── CADRAGE_PROJET_BIODIVERSITE.md
```

---

## 🚀 Prochaine Séance (Jalon 2)

1. **Module Vision (`src/vision/detector.py`) :**
   - Détection automatique d'animaux sur pièges photos.
   - Tracé des boîtes englobantes (*Bounding Boxes*), scores de confiance et filtrage du contrôle négatif (forêt vide).
2. **Dashboard Web Interactif (`web/`) :**
   - Carte géographique interactive avec les stations de capteurs géolocalisées.
   - Lecteur audio avec spectrogramme synchronisé.
   - KPIs écologiques en direct et zone de téléversement test (*Drag & Drop*).

---

## ⚡ Commandes utiles pour reprendre

```powershell
# 1. Tester le moteur écologique
.\venv\Scripts\python src/ecology/metrics.py

# 2. Régénérer les spectrogrammes audio
.\venv\Scripts\python src/audio/processor.py
```
