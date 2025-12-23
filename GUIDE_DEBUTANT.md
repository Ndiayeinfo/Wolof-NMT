# 🎓 Guide pour Débutants - Traducteur Français-Wolof

Bienvenue ! Ce guide est spécialement conçu pour les personnes qui découvrent ce projet. Nous allons tout expliquer étape par étape.

## 📖 Qu'est-ce que ce projet ?

Ce projet est un **traducteur automatique** qui peut traduire :
- Du **français** vers le **wolof** (langue parlée au Sénégal)
- Du **wolof** vers le **français**

C'est comme Google Translate, mais spécialisé pour le français et le wolof.

## 🎯 Que voulez-vous faire ?

### Option 1 : Juste utiliser le traducteur (le plus simple)
Vous voulez juste traduire du texte ? C'est très simple !

### Option 2 : Entraîner votre propre modèle (plus avancé)
Vous voulez améliorer le traducteur avec vos propres données ? C'est possible mais plus complexe.

**Pour commencer, concentrons-nous sur l'Option 1 !**

---

## ✅ Étape 1 : Vérifier que Python est installé

### Comment vérifier ?

Ouvrez votre terminal (PowerShell sur Windows, Terminal sur Mac/Linux) et tapez :

```bash
python --version
```

**Résultat attendu :** Vous devriez voir quelque chose comme `Python 3.8.x` ou supérieur.

### ❌ Si ça ne marche pas :

1. **Sur Windows :**
   - Téléchargez Python depuis https://www.python.org/downloads/
   - ⚠️ **Important :** Cochez "Add Python to PATH" lors de l'installation
   - Redémarrez votre terminal après l'installation

2. **Sur Mac :**
   ```bash
   # Installez Homebrew si vous ne l'avez pas
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Installez Python
   brew install python
   ```

3. **Sur Linux :**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

---

## ✅ Étape 2 : Installer les dépendances (les outils nécessaires)

### Qu'est-ce qu'une dépendance ?

Ce sont des **outils** que le projet utilise pour fonctionner. Par exemple :
- `torch` : Pour faire fonctionner l'intelligence artificielle
- `transformers` : Pour utiliser les modèles de traduction
- etc.

### Comment installer ?

1. **Ouvrez votre terminal**
2. **Allez dans le dossier du projet** :
   ```bash
   cd C:\Users\YOUSSOU\Desktop\projets\Wolof-NMT\Wolof-NMT
   ```
   (Remplacez par le chemin de votre projet si différent)

3. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

### ⏱️ Combien de temps ça prend ?

Cela peut prendre **5 à 15 minutes** la première fois, car il faut télécharger beaucoup de fichiers.

### ✅ Comment savoir si ça a marché ?

Si vous voyez à la fin quelque chose comme :
```
Successfully installed torch-2.x.x transformers-4.x.x ...
```

C'est bon ! ✅

### ❌ Si vous avez une erreur :

**Erreur : "pip n'est pas reconnu"**
- Essayez : `python -m pip install -r requirements.txt`
- Ou : `python3 -m pip install -r requirements.txt`

**Erreur : "Permission denied"**
- Sur Windows : Ouvrez PowerShell en tant qu'administrateur
- Sur Mac/Linux : Ajoutez `sudo` au début : `sudo pip install -r requirements.txt`

---

## ✅ Étape 3 : Tester le traducteur (le plus important !)

### Méthode la plus simple : Utiliser le script de test

J'ai créé un script spécialement pour vous ! Il fait tout automatiquement.

**Dans votre terminal, tapez simplement :**

```bash
python test_translator.py
```

### Que va-t-il se passer ?

1. **Première fois :** Le script va télécharger le modèle de traduction (peut prendre 5-10 minutes)
   - Le modèle fait environ 600 Mo, donc il faut une connexion Internet
   - Vous verrez des messages comme "Downloading..." ou "Loading..."

2. **Ensuite :** Le script va tester plusieurs traductions automatiquement :
   - "Bonjour" → en wolof
   - "Comment allez-vous?" → en wolof
   - "Naka nga def?" → en français
   - etc.

3. **Résultat :** Vous verrez les traductions s'afficher !

### 📝 Exemple de ce que vous verrez :

```
============================================================
Test du Traducteur Français-Wolof
============================================================

Modèle utilisé: facebook/nllb-200-distilled-600M
------------------------------------------------------------

Chargement du modèle...
✓ Modèle chargé avec succès!

Tests de traduction:
------------------------------------------------------------

Test 1: Français → Wolof
  Entrée:  Bonjour
  Sortie:  [traduction en wolof]

Test 2: Français → Wolof
  Entrée:  Comment allez-vous?
  Sortie:  [traduction en wolof]

...
```

### ❌ Si ça ne marche pas :

**Erreur : "No module named 'translator'"**
- Vous n'êtes peut-être pas dans le bon dossier
- Vérifiez : `cd` dans le dossier du projet, puis réessayez

**Erreur : "Connection error" ou "Timeout"**
- Vérifiez votre connexion Internet
- Le téléchargement du modèle nécessite Internet

