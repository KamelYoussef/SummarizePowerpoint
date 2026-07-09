Voici une traduction en français de votre aperçu pratique de l'écosystème ASR (transcription) en Python, suivi du tableau comparatif.

---

## Les principales options en Python

### Modèles Hugging Face / à poids ouverts (*open-weight*) — Priorité

* **`openai/whisper` (via *transformers* ou le package original `openai-whisper`)** — La référence (*baseline*), multilingue, disponible en plusieurs tailles.
* **`faster-whisper` (SYSTRAN, backend CTranslate2)** — Utilise les mêmes poids que Whisper, mais beaucoup plus rapide et léger. C'est le choix incontournable pour la production.
* **`WhisperX`** — Encapsule `faster-whisper` et y ajoute l'alignement forcé (horodatages au niveau du mot) ainsi que la diarisation des locuteurs via `pyannote`. C'est probablement ce qu'il vous faut si le terme « annotation » implique d'identifier les locuteurs et les horodatages.
* **`distil-whisper` / `faster-distil-large-v3**` — Version distillée de Whisper, environ 6 fois plus rapide, avec une précision quasi identique.
* **`NVIDIA Parakeet / Canary (NeMo)`** — Désormais multilingue (25 langues européennes, dont le français) depuis les versions v2/v3. Ces modèles dominent actuellement le classement *HF Open ASR Leaderboard* en termes de précision et de débit (*throughput*).
* **Modèles affinés (*fine-tunes*) spécifiques au français** : `bofenghuang/whisper-medium-french`, `pierreguillou/whisper-medium-french`, modèles LeBenchmark wav2vec2 (`facebook/wav2vec2-large-xlsr-53-french`). Intéressants si votre contenu audio est exclusivement en français et que vous cherchez à maximiser la précision.
* **`pyannote.audio`** — Ne fait pas de transcription en soi, mais c'est la référence pour la diarisation du locuteur (« qui parle quand »). Il est généralement associé à l'un des modèles ci-dessus.

### Options Hors-HF / API (Cloud)

* **Deepgram, AssemblyAI, Google Speech-to-Text, Azure Speech, OpenAI API (`gpt-4o-transcribe`)** — Solutions cloud, aucun GPU requis, meilleures pour le streaming en temps réel et intègrent nativement la diarisation. Cependant, elles sont payantes et ne garantissent pas une confidentialité locale des données.

---

## Tableau comparatif (*Benchmark*)

Les chiffres proviennent de benchmarks publiés (tests sur des clips audio de 13 minutes, WER sur LibriSpeech/Common Voice/Fleurs, HF Open ASR Leaderboard). Ils sont donnés à titre indicatif : les résultats réels dépendront de votre GPU, de la qualité audio et des accents.

