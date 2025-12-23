"""
Script ultra-simple pour débuter avec le traducteur français-wolof.
Parfait pour les personnes qui découvrent le projet !
"""
import sys

def verifier_installation():
    """Vérifie que tout est bien installé."""
    print("🔍 Vérification de l'installation...")
    
    try:
        import torch
        print("  ✓ PyTorch installé")
    except ImportError:
        print("  ✗ PyTorch non installé")
        print("    → Installez avec: pip install torch")
        return False
    
    try:
        import transformers
        print("  ✓ Transformers installé")
    except ImportError:
        print("  ✗ Transformers non installé")
        print("    → Installez avec: pip install transformers")
        return False
    
    try:
        from translator import FrenchWolofTranslator
        print("  ✓ Module translator trouvé")
    except ImportError:
        print("  ✗ Module translator non trouvé")
        print("    → Assurez-vous d'être dans le dossier du projet")
        return False
    
    print("\n✅ Tout semble correct !\n")
    return True

def test_simple():
    """Test très simple du traducteur."""
    print("=" * 70)
    print("  🎯 TEST SIMPLE DU TRADUCTEUR FRANÇAIS-WOLOF")
    print("=" * 70)
    print("\n📝 Ce script va :")
    print("   1. Télécharger le modèle (première fois seulement, ~600 Mo)")
    print("   2. Tester une traduction simple")
    print("   3. Vous montrer le résultat")
    print("\n⏱️  Temps estimé : 5-10 minutes la première fois")
    print("   (le modèle sera sauvegardé sur votre ordinateur ensuite)\n")
    print("-" * 70)
    
    reponse = input("Voulez-vous continuer ? (o/n) : ").strip().lower()
    if reponse not in ['o', 'oui', 'y', 'yes']:
        print("\n❌ Annulé. Relancez le script quand vous serez prêt !")
        return
    
    print("\n🚀 Démarrage...\n")
    
    try:
        from translator import FrenchWolofTranslator
        from env_config import EnvConfig
        
        # Récupérer le modèle
        model_checkpoint = EnvConfig.MODEL_CHECKPOINT()
        print(f"📦 Modèle utilisé : {model_checkpoint}\n")
        
        # Charger le traducteur
        print("⏳ Chargement du modèle...")
        print("   (Cela peut prendre quelques minutes la première fois)\n")
        
        translator = FrenchWolofTranslator(model_checkpoint=model_checkpoint)
        print("✅ Modèle chargé avec succès !\n")
        
        # Test simple
        print("=" * 70)
        print("  📝 TEST DE TRADUCTION")
        print("=" * 70)
        
        # Test 1 : Français vers Wolof
        texte_fr = "Bonjour"
        print(f"\n🇫🇷 Français : {texte_fr}")
        print("   Traduction en cours...")
        traduction_wo = translator.translate_french_to_wolof(texte_fr)
        print(f"🇸🇳 Wolof : {traduction_wo}")
        
        # Test 2 : Wolof vers Français
        texte_wo = "Naka nga def?"
        print(f"\n🇸🇳 Wolof : {texte_wo}")
        print("   Traduction en cours...")
        traduction_fr = translator.translate_wolof_to_french(texte_wo)
        print(f"🇫🇷 Français : {traduction_fr}")
        
        # Résultat
        print("\n" + "=" * 70)
        print("  ✅ SUCCÈS ! Le traducteur fonctionne correctement !")
        print("=" * 70)
        print("\n🎉 Félicitations ! Vous pouvez maintenant utiliser le traducteur.")
        print("\n📚 Prochaines étapes :")
        print("   • Consultez GUIDE_DEBUTANT.md pour plus d'informations")
        print("   • Essayez : python test_translator.py pour plus de tests")
        print("   • Créez vos propres scripts de traduction !\n")
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("  ❌ ERREUR")
        print("=" * 70)
        print(f"\nErreur : {e}\n")
        print("🔧 Solutions :")
        print("   1. Vérifiez votre connexion Internet")
        print("   2. Assurez-vous d'avoir installé les dépendances :")
        print("      → pip install -r requirements.txt")
        print("   3. Consultez GUIDE_DEBUTANT.md pour plus d'aide")
        print("   4. Vérifiez que vous êtes dans le bon dossier du projet\n")

def main():
    """Fonction principale."""
    print("\n" + "=" * 70)
    print("  🎓 GUIDE DE DÉMARRAGE - TRADUCTEUR FRANÇAIS-WOLOF")
    print("=" * 70)
    print("\nBienvenue ! Ce script va vous aider à démarrer.\n")
    
    # Vérifier l'installation
    if not verifier_installation():
        print("\n❌ Veuillez installer les dépendances manquantes avant de continuer.")
        print("   Commande : pip install -r requirements.txt\n")
        sys.exit(1)
    
    # Proposer le test
    print("=" * 70)
    print("  🧪 PRÊT POUR LE TEST ?")
    print("=" * 70)
    print("\nVoulez-vous tester le traducteur maintenant ?")
    print("(Le modèle sera téléchargé automatiquement si nécessaire)\n")
    
    test_simple()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrompu par l'utilisateur. Au revoir !\n")
        sys.exit(0)

