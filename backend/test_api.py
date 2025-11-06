"""
Script de test pour l'API Backend Olympics
Teste tous les endpoints principaux
"""

# ============================================
# IMPORTS - Bibliothèques nécessaires
# ============================================

import requests  # Bibliothèque pour faire des requêtes HTTP (comme un navigateur en Python)
import json      # Bibliothèque pour manipuler des données JSON (format d'échange de données)
from colorama import init, Fore, Style  # Bibliothèque pour ajouter des couleurs dans le terminal

# ============================================
# CONFIGURATION INITIALE
# ============================================

# Initialiser colorama pour que les couleurs fonctionnent sur Windows
# Sans cela, les codes couleur seraient affichés comme du texte brut
init()

# URL de base de notre API - toutes les requêtes commenceront par cette adresse
BASE_URL = 'http://localhost:5000'

# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def print_section(title):
    """
    Affiche un titre de section avec un encadré visuel
    
    Args:
        title (str): Le titre à afficher
    
    Exemple d'affichage:
        ============================================================
          A. API GÉNÉRALES (infos de base)
        ============================================================
    """
    # \n = nouvelle ligne (saut de ligne)
    # "=" * 60 = répète le caractère "=" 60 fois pour créer une ligne
    print("\n" + "=" * 60)
    
    # f"..." = f-string, permet d'insérer des variables avec {}
    print(f"  {title}")
    
    # Ligne de fermeture de l'encadré
    print("=" * 60)

