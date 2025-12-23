"""
Script de test simple pour le traducteur français-wolof.
Utilisez ce script pour tester rapidement le fonctionnement du traducteur.
"""
from translator import FrenchWolofTranslator
from env_config import EnvConfig

def test_translator():
    """Teste le traducteur avec quelques exemples."""
    print("=" * 60)
    print("Test du Traducteur Français-Wolof")
    print("=" * 60)
    print("\n💡 Astuce : Ce script va télécharger le modèle la première fois.")
    print("   Cela peut prendre 5-10 minutes selon votre connexion Internet.")
    print("   Le modèle fait environ 600 Mo.\n")
    
    # Récupérer le checkpoint depuis les variables d'environnement ou utiliser le défaut
    model_checkpoint = EnvConfig.MODEL_CHECKPOINT()
    print(f"Modèle utilisé: {model_checkpoint}")
    print("-" * 60)
    
    try:
        # Initialiser le traducteur
        print("\nChargement du modèle...")
        translator = FrenchWolofTranslator(model_checkpoint=model_checkpoint)
        print("✓ Modèle chargé avec succès!\n")
        
        # Tests de traduction
        test_cases = [
            {
                "direction": "Français → Wolof",
                "text": "Bonjour",
                "method": translator.translate_french_to_wolof
            },
            {
                "direction": "Français → Wolof",
                "text": "Comment allez-vous?",
                "method": translator.translate_french_to_wolof
            },
            {
                "direction": "Wolof → Français",
                "text": "Naka nga def?",
                "method": translator.translate_wolof_to_french
            },
            {
                "direction": "Wolof → Français",
                "text": "Jamm rekk",
                "method": translator.translate_wolof_to_french
            },
        ]
        
        print("Tests de traduction:")
        print("-" * 60)
        
        for i, test in enumerate(test_cases, 1):
            try:
                translation = test["method"](test["text"])
                print(f"\nTest {i}: {test['direction']}")
                print(f"  Entrée:  {test['text']}")
                print(f"  Sortie:  {translation}")
            except Exception as e:
                print(f"\n✗ Erreur lors du test {i}: {e}")
        
        # Test avec la méthode générique
        print("\n" + "-" * 60)
        print("Test avec méthode générique:")
        print("-" * 60)
        
        generic_tests = [
            ("Bonjour, comment ça va?", "fr"),
            ("Naka nga def?", "wo"),
        ]
        
        for text, source_lang in generic_tests:
            try:
                result = translator.translate(text, source_lang=source_lang)
                lang_name = "Français" if source_lang == "fr" else "Wolof"
                print(f"\n  {lang_name}: {text}")
                print(f"  Traduction: {result}")
            except Exception as e:
                print(f"\n✗ Erreur: {e}")
        
        print("\n" + "=" * 60)
        print("✓ Tous les tests sont terminés!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Erreur lors de l'initialisation: {e}")
        print("\n🔧 Solutions possibles:")
        print("  1. Vérifiez que les dépendances sont installées:")
        print("     → pip install -r requirements.txt")
        print("\n  2. Vérifiez votre connexion Internet")
        print("     → Le modèle doit être téléchargé depuis Internet")
        print("\n  3. Vérifiez que vous êtes dans le bon dossier")
        print("     → cd dans le dossier du projet")
        print("\n  4. Si l'erreur persiste, consultez GUIDE_DEBUTANT.md")
        print("     → Ce guide explique tout en détail pour les débutants")
        return False
    
    return True

if __name__ == "__main__":
    test_translator()

