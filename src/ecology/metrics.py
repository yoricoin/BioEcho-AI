"""
Module de Métriques Écologiques et d'Évaluation de la Biodiversité.

Fournit le calcul des indices standards reconnus par la communauté scientifique :
- Richesse Spécifique (S)
- Indice de Diversité de Shannon (H')
- Équitabilité de Pielou (J')
- Indice de Diversité de Simpson (1 - D)
- Analyse des rythmes circadiens (répartition temporelle)
- Détection des alertes d'espèces menacées (UICN)
"""

import math
from collections import Counter
from typing import Dict, List, Any, Optional

# Classification officielle UICN (Union Internationale pour la Conservation de la Nature)
IUCN_WEIGHTS = {
    "CR": {"label": "En danger critique d'extinction", "priority": 1, "alert": True},
    "EN": {"label": "En danger", "priority": 2, "alert": True},
    "VU": {"label": "Vulnérable", "priority": 3, "alert": True},
    "NT": {"label": "Quasi menacé", "priority": 4, "alert": False},
    "LC": {"label": "Préoccupation mineure", "priority": 5, "alert": False},
    "None": {"label": "Non applicable / Non évalué", "priority": 6, "alert": False}
}

def species_richness(species_counts: Dict[str, int]) -> int:
    """
    Calcule la Richesse Spécifique (S) : nombre total d'espèces distinctes identifiées.
    Exclut les détections vides ou non identifiées ('None', 'empty').
    """
    valid_species = [s for s, c in species_counts.items() if s not in ("None", "empty", "unknown", "") and c > 0]
    return len(valid_species)

def shannon_diversity_index(species_counts: Dict[str, int]) -> float:
    """
    Calcule l'Indice de Diversité de Shannon (H') :
    H' = - sum(p_i * ln(p_i))
    où p_i est la proportion relative de l'espèce i (n_i / N).
    
    Interprétation :
    - Plus H' est élevé, plus l'écosystème est diversifié et équilibré.
    - Typiquement compris entre 1.5 et 3.5 dans les habitats naturels tempérés.
    """
    filtered = {s: c for s, c in species_counts.items() if s not in ("None", "empty", "unknown", "") and c > 0}
    total_individuals = sum(filtered.values())
    
    if total_individuals == 0 or len(filtered) <= 1:
        return 0.0
    
    h_prime = 0.0
    for count in filtered.values():
        p_i = count / total_individuals
        h_prime -= p_i * math.log(p_i)
        
    return round(h_prime, 4)

def pielou_evenness(h_prime: float, richness: int) -> float:
    """
    Calcule l'Équitabilité de Pielou (J') :
    J' = H' / ln(S)
    
    Interprétation :
    - Varie entre 0 et 1.
    - Proche de 1 : les espèces sont représentées en proportions égales.
    - Proche de 0 : une ou deux espèces sur-dominent l'habitat.
    """
    if richness <= 1:
        return 0.0
    max_h = math.log(richness)
    j_prime = h_prime / max_h
    return round(min(1.0, max(0.0, j_prime)), 4)

def simpson_diversity_index(species_counts: Dict[str, int]) -> float:
    """
    Calcule l'Indice de Diversité de Simpson (1 - D) :
    1 - D = 1 - sum( (n_i * (n_i - 1)) / (N * (N - 1)) )
    
    Représente la probabilité que deux individus tirés au hasard appartiennent à des espèces différentes.
    """
    filtered = {s: c for s, c in species_counts.items() if s not in ("None", "empty", "unknown", "") and c > 0}
    n = sum(filtered.values())
    
    if n <= 1:
        return 0.0
        
    sum_n_ni = sum(count * (count - 1) for count in filtered.values())
    d = sum_n_ni / (n * (n - 1))
    return round(1.0 - d, 4)

