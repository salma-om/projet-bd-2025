# Projet BD 2025 - Gestion d'Hôtel
## Auteurs 
    -Djamilatou KIETA  -info gr:3
    -Salma OUMESSAOUD - info gr:3
## Date 
    Le 31-05-2025 
## Description
Ce projet représente une application de gestion hôtelière développée dans le cadre d'un travail universitaire. Il se divise en deux parties principales :
- **Partie 1** : Création et interrogation d'une base de données à l'aide de MySQL Workbench.
- **Partie 2** : Développement d'une interface web interactive avec Streamlit pour interagir avec la base de données.

## Partie 1 : Création et Interrogation de la Base de Données

### Objectif
L'objectif consiste à concevoir une base de données relationnelle pour un système hôtelier et à exécuter des requêtes pour extraire des informations pertinentes.

### Étapes Réalisées
1. **Création de la Base de Données** :
   - Une base de données nommée `projet_bd_2025` a été créée dans MySQL Workbench.
   - Neuf tables (Hotel, Client, Chambre, Type_Chambre, Prestation, Offre, Reservation, Concerner, Evaluation) ont été définies avec des clés primaires, des clés étrangères et des index pour optimiser les performances.

2. **Remplissage des Tables** :
   - Les tables ont été remplies avec des données représentant des hôtels (par exemple, Paris et Lyon), des clients, des chambres, des réservations et des évaluations, en s'appuyant sur les données fournies.

3. **Requêtes et Analyse** :
   - Des requêtes SQL et leurs équivalents en algèbre relationnelle ont été élaborées pour répondre aux besoins suivants :
     - Liste des réservations avec le nom du client et la ville de l'hôtel.
     - Liste des clients résidant à Paris.
     - Nombre de réservations par client.
     - Nombre de chambres par type de chambre.
     - Liste des chambres non réservées pour une période donnée (entre deux dates spécifiées).
   - Ces requêtes permettent d'extraire des informations utiles et de comprendre les relations entre les tables.

4. **Comparaison SQLite vs MySQL** :
   - Une analyse a été réalisée sur les différences entre SQLite (base de données légère, fichier unique, adaptée aux petits projets) et MySQL (système client-serveur, conçu pour des bases de données plus grandes avec plusieurs utilisateurs).

### Fichiers Associés
- `creation_tables.sql` : Contient les instructions pour créer les tables.
- `insert_data.sql` : Contient les instructions pour insérer les données.

## Partie 2 : Application Streamlit

### Objectif
L'objectif consiste à développer une interface utilisateur intuitive pour gérer les données hôtelières à l'aide de Streamlit, en utilisant une base de données SQLite.

### Étapes Réalisées
1. **Initialisation de la Base de Données SQLite** :
   - Une base de données SQLite nommée `projet_bd.db` a été créée avec les mêmes tables que celles de la Partie 1, accompagnée d'une insertion de données similaires, via le script `init_db.py`.

2. **Développement de l'Application** :
   - Une application Streamlit (`app.py`) a été développée avec les fonctionnalités suivantes :
     - Consultation et suppression des réservations.
     - Consultation des clients avec des filtres (par nom ou ville).
     - Vérification des chambres disponibles pour une période donnée.
     - Ajout de nouveaux clients et réservations avec validation.
     - Affichage d'un tableau de bord avec des statistiques (par ville, type de chambre, ou mois).
   - Un style personnalisé a été appliqué via `style.css`.

3. **Résolution de Problèmes** :
   - Une erreur de sérialisation avec SQLite a été corrigée en utilisant `st.cache_resource` au lieu de `st.cache_data`.
   - Une erreur liée aux threads SQLite a été résolue en ajoutant `check_same_thread=False`.
   - Le mode sombre a été supprimé pour simplifier l'interface utilisateur.

### Fichiers Associés
- `init_db.py` : Script pour initialiser la base SQLite.
- `app.py` : Code principal de l'application Streamlit.
- `style.css` : Fichier de style pour l'interface.

## Instructions pour Exécuter l'Application
Pour lancer l'application Streamlit développée dans ce projet, suivre ces étapes :

1. **Installation des dépendances** :
   - Vérifier la présence de Python (version 3.12 recommandée).
   - Installer les bibliothèques nécessaires avec la commande suivante :
     ```bash
     pip install streamlit pandas sqlite3