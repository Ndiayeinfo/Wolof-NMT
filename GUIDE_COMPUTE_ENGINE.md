# 🖥️ Guide de Configuration - Google Cloud Compute Engine

Ce guide vous explique comment créer et configurer une machine virtuelle sur Google Cloud Compute Engine pour tester et exécuter le projet de traduction français-wolof.

## 📊 Spécifications Recommandées

### 🎯 Option 1 : Pour l'Inférence (Traduction uniquement) - ÉCONOMIQUE

**Utilisation :** Tester le traducteur, faire des traductions  
**Coût estimé :** ~$30-50/mois (selon utilisation)

#### Configuration Recommandée :

```
Type de machine : n1-standard-2 ou e2-standard-2
├── vCPU : 2
├── RAM : 7.5 Go (n1) ou 8 Go (e2)
├── GPU : Aucune (fonctionne sur CPU)
├── Disque : 50 Go SSD (Standard Persistent Disk)
└── OS : Ubuntu 22.04 LTS
```

**Avantages :**
- ✅ Coût réduit
- ✅ Suffisant pour tester et utiliser le traducteur
- ✅ Pas besoin de GPU
- ✅ Démarrage rapide

**Inconvénients :**
- ⚠️ Traductions plus lentes (quelques secondes par phrase)
- ⚠️ Ne convient pas pour l'entraînement

---

### 🚀 Option 2 : Pour l'Entraînement - RECOMMANDÉ

**Utilisation :** Entraîner un modèle personnalisé  
**Coût estimé :** ~$200-400/mois (selon utilisation)

#### Configuration Recommandée :

```
Type de machine : n1-standard-8 avec GPU
├── vCPU : 8
├── RAM : 30 Go
├── GPU : 1x NVIDIA T4 (16 Go VRAM)
├── Disque : 100 Go SSD (Standard Persistent Disk)
└── OS : Ubuntu 22.04 LTS avec CUDA
```

**Spécifications détaillées :**
- **Machine Type :** `n1-standard-8`
- **GPU Type :** `nvidia-tesla-t4`
- **Nombre de GPU :** 1
- **Disque Boot :** 100 Go SSD
- **Disque Additionnel :** 50 Go pour les données (optionnel)

**Avantages :**
- ✅ Entraînement rapide (quelques heures au lieu de jours)
- ✅ Peut gérer de gros datasets
- ✅ Supporte l'entraînement avec mixed precision (FP16)

**Inconvénients :**
- ⚠️ Coût plus élevé
- ⚠️ Nécessite configuration CUDA

---

### 💪 Option 3 : Pour l'Entraînement Intensif - HAUTE PERFORMANCE

**Utilisation :** Entraînement de gros modèles, datasets volumineux  
**Coût estimé :** ~$500-1000/mois (selon utilisation)

#### Configuration Recommandée :

```
Type de machine : n1-standard-16 avec GPU
├── vCPU : 16
├── RAM : 60 Go
├── GPU : 1x NVIDIA V100 (32 Go VRAM) ou 2x NVIDIA T4
├── Disque : 200 Go SSD (Standard Persistent Disk)
└── OS : Ubuntu 22.04 LTS avec CUDA
```

**Spécifications détaillées :**
- **Machine Type :** `n1-standard-16`
- **GPU Type :** `nvidia-tesla-v100` ou `nvidia-tesla-t4` (x2)
- **Nombre de GPU :** 1 ou 2
- **Disque Boot :** 200 Go SSD

---

## 🛠️ Instructions de Création sur Google Cloud

### Étape 1 : Créer la Machine Virtuelle

#### Via la Console Web :

1. **Accédez à Compute Engine :**
   - Allez sur https://console.cloud.google.com
   - Naviguez vers **Compute Engine** > **VM instances**

2. **Cliquez sur "CREATE INSTANCE"**

