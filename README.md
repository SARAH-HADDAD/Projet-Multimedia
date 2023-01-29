## Description

Ce code permet de détecter les changements dans les frames d'une vidéo en utilisant une technique de comparaison de blocs. Il utilise une méthode de recherche dichotomique pour optimiser les performances.

Le code divisera la frame en blocs de la taille définie, puis recherchera dans un voisinage de taille kxk le bloc similaire et calculera le résidu. Les blocs similaires seront encadrés d'un carré de la couleur définie, et l'image des résidus sera affichée. Si un bloc n'a pas changé, il sera affiché comme un rectangle noir.

La recherche dichotomique est utilisée pour optimiser les performances de la détection des changements. Un document de référence est également fourni pour une consultation supplémentaire.