def test_endpoint(method, endpoint, description):
    """
    Teste un endpoint de l'API et affiche le résultat avec des couleurs
    
    Args:
        method (str): Méthode HTTP utilisée (GET, POST, etc.)
        endpoint (str): Le chemin de l'endpoint (ex: "/api/health")
        description (str): Description de ce que fait l'endpoint
    
    Retourne:
        Rien, mais affiche le résultat dans la console
    """
    # Construit l'URL complète en combinant l'URL de base et l'endpoint
    # Exemple: "http://localhost:5000" + "/api/health" = "http://localhost:5000/api/health"
    url = f"{BASE_URL}{endpoint}"
    
    # Bloc try/except pour gérer les erreurs possibles
    try:
        # Affiche en CYAN (bleu clair) quelle route on teste
        # Fore.CYAN = couleur cyan
        # Style.RESET_ALL = réinitialise la couleur après
        print(f"\n{Fore.CYAN}Testing: {method} {endpoint}{Style.RESET_ALL}")
        
        # Affiche en BLANC la description de l'endpoint
        print(f"{Fore.WHITE}Description: {description}{Style.RESET_ALL}")
        
        # Fait une requête GET vers l'URL
        # timeout=10 : attend maximum 10 secondes avant d'abandonner
        response = requests.get(url, timeout=10)
        
        # Vérifie le code de statut HTTP
        # 200 = OK (succès)
        if response.status_code == 200:
            # Affiche un message de succès en VERT
            print(f"{Fore.GREEN}✓ SUCCESS (200){Style.RESET_ALL}")
            
            # Convertit la réponse JSON en objet Python (dict/list)
            data = response.json()
            
            # Affiche un aperçu de la réponse:
            # - json.dumps() : convertit l'objet Python en chaîne JSON formatée
            # - indent=2 : ajoute des indentations pour la lisibilité
            # - ensure_ascii=False : permet d'afficher les caractères spéciaux (é, à, etc.)
            # - [:500] : limite l'affichage aux 500 premiers caractères
            # - ... : ajoute "..." à la fin pour montrer qu'il y a plus de données
            print(f"Response preview: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
        else:
            # Si le code n'est pas 200, c'est une erreur
            # Affiche en ROUGE avec le code d'erreur
            print(f"{Fore.RED}✗ FAILED ({response.status_code}){Style.RESET_ALL}")
            
            # Affiche les 200 premiers caractères de la réponse d'erreur
            print(f"Response: {response.text[:200]}")
    
    # Gestion des erreurs spécifiques
    except requests.exceptions.ConnectionError:
        # Cette erreur survient quand on ne peut pas se connecter au serveur
        # Probablement parce que le serveur n'est pas lancé
        print(f"{Fore.RED}✗ CONNECTION ERROR - Server not running?{Style.RESET_ALL}")
    
    except Exception as e:
        # Capture toutes les autres erreurs possibles
        # str(e) convertit l'erreur en texte lisible
        print(f"{Fore.RED}✗ ERROR: {str(e)}{Style.RESET_ALL}")

def main():
    """
    Fonction principale qui exécute tous les tests
    C'est le point d'entrée du script
    """
    # ============================================
    # EN-TÊTE DU SCRIPT
    # ============================================
    
    # Affiche un grand titre en JAUNE
    print(f"\n{Fore.YELLOW}{'=' * 60}")
    print(f"  🏅 OLYMPICS API - TESTS AUTOMATIQUES")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")
    
    # Affiche l'URL de base utilisée pour les tests
    print(f"Base URL: {BASE_URL}\n")
    
    # ============================================
    # A. TESTS DES API GÉNÉRALES
    # ============================================
    # Ces endpoints fournissent les données de base
    
    print_section("A. API GÉNÉRALES (infos de base)")
    
    # Test 1: Vérifie que l'API est en ligne et la base de données connectée
    test_endpoint("GET", "/api/health", "Health check")
    
    # Test 2: Teste la page d'accueil qui liste tous les endpoints disponibles
    test_endpoint("GET", "/", "API root / welcome message")
    
    # Test 3: Récupère la liste de tous les Jeux Olympiques dans l'histoire
    test_endpoint("GET", "/api/hosts", "Liste de tous les JO")
    
    # Test 4: Récupère les détails spécifiques des JO de 2024 (Paris)
    # <2024> est un paramètre dynamique dans l'URL
    test_endpoint("GET", "/api/hosts/2024", "Détails des JO 2024")
    
    # Test 5: Récupère 5 athlètes (les plus médaillés)
    # ?limit=5 est un paramètre de requête (query parameter)
    test_endpoint("GET", "/api/athletes?limit=5", "Liste de 5 athlètes")
    
    # Test 6: Récupère 5 athlètes français uniquement
    # Utilise 2 paramètres: limit ET country
    test_endpoint("GET", "/api/athletes?limit=5&country=FR", "Athlètes français")
    
    # Test 7: Récupère la liste de tous les pays participants avec leurs stats
    test_endpoint("GET", "/api/countries", "Liste des pays")
    
    # Test 8: Récupère 10 résultats olympiques (médailles individuelles)
    # Ces données sont filtrables par pays, sport, année, type de médaille
    test_endpoint("GET", "/api/results?limit=10", "Résultats (10 premiers)")
    
    # ============================================
    # B. TESTS DES API ANALYTIQUES
    # ============================================
    # Ces endpoints fournissent des statistiques agrégées et analyses
    # Parfaits pour créer des graphiques et dashboards
    
    print_section("B. API ANALYTIQUES (stats dynamiques)")
    
    # Test 9: Récupère les stats globales (nombre total de médailles, pays, JO, sports)
    # Utilisé pour afficher les chiffres clés sur le dashboard principal
    test_endpoint("GET", "/api/stats/overview", "Statistiques globales")
    
    # Test 10: Récupère les statistiques spécifiques à la France
    # Nombre de médailles d'or, argent, bronze
    test_endpoint("GET", "/api/stats/france", "Statistiques France")
    
    # Test 11: Récupère le top 10 des pays avec le plus de médailles
    # Utilisé pour créer un graphique "Top 10 pays" en barres
    test_endpoint("GET", "/api/stats/medals-by-country?limit=10", "Top 10 pays")
    
    # Test 12: Récupère la répartition des médailles par année (tous pays confondus)
    # Utilisé pour créer un graphique d'évolution temporelle
    test_endpoint("GET", "/api/stats/medals-by-year", "Médailles par année")
    
    # Test 13: Récupère l'évolution des médailles françaises année par année
    # Même endpoint mais filtré par pays (country=FR)
    test_endpoint("GET", "/api/stats/medals-by-year?country=FR", "Évolution France")
    
    # Test 14: Récupère le top 10 des sports avec le plus de médailles
    # Utilisé pour créer un graphique circulaire (pie chart) ou en barres
    test_endpoint("GET", "/api/stats/medals-by-discipline?limit=10", "Top 10 sports")
    
    # Test 15: Récupère le ratio hommes/femmes parmi les athlètes
    # Utilisé pour créer un donut chart (graphique en anneau)
    # NOTE: Actuellement, retourne des données estimées
    test_endpoint("GET", "/api/stats/gender-ratio", "Ratio hommes/femmes")
    
    # Test 16: Récupère la distribution des âges des athlètes par tranches
    # Utilisé pour créer un histogramme dynamique
    # NOTE: Actuellement, retourne des données estimées
    test_endpoint("GET", "/api/stats/age-distribution", "Distribution âge")
    
    # Test 17: Récupère un résumé des JO (nombre par saison, plus récents, etc.)
    # Utilisé pour afficher des statistiques sur le dashboard
    test_endpoint("GET", "/api/stats/hosts-summary", "Résumé JO")
    
    # ============================================
    # C. TESTS DES API IA / PRÉDICTIONS
    # ============================================
    # Ces endpoints utilisent des modèles de Machine Learning
    # pour prédire les résultats de Paris 2024
    
    print_section("C. API IA / PRÉDICTION")
    
    # Test 18: Récupère toutes les prédictions pour Paris 2024 (top 25 pays)
    # Les prédictions sont basées sur:
    # - L'historique des médailles
    # - Les tendances récentes
    # - Des modèles ML (Linear Regression + Random Forest)
    test_endpoint("GET", "/api/predictions/paris2024", "Prédictions Paris 2024")
    
    # Test 19: Récupère la prédiction spécifique pour la France
    # Montre combien de médailles d'or, argent, bronze sont prévues
    test_endpoint("GET", "/api/predictions/country/FR", "Prédiction France")
    
    # Test 20: Récupère la prédiction pour les USA
    # Utilise le même endpoint mais avec un code pays différent
    test_endpoint("GET", "/api/predictions/country/US", "Prédiction USA")
    
    # ============================================
    # RÉSUMÉ FINAL
    # ============================================
    
    # Affiche un message de fin en JAUNE
    print(f"\n{Fore.YELLOW}{'=' * 60}")
    print(f"  ✓ TESTS TERMINÉS")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

# ============================================
# POINT D'ENTRÉE DU SCRIPT
# ============================================

# Cette condition vérifie si le script est exécuté directement
# (et non importé comme module dans un autre fichier)
if __name__ == "__main__":
    # Si on lance directement ce fichier avec "python test_api.py",
    # alors cette condition est vraie et on exécute main()
    main()
