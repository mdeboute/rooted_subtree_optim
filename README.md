# Comment exécuter les programmes (sans les jupyter notebooks) ?

## Exécution sur une seule instance

Comme nous devons passer des arguments à notre programme, nous allons devoir exécuter le programme en ligne de commande (contrairement au notebook). Pour cela, on ouvre un terminal et on se place dans le répertoire du projet.

Une fois après avoir pris le soin de vérifier que les librairies (*cf* le fichier de dépendances `pyproject.toml`) dont nous avons besoin sont installées sur la machine ou un environnement virtuel (*cf* [virtualenv](https://virtualenv.pypa.io/en/latest/) ou [poetry](https://python-poetry.org)), on peut exécuter notre programme avec la ligne de commande suivante :
`python3 model_1.py Instances/btk_1-Reichstett_0_0.dat Solutions_model_1`

Dans le répertoire `Solutions_model_1` un fichier est créé ayant pour nom, le nom du fichier instance et avec comme extension `.sol`. Ce fichier contient les résultats obtenus avec le programme.

## Exécution sur toutes les instances d'un répertoire

Afin d'exécuter automatiquement le programme sur toutes les instances d'un répertoire, il faut exécuter le script `shell` qui va automatiser le lancement des commandes.

Pour exécuter le script, il faut lancer les commandes\
`chmod +x test.sh` \ afin de donner les droits d'exécution au script \ `./test.sh Instances Solutions_model_1 model_1` \ ou `./test.sh Instances Solutions_model_2 model_2` \

Le premier argument de la dernière commande correspond au répertoire où se trouvent les instances, tandis que le second est le répertoire où seront enregistrés les résultats et le dernier le modèle utilisé pour résoudre les instances.

### Crédits
- Martin Debouté
- Basile Blayac