3. **Configurez les paramètres :**

   **Nom de l'instance :**
   ```
   wolof-translator-vm
   ```

   **Région et Zone :**
   - Choisissez une région proche de vous
   - Exemple : `europe-west1-b` (Belgique) ou `us-central1-a` (Iowa)

   **Type de machine :**
   - Pour inférence : `e2-standard-2` ou `n1-standard-2`
   - Pour entraînement : `n1-standard-8`

   **GPU (uniquement pour entraînement) :**
   - Cochez "Add GPU"
   - Type : `NVIDIA T4` ou `NVIDIA V100`
   - Nombre : 1

   **Disque Boot :**
   - Type : **SSD Persistent Disk**
   - Taille : 50 Go (inférence) ou 100-200 Go (entraînement)
   - Image : **Ubuntu 22.04 LTS**

   **Firewall :**
   - Cochez "Allow HTTP traffic"
   - Cochez "Allow HTTPS traffic"

4. **Cliquez sur "CREATE"**

#### Via gcloud CLI :

**Pour l'inférence (sans GPU) :**
```bash
gcloud compute instances create wolof-translator-vm \
    --zone=europe-west1-b \
    --machine-type=e2-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-standard \
    --tags=http-server,https-server
```

**Pour l'entraînement (avec GPU) :**
```bash
gcloud compute instances create wolof-translator-vm \
    --zone=europe-west1-b \
    --machine-type=n1-standard-8 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=100GB \
    --boot-disk-type=pd-ssd \
    --maintenance-policy=TERMINATE \
    --tags=http-server,https-server
```

⚠️ **Note importante :** Les GPU nécessitent une **quota spéciale** sur Google Cloud. Vous devrez peut-être demander une augmentation de quota.

---

### Étape 2 : Se Connecter à la Machine

#### Via SSH dans la Console Web :
1. Cliquez sur votre instance
2. Cliquez sur "SSH" (ouvre un terminal dans le navigateur)

#### Via gcloud CLI :
```bash
gcloud compute ssh wolof-translator-vm --zone=europe-west1-b
```

#### Via SSH classique :
```bash
ssh -i ~/.ssh/google_compute_engine votre-utilisateur@IP_EXTERNE
```

---

### Étape 3 : Configuration Initiale (Ubuntu)

Une fois connecté, exécutez ces commandes :

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les outils de base
sudo apt install -y python3 python3-pip git curl wget

# Installer Python 3.10+ si nécessaire
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev

# Vérifier la version
python3 --version  # Doit être 3.8 ou supérieur
```

---

### Étape 4 : Installation de CUDA (UNIQUEMENT pour GPU)

Si vous avez une machine avec GPU, installez CUDA :

```bash
# Installer les dépendances
sudo apt install -y build-essential

# Télécharger et installer CUDA 11.8 (compatible avec PyTorch)
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run

# Ajouter CUDA au PATH
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Installer cuDNN (optionnel mais recommandé)
# Téléchargez depuis https://developer.nvidia.com/cudnn
# Suivez les instructions d'installation
```

**Alternative plus simple :** Utilisez l'image Deep Learning de Google Cloud qui inclut déjà CUDA :
```bash
# Lors de la création de la VM, utilisez :
--image-family=common-cu121 \
--image-project=ml-images
```

---

### Étape 5 : Cloner et Installer le Projet

```bash
# Cloner le projet (remplacez par votre repo)
git clone https://github.com/votre-username/Wolof-NMT.git
cd Wolof-NMT

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Pour GPU, installer PyTorch avec support CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

### Étape 6 : Configuration

```bash
# Créer le fichier .env
nano .env
```

Ajoutez :
```bash
MODEL_CHECKPOINT=facebook/nllb-200-distilled-600M
DATASET_NAME=galsenai/french-wolof-translation
```

Sauvegardez avec `Ctrl+O`, puis `Ctrl+X`.

---

### Étape 7 : Tester l'Installation

```bash
# Test simple
python3 test_translator.py

# Ou utiliser le script de démarrage
python3 debuter.py
```

---

## 🔧 Configuration Avancée

### Vérifier la Disponibilité GPU

