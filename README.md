# Openclassrooms : DA Python : P8

## Contexte

Ce repo contient l'ensemble du code réalisé pour le projet 8 du parcours DA Python d'Openclassrooms. L'objectif du projet est de créer un site web pour la société PurBeurre, répondant à un cahier des charges très précis.

## Présentation

### Organisation

Le projet Django PurBeurre contient diverses applications afin de mener les actions requises. Ces applications sont :

-   **purebeurre**  : l'application centrale
-   **favorites**  : l'application permettant la sauvegarde des favoris préférés
-   **search**  : l'application permettant de rechercher et renvoyer les produits de la db
-   **products**  : l'application de gestion des produits dans la db
-   **openfoodfacts**  : l'application qui utilise l'API d'openfoodfacts incluant un sous-dossier avec une commande permettant l'alimentation de la base de données
-   **User**  : l'application se chargeant de la gestion des comptes utilisateurs

Chaque application est testé et un rapport de coverage est disponible dans le dossier "coverage_html" 

### Déploiement

La définition des variables d'environnement suivantes est requise pour permettre le bon déploiement du projet :

-   `db_user`  : le nom de l'utilisateur pour la base de données
-   `db_pass`  : le mot de passe pour l'utilisateur

La base de données attendue est une base PostgreSQL nommée  `purbeurre`.

Le déploiement sur heroku est facilité grâce à la présence du fichier  `Procfile`  requis ainsi que de l'emploi du  _package_  `django-heroku`. Il est néanmoins nécessaire de définir la variable d'environnement  `HEROKU`  à 1 afin de permettre le déploiement effectif sur la plateforme.

### Application en ligne
L'application en ligne peut être utilisé ici : https://purebeurreprojet8.herokuapp.com/