def analyze_circadian_rhythm(timestamps_or_hours: List[int]) -> Dict[str, Any]:
    """
    Classe les heures d'observation selon 4 créneaux écologiques majeurs :
    - Aube (Dawn) : 05h00 - 08h00
    - Jour (Day) : 08h00 - 18h00
    - Crépuscule (Dusk) : 18h00 - 21h00
    - Nuit (Night) : 21h00 - 05h00
    """
    slots = {"Aube (05h-08h)": 0, "Jour (08h-18h)": 0, "Crépuscule (18h-21h)": 0, "Nuit (21h-05h)": 0}
    
    for h in timestamps_or_hours:
        hour = h % 24
        if 5 <= hour < 8:
            slots["Aube (05h-08h)"] += 1
        elif 8 <= hour < 18:
            slots["Jour (08h-18h)"] += 1
        elif 18 <= hour < 21:
            slots["Crépuscule (18h-21h)"] += 1
        else:
            slots["Nuit (21h-05h)"] += 1
            
    total = len(timestamps_or_hours) if timestamps_or_hours else 1
    percentages = {slot: round((count / total) * 100, 1) for slot, count in slots.items()}
    
    return {
        "counts": slots,
        "percentages": percentages,
        "dominant_slot": max(slots, key=slots.get) if timestamps_or_hours else "Aucun"
    }

def generate_ecological_report(observations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Génère un rapport de synthèse écologique complet à partir d'une liste d'observations
    (provenant de caméras et de micros géolocalisés).
    """
    species_counter = Counter()
    iucn_alerts = []
    hours = []
    stations = set()
    modalities = Counter()

    for obs in observations:
        sp = obs.get("scientific_name", "None")
        common = obs.get("common_name", sp)
        status = obs.get("iucn_status", "LC")
        station = obs.get("station_id", "STATION_UNKNOWN")
        modality = obs.get("modality", "unknown")
        
        stations.add(station)
        modalities[modality] += 1
        
        if sp not in ("None", "empty", "unknown", ""):
            species_counter[sp] += 1
            
            # Vérification des alertes d'extinction UICN
            if status in ("CR", "EN", "VU"):
                iucn_alerts.append({
                    "scientific_name": sp,
                    "common_name": common,
                    "status": status,
                    "status_label": IUCN_WEIGHTS.get(status, {}).get("label", "Menacé"),
                    "station_id": station,
                    "modality": modality
                })
                
        # Heure fictive ou fournie
        hour = obs.get("hour", 14)
        hours.append(hour)

    richness = species_richness(species_counter)
    shannon = shannon_diversity_index(species_counter)
    pielou = pielou_evenness(shannon, richness)
    simpson = simpson_diversity_index(species_counter)
    circadian = analyze_circadian_rhythm(hours)

    return {
        "summary": {
            "total_observations": len(observations),
            "total_species_detected": richness,
            "active_stations_count": len(stations),
            "modalities_breakdown": dict(modalities)
        },
        "indices": {
            "species_richness_S": richness,
            "shannon_diversity_H": shannon,
            "pielou_evenness_J": pielou,
            "simpson_diversity_1_minus_D": simpson,
            "diversity_assessment": (
                "Écosystème riche et équilibré" if shannon >= 2.0 and pielou >= 0.75
                else "Diversité moyenne / modérée" if shannon >= 1.0
                else "Faible diversité ou forte dominance d'une seule espèce"
            )
        },
        "iucn_alerts": {
            "threatened_species_count": len(iucn_alerts),
            "details": iucn_alerts
        },
        "circadian_rhythm": circadian
    }

if __name__ == "__main__":
    print("🌿 Test unitaire du moteur écologique BioEcho...")
    test_obs = [
        {"scientific_name": "Canis lupus", "common_name": "Loup gris", "iucn_status": "LC", "station_id": "ST_01", "hour": 23, "modality": "image"},
        {"scientific_name": "Lynx lynx", "common_name": "Lynx boréal", "iucn_status": "VU", "station_id": "ST_02", "hour": 22, "modality": "image"},
        {"scientific_name": "Cervus elaphus", "common_name": "Cerf élaphe", "iucn_status": "LC", "station_id": "ST_01", "hour": 6, "modality": "image"},
        {"scientific_name": "Cervus elaphus", "common_name": "Cerf élaphe", "iucn_status": "LC", "station_id": "ST_03", "hour": 7, "modality": "image"},
        {"scientific_name": "Strix aluco", "common_name": "Chouette hulotte", "iucn_status": "LC", "station_id": "ST_01", "hour": 2, "modality": "audio"},
        {"scientific_name": "Erithacus rubecula", "common_name": "Rouge-gorge", "iucn_status": "LC", "station_id": "ST_02", "hour": 6, "modality": "audio"},
    ]
    
    report = generate_ecological_report(test_obs)
    import pprint
    pprint.pprint(report)