```bash
# Installer nvidia-smi
sudo apt install -y nvidia-utils-535

# Vérifier
nvidia-smi
```

Vous devriez voir votre GPU listé avec ses spécifications.

### Optimiser les Performances

**Pour l'inférence :**
```python
# Dans votre code, forcez l'utilisation du CPU si GPU non disponible
translator = FrenchWolofTranslator(
    model_checkpoint="facebook/nllb-200-distilled-600M",
    device="cpu"  # ou "cuda" si GPU disponible
)
```

**Pour l'entraînement :**
- Utilisez `fp16=True` dans `TrainingConfig` (déjà activé par défaut)
- Ajustez `per_device_train_batch_size` selon votre GPU

---

## 💰 Estimation des Coûts

### Option 1 (Inférence - e2-standard-2) :
- **Machine :** ~$0.067/heure = ~$50/mois (si utilisé 24/7)
- **Disque :** ~$8/mois (50 Go SSD)
- **Total :** ~$58/mois

### Option 2 (Entraînement - n1-standard-8 + T4) :
- **Machine :** ~$0.38/heure = ~$280/mois (si utilisé 24/7)
- **GPU T4 :** ~$0.35/heure = ~$250/mois
- **Disque :** ~$17/mois (100 Go SSD)
- **Total :** ~$547/mois

⚠️ **Astuce :** Arrêtez la machine quand vous ne l'utilisez pas pour économiser !

```bash
# Arrêter la machine
gcloud compute instances stop wolof-translator-vm --zone=europe-west1-b

# Redémarrer
gcloud compute instances start wolof-translator-vm --zone=europe-west1-b
```

---

## 🚨 Points Importants

### Quotas GPU

Les GPU nécessitent une **quota spéciale** sur Google Cloud :
1. Allez dans **IAM & Admin** > **Quotas**
2. Filtrez par "NVIDIA T4" ou "NVIDIA V100"
3. Demandez une augmentation si nécessaire

### Firewall

Pour accéder à votre application depuis l'extérieur :
```bash
# Autoriser le port 8000 (exemple)
gcloud compute firewall-rules create allow-translator \
    --allow tcp:8000 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow translator API"
```

### Sauvegarde

Créez des snapshots réguliers :
```bash
gcloud compute disks snapshot wolof-translator-vm \
    --snapshot-names wolof-translator-snapshot-$(date +%Y%m%d) \
    --zone=europe-west1-b
```

---

## 📋 Checklist de Déploiement

- [ ] Machine créée avec les bonnes spécifications
- [ ] Connexion SSH fonctionnelle
- [ ] Python 3.8+ installé
- [ ] CUDA installé (si GPU)
- [ ] Projet cloné
- [ ] Dépendances installées
- [ ] Fichier .env configuré
- [ ] Test réussi avec `test_translator.py`
- [ ] GPU détecté (si applicable) avec `nvidia-smi`
- [ ] Firewall configuré (si API externe)
- [ ] Snapshots configurés

---

## 🆘 Dépannage

### GPU non détecté
```bash
# Vérifier les drivers NVIDIA
nvidia-smi

# Si erreur, installer les drivers
sudo apt install -y nvidia-driver-535
sudo reboot
```

### Erreur "CUDA out of memory"
- Réduisez `per_device_train_batch_size` dans `config.py`
- Utilisez `gradient_accumulation_steps` pour simuler des batches plus grands

### Machine trop lente
- Vérifiez l'utilisation CPU/RAM : `htop`
- Vérifiez l'utilisation disque : `df -h`
- Considérez une machine plus puissante

---

## 📚 Ressources Utiles

- [Documentation Compute Engine](https://cloud.google.com/compute/docs)
- [Guide GPU sur GCP](https://cloud.google.com/compute/docs/gpus)
- [Prix Compute Engine](https://cloud.google.com/compute/pricing)
- [Quotas GCP](https://cloud.google.com/compute/quotas)

---

**Bon déploiement ! 🚀**

