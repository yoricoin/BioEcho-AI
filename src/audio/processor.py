"""
Module Bioacoustique : Traitement du signal sonore et génération de spectrogrammes Mel.

Transforme le signal audio 1D en une représentation temps-fréquence 2D (Spectrogramme)
utilisable par les modèles de Deep Learning (CNN / Vision Transformers).
"""

import os
import glob
import numpy as np
import librosa
import librosa.display
import matplotlib
matplotlib.use("Agg")  # Mode sans interface graphique pour générer les images proprement
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAMPLES_DIR = os.path.join(BASE_DIR, "data", "samples")
AUDIO_DIR = os.path.join(SAMPLES_DIR, "audio")
SPECTRO_DIR = os.path.join(SAMPLES_DIR, "spectrograms")

os.makedirs(SPECTRO_DIR, exist_ok=True)

def generate_mel_spectrogram(
    audio_path: str,
    output_image_path: str = None,
    target_sr: int = 22050,
    n_mels: int = 128,
    hop_length: int = 512,
    n_fft: int = 2048
) -> dict:
    """
    Charge un fichier audio WAV et génère son spectrogramme Mel en décibels.
    
    Paramètres :
    - audio_path : Chemin vers le fichier .wav
    - output_image_path : Chemin où enregistrer l'image .png générée
    - target_sr : Fréquence d'échantillonnage standardisée
    - n_mels : Nombre de bandes de fréquence sur l'échelle Mel (hauteur de l'image)
    
    Retourne :
    - Dictionnaire avec métadonnées acoustiques (durée, centroïde spectral, énergie moyenne)
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")
        
    # 1. Chargement de l'onde sonore (signal y et fréquence sr)
    y, sr = librosa.load(audio_path, sr=target_sr)
    duration_s = round(float(librosa.get_duration(y=y, sr=sr)), 2)
    
    # 2. Calcul du spectrogramme Mel
    mel_spec = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0
    )
    
    # 3. Conversion de la puissance en Décibels (échelle logarithmique perçue par l'oreille)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    # 4. Calcul d'indicateurs acoustiques de base
    # Centroïde spectral : "centre de gravité" des fréquences (indique si le son est globalement aigu ou grave)
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    mean_centroid_hz = round(float(np.mean(spectral_centroids)), 1)
    
    # Énergie RMS (puissance du son)
    rms = librosa.feature.rms(y=y)[0]
    mean_energy = round(float(np.mean(rms)), 4)
    
    # 5. Enregistrement visuel du Spectrogramme
    if output_image_path:
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(
            mel_spec_db,
            sr=sr,
            hop_length=hop_length,
            x_axis="time",
            y_axis="mel",
            cmap="magma"
        )
        plt.colorbar(format="%+2.0f dB")
        base_title = os.path.basename(audio_path)
        plt.title(f"Spectrogramme Mel : {base_title} | Durée : {duration_s}s | Freq Moyenne : {mean_centroid_hz} Hz", fontsize=11)
        plt.tight_layout()
        plt.savefig(output_image_path, dpi=150)
        plt.close()
        
    return {
        "audio_file": os.path.basename(audio_path),
        "duration_seconds": duration_s,
        "sample_rate_hz": sr,
        "mean_spectral_centroid_hz": mean_centroid_hz,
        "mean_rms_energy": mean_energy,
        "spectrogram_image": os.path.basename(output_image_path) if output_image_path else None
    }

def process_all_samples():
    """Traite automatiquement tous les fichiers audio présents dans data/samples/audio/"""
    wav_files = glob.glob(os.path.join(AUDIO_DIR, "*.wav"))
    if not wav_files:
        print(f"⚠️ Aucun fichier .wav trouvé dans {AUDIO_DIR}")
        return []
        
    print(f"🎙️ Début du traitement bioacoustique de {len(wav_files)} fichiers...")
    results = []
    
    for wav_path in wav_files:
        filename = os.path.basename(wav_path)
        name_no_ext = os.path.splitext(filename)[0]
        spectro_filename = f"{name_no_ext}_spectrogram.png"
        output_png = os.path.join(SPECTRO_DIR, spectro_filename)
        
        print(f"  🎵 Traitement de {filename}...")
        res = generate_mel_spectrogram(wav_path, output_png)
        print(f"     ✅ Spectrogramme généré -> {spectro_filename} (Fréquence moyenne : {res['mean_spectral_centroid_hz']} Hz)")
        results.append(res)
        
    print(f"\n🎉 Traitement terminé ! Les images sont dans data/samples/spectrograms/")
    return results

if __name__ == "__main__":
    process_all_samples()