| Outil / Modèle | VRAM GPU | Vitesse (par rapport au temps réel) | Support du français | Adapté au temps réel | Annotation du locuteur (Diarisation) | Taux d'erreur (WER) |
| --- | --- | --- | --- | --- | --- | --- |
| **openai/whisper large-v3** (PyTorch, fp16) | ~10 Go (Whisper Large v3 requiert au moins 10 Go de VRAM) | ~1x (référence, lent) | Bon, mais moins performant qu'en anglais. Le WER moyen selon les langues peut grimper jusqu'à 24,9 % en français sur certains benchmarks forensiques. | Non (traitement par lots uniquement) | ❌ (nécessite l'extension pyannote) | ~7–9 % en général, plus élevé pour le français avec accent ou bruité. |
| **faster-whisper** (large-v3, int8) | ~2,5–3 Go (Large-v3 int8 sur une RTX 4070 tourne à environ 12x le temps réel et utilise environ 2,5 Go de VRAM) | ~10–12x plus rapide que le temps réel sur un GPU moyen. | Mêmes poids que Whisper, même WER. Le taux d'erreur par mot est identique à Whisper puisque seule la méthode de calcul change. | Oui, avec découpage en blocs (chunking) / VAD | ❌ (à associer avec pyannote) | Identique à Whisper large-v3. |
| **faster-distil-large-v3** | ~1,5–2,4 Go (A utilisé environ 1481 Mo en int8 et 2409 Mo en fp16 lors d'un benchmark de 13 minutes) | ~6x plus rapide que large-v3. Distil-Whisper atteint une vitesse d'inférence 6x supérieure tout en restant à moins de 1 % de différence de WER sur des audios hors distribution. | Même couverture linguistique que Whisper, WER légèrement plus élevé. | Oui | ❌ | ~1 % de moins (plus de fautes) que large-v3. |
| **large-v3-turbo** (faster-whisper) | ~1,5–2 Go | ~2x plus rapide que large-v3, précision quasi identique. Whisper Large V3 Turbo offre une inférence 6x plus rapide que Large V3 (via l'architecture d'origine) en réduisant les couches du décodeur de 32 à 4. | Bon | Oui | ❌ | À 1–2 % près de large-v3. |
| **WhisperX** (faster-whisper + alignement + pyannote) | ~4–6 Go (modèle Whisper + modèle de diarisation) | Similaire à faster-whisper, avec le coût de calcul de la diarisation en plus. | Identique au modèle Whisper sous-jacent. | Quasi temps réel avec traitement par lots | ✅ Horodatages au niveau du mot + identification des locuteurs. | Même WER pour l'ASR ; l'erreur de diarisation est distincte (~5–15 % de DER typique). |
| **NVIDIA Canary-1B-v2** | ~4–6 Go | Débit élevé, « jusqu'à 10x plus rapide que des modèles de qualité comparable ». Canary-1B-v2 offre une qualité de transcription et de traduction comparable à des modèles 3x plus grands. | Support explicite du français, en tête du classement. Canary transcrit l'anglais, l'espagnol, l'allemand et le français avec un WER moyen de 6,67 % sur le HF Open ASR Leaderboard. | Non conçu pour le streaming | Ponctuation et capitalisation intégrées, pas de diarisation native. | ~6,3–6,7 % en moyenne (multilingue). |
| **NVIDIA Parakeet-TDT-0.6B-v3** | ~2–3 Go (0.6B paramètres) | Débit le plus élevé parmi les modèles ouverts multilingues (mesuré par la durée audio transcrite divisée par le temps de calcul). | 25 langues dont le français. Le modèle détecte automatiquement la langue de l'audio sans configuration requise. | Oui, conçu pour le streaming / temps réel | Pas de diarisation native (une variante multi-locuteurs distincte existe). | Compétitif avec Canary, légèrement en retrait sur les tâches optimisées pour la précision stricte. |
| **wav2vec2-FR** (LeBenchmark / XLSR-53-French) | ~2–4 Go | Rapide (CTC, non-autorégressif) | Spécifique au français, affiné sur Common Voice FR. | Oui (le CTC est très léger) | ❌ | Généralement derrière Whisper pour le français lors des tests comparatifs. Le WER de Wav2Vec2.0 varie de 13,1 % à 34,8 %, générant globalement plus d'erreurs que Whisper. |
| **Deepgram Nova-3** (API, non-HF) | 0 (Cloud) | Streaming en temps réel, optimisé pour la production. | Supporté | Oui, conçu spécifiquement pour le streaming. | ✅ Intégrée | Compétitif, ~5–8 % selon le domaine. |
| **OpenAI gpt-4o-transcribe** (API, non-HF) | 0 (Cloud) | Appel API rapide | Supporté | Oui | ❌ (pas de diarisation native) | En tête des benchmarks de précision avec un WER d'environ 2,46 % sur les ensembles de tests majoritairement en anglais (non confirmé séparément pour le français). |

---

## Mon avis pour un projet de transcription en français

* **Si vous voulez une solution locale, gratuite et avec diarisation** : Optez pour **WhisperX** (avec un backend *large-v3* ou *large-v3-turbo*) + **pyannote**. C'est la pile (*stack*) la plus courante pour transcrire des réunions ou des entretiens en français avec identification des locuteurs.
* **Si vous cherchez la meilleure précision sur le français (ou du multilingue) avec une bonne vitesse, sans besoin de diarisation** : Choisissez **nvidia/canary-1b-v2**.
* **Si vous voulez un débit maximal sur du matériel modeste** : Utilisez **faster-whisper** avec **distil-large-v3** ou **large-v3-turbo** en quantification **int8**.
* **Si vous devez absolument gratter le moindre pourcent de précision en français** : Testez une version affinée comme `bofenghuang/whisper-medium-french` face au Whisper `large-v3` de base sur un échantillon de vos propres fichiers audio. Les modèles affinés sous-performent parfois par rapport au modèle généraliste lorsqu'ils sortent de leur domaine d'entraînement, il est donc crucial de comparer les deux.
