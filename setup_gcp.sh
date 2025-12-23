#!/bin/bash
# Script d'installation automatique pour Google Cloud Compute Engine
# Usage: bash setup_gcp.sh

set -e  # Arrêter en cas d'erreur

echo "=========================================="
echo "  Configuration GCP - Wolof Translator"
echo "=========================================="
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si on est root
if [ "$EUID" -eq 0 ]; then 
   error "Ne pas exécuter en tant que root. Utilisez un utilisateur normal."
   exit 1
fi

info "Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

info "Installation des outils de base..."
sudo apt install -y python3 python3-pip python3-venv git curl wget build-essential

# Vérifier la version de Python
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
info "Version Python détectée: $PYTHON_VERSION"

if [ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.8" ]; then
    warn "Python 3.8+ requis. Installation de Python 3.10..."
    sudo apt install -y software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    sudo apt install -y python3.10 python3.10-venv python3.10-dev
    PYTHON_CMD="python3.10"
else
    PYTHON_CMD="python3"
fi

info "Vérification de la présence d'un GPU..."
if command -v nvidia-smi &> /dev/null; then
    info "GPU détecté !"
    nvidia-smi
    HAS_GPU=true
else
    warn "Pas de GPU détecté. Le projet fonctionnera sur CPU (plus lent)."
    HAS_GPU=false
fi

# Installation de CUDA si GPU disponible
if [ "$HAS_GPU" = true ]; then
    info "Installation des outils NVIDIA..."
    sudo apt install -y nvidia-utils-535 || warn "Impossible d'installer nvidia-utils"
fi

info "Création de l'environnement virtuel..."
$PYTHON_CMD -m venv venv
source venv/bin/activate

info "Mise à jour de pip..."
pip install --upgrade pip

info "Installation de PyTorch..."
if [ "$HAS_GPU" = true ]; then
    info "Installation de PyTorch avec support CUDA..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    info "Installation de PyTorch pour CPU..."
    pip install torch torchvision torchaudio
fi

info "Vérification de l'installation PyTorch..."
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"

info "Installation des dépendances du projet..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    warn "requirements.txt non trouvé. Installation des dépendances de base..."
    pip install transformers datasets evaluate sacrebleu python-dotenv numpy tqdm
fi

info "Création du fichier .env..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
MODEL_CHECKPOINT=facebook/nllb-200-distilled-600M
DATASET_NAME=galsenai/french-wolof-translation
EOF
    info "Fichier .env créé avec les valeurs par défaut"
else
    warn "Fichier .env existe déjà. Pas de modification."
fi

echo ""
echo "=========================================="
echo "  ✅ Installation terminée !"
echo "=========================================="
echo ""
echo "Prochaines étapes :"
echo "  1. Activez l'environnement virtuel : source venv/bin/activate"
echo "  2. Testez l'installation : python3 test_translator.py"
echo "  3. Ou utilisez : python3 debuter.py"
echo ""
echo "Pour désactiver l'environnement virtuel : deactivate"
echo ""

