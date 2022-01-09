# usage : ./test.sh repertoire_ou_sont_les_instances repertoire_ou_on_veut_stocker_les_resultats modele

echo Campagne experimentale: arbre enraciné de profit maximum avec des contraintes de capacité
echo Repertoire de données: $1
echo Repertoire de sortie: $2
echo Modèle: $3

mkdir -p $2 # crée le répertoire de sortie s'il n'existe pas encore
echo `date` > $2/date.txt

for instance in `ls $1` ; do  # pour chaque instance dans le repertoire $1
    echo Résolution de l\'instance $instance
    python3 $3.py $1/$instance $2 >> $2/log_${instance}.txt   # écriture de la sortie console dans un fichier log
done
grep Bilan $2/*.sol >> $2/bilan.csv  # les lignes contenant le mot "Bilan" seront concaténées dans le fichier bilan.csv
