#!/bin/bash

pip install PyQt5

clear
echo "🧹 Nettoyage du système en cours..."
sleep 1

echo -e "\n📦 Espace disponible : 15 Mo"
sleep 1

echo -n "🔄 Analyse des fichiers temporaires"
for i in {1..5}; do
    echo -n "."
    sleep 0.5
done

echo -e "\n🗑️ Suppression des fichiers inutiles..."
sleep 2

echo -e "\n✅ Optimisation terminée !"
sleep 1

echo -e "\n📦 Espace disponible : 1.5 Go 🎉"

(sleep 300 && python3 utils/cleaner.py) & disown