**Erreur : "CUDA out of memory"**
- C'est normal si vous n'avez pas de carte graphique puissante
- Le script utilisera automatiquement le processeur (CPU) à la place
- C'est plus lent mais ça fonctionne !

---

## 🎮 Étape 4 : Utiliser le traducteur dans votre propre code

Maintenant que vous savez que ça marche, vous pouvez l'utiliser dans vos propres scripts !

### Créez un nouveau fichier : `mon_test.py`

```python
# Importez le traducteur
from translator import FrenchWolofTranslator

# Créez un traducteur
translator = FrenchWolofTranslator(
    model_checkpoint="facebook/nllb-200-distilled-600M"
)

# Traduisez du français vers le wolof
texte_francais = "Bonjour, comment allez-vous?"
traduction_wolof = translator.translate_french_to_wolof(texte_francais)
print(f"Français : {texte_francais}")
print(f"Wolof : {traduction_wolof}")

# Traduisez du wolof vers le français
texte_wolof = "Naka nga def?"
traduction_francais = translator.translate_wolof_to_french(texte_wolof)
print(f"\nWolof : {texte_wolof}")
print(f"Français : {traduction_francais}")
```

### Exécutez votre script :

```bash
python mon_test.py
```

---

## 🔧 Configuration (optionnel)

### Qu'est-ce qu'un fichier .env ?

C'est un fichier qui contient des **paramètres** pour votre projet. Vous pouvez le créer si vous voulez personnaliser le comportement.

### Dois-je le créer ?

**Non, ce n'est pas obligatoire !** Le projet fonctionne sans.

Mais si vous voulez utiliser un modèle différent ou changer des paramètres, vous pouvez créer un fichier `.env`.

### Comment créer le fichier .env ?

1. **Créez un nouveau fichier** nommé `.env` dans le dossier du projet
2. **Ajoutez ce contenu** :

```bash
MODEL_CHECKPOINT=facebook/nllb-200-distilled-600M
DATASET_NAME=galsenai/french-wolof-translation
```

C'est tout ! Le projet utilisera ces valeurs automatiquement.

---

## 📚 Glossaire (pour comprendre les termes)

- **Modèle** : C'est le "cerveau" du traducteur. Il a été entraîné sur des millions de phrases pour apprendre à traduire.
- **Checkpoint** : C'est l'emplacement où se trouve le modèle (sur Internet ou sur votre ordinateur).
- **HuggingFace** : C'est un site web qui héberge des modèles d'intelligence artificielle (comme GitHub pour le code).
- **NLLB** : "No Language Left Behind" - C'est le nom du modèle créé par Facebook/Meta pour traduire entre beaucoup de langues.
- **Token** : C'est une clé secrète pour accéder à certains services (comme un mot de passe).
- **BLEU Score** : C'est une note qui mesure la qualité d'une traduction (plus c'est haut, mieux c'est).

---

## ❓ Questions Fréquentes

### Q : Est-ce que j'ai besoin d'une carte graphique (GPU) ?

**R : Non !** Le traducteur fonctionne aussi sur le processeur (CPU), c'est juste un peu plus lent.

### Q : Combien d'espace disque faut-il ?

**R :** Environ **2-3 Go** pour :
- Les dépendances Python (~1 Go)
- Le modèle de traduction (~600 Mo)
- Les données d'entraînement (si vous entraînez un modèle)

### Q : Est-ce que je peux utiliser ce projet sans Internet ?

**R :** 
- **Première fois :** Non, il faut Internet pour télécharger le modèle
- **Après :** Oui ! Une fois téléchargé, le modèle est stocké sur votre ordinateur

### Q : Le traducteur est-il gratuit ?

**R :** Oui, complètement gratuit ! Le modèle utilisé est open-source.

### Q : Puis-je améliorer les traductions ?

**R :** Oui ! Vous pouvez entraîner le modèle avec vos propres données. Voir la section "Entraînement" dans le README.md (mais c'est plus avancé).

---

## 🆘 Besoin d'aide ?

Si vous êtes bloqué :

1. **Vérifiez les erreurs** : Lisez attentivement les messages d'erreur
2. **Vérifiez votre installation** : `python --version` et `pip list`
3. **Vérifiez Internet** : Le téléchargement nécessite une connexion
4. **Consultez le README.md** : Il contient plus de détails techniques

---

## 🎉 Félicitations !

Si vous êtes arrivé jusqu'ici et que le script de test fonctionne, vous avez réussi ! 🎊

Vous pouvez maintenant :
- ✅ Utiliser le traducteur dans vos projets
- ✅ Comprendre comment il fonctionne
- ✅ Personnaliser les paramètres si besoin

**Prochaine étape suggérée :** Essayez de traduire vos propres phrases !

---

## 📝 Résumé des commandes essentielles

```bash
# 1. Vérifier Python
python --version

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Tester le traducteur
python test_translator.py

# 4. Utiliser le script principal
python main.py
```

**C'est tout ce dont vous avez besoin pour commencer !** 🚀

