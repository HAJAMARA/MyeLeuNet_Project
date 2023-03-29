import streamlit as st
from PIL import Image


title = "Blood cells classification"
sidebar_name = "Introduction"


def run():

    # TODO: choose between one of these GIFs
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        ## 1. Contexte
        ### 1.1. Types cellulaires du sang périphérique

        Chez l’Homme adulte, le sang périphérique (sang circulant dans 
        l’ensemble du circuit sanguin) contient de nombreux types cellulaires 
        issus pour la majorité de la moëlle osseuse (Kenneth M. Murphy, 2011). 
        Ces types cellulaires peuvent être regroupés en trois catégories : les 
        érythrocytes (Hématies ou globules rouges) dont les fonctions 
        principales sont le transport de l’oxygène, du CO2 et la régulation du 
        pH (Helms et al., 2018), les leucocytes (Globules blancs), qui 
        représentent les cellules effectrices du système immunitaire, et les 
        thrombocytes (Plaquettes sanguines), impliqués dans les processus de 
        coagulation et de cicatrisation (Figure 1). 

        Les érythrocytes et les thrombocytes se distinguent morphologiquement 
        des leucocytes par l’absence de noyau, les premiers suite à un 
        processus d’énucléation, les seconds suite à la fragmentation de leur 
        cellule d’origine, les mégacaryocytes.  Les leucocytes se regroupent 
        quant à eux en 3 sous-catégories : les lymphocytes (cellules B, T et 
        NK), effecteurs de la réponse immunitaire adaptative (réponse 
        longue-durée, mémoire immunitaire), les monocytes, impliqués dans la 
        réponse immunitaire innée (réponse courte durée), et les granulocytes. 
        Parmi les granulocytes, aussi appelés polymorphonucléaires pour la 
        segmentation de leurs noyaux, on retrouve trois catégories : les 
        éosinophiles, les basophiles et les neutrophiles, tous présentant des 
        granules dans leur corps cellulaire (cytoplasme) et effecteurs de la 
        réponse immunitaire antibactérienne et antiparasitaire (Kenneth M. 
        Murphy, 2011) (Figure 1).
        
        En proportion marginales, le sang périphérique peut également contenir 
        d’autre types cellulaires, comme les précurseurs de mastocytes 
        (impliqués dans les processus de réaction allergique), les plasmocytes 
        (lymphocytes différenciés pour la production d’anticorps suite à une 
        infection) et les cellules dendritiques (impliquées dans la détection 
        d’antigènes étrangers) (Robinson et al., 1999). 
        
        Chez les adultes sains, les proportions moyennes des leucocytes sont 
        les suivantes :  60 à 70% de neutrophiles, 20 à 25% de lymphocytes, 
        3 à 8% de monocytes, 2 à 4% d’éosinophiles et 0.5 à 4% de basophiles 
        (Xie, 2015). Il est important de noter que ces pourcentages peuvent 
        grandement varier d’un individu et d’une population à l’autre, selon 
        le fond génétique, l’environnement, et les pathogènes auxquels les 
        patients ont pu être exposés. Les érythrocytes et les thrombocytes 
        (plaquettes) représentent quant à eux l’écrasante majorité du volume 
        sanguin, jusqu’à 98%, dans un ratio de 20  pour 1 (Stiff, 1990).
        """
    )

    st.image(
      Image.open("assets/composants_sang_peripherique.jpg"),
      caption = "Figure 1 : Cellules unicellulaires présentes dans le sang " + 
        "périphérique"
    )

    st.markdown(
      """
      ### 1.2. Leucémies Myéloïdes et Pro-myéloïdes Aiguës

      La leucémie myéloïde aiguë (Acute Myeloïd Leukemia, AML) est un type de 
      cancer touchant les cellules précurseures (aussi appelés progéniteurs) 
      de la lignée myéloïde à l’origine des érythrocytes, thrombocytes, 
      granulocytes et monocytes (De Kouchkovsky and Abdul-Hay, 2016). Chez les 
      patients atteints d’AML, des mutations entravent la différenciation de 
      ces progéniteurs, causant leur sur-prolifération et leur échappement 
      hors de leur niche naturelle, la moëlle osseuse, dans le sang 
      périphérique. Parallèlement, le défaut de différenciation des 
      progéniteurs cause un déficit dans le sang de leurs lignées filles 
      (érythrocytes, plaquettes et granulocytes notamment)(Pelcovits and 
      Niroula, 2020).

      L’AML est une famille de cancers recouvrant une importante diversité de 
      mutations et de progéniteurs touchés. Les myéloblastes et les myélocytes 
      représentent l’une des classes de progéniteurs les plus représentés. Les 
      promyélocytes peuvent également être atteints. On parle alors de 
      Leucémie Pro-myéloïde Aiguë (Acute Pro-myelocytic Leukemia, APL) 
      (Jimenez et al., 2020) (Figure 2). 
      """
    )

    st.image(
      Image.open("assets/progeniteurs_hematopoietiques_aml_apl.jpg"),
      caption = "Figure 2 : Illustration simplifiée des progéniteurs " + 
        "hématopoïétiques touchés dans l'AML et l'APL"
      )

    st.markdown(
      """
      ### 1.3. Diagnostic des leucémies

      Le diagnostic d’une leucémie passe par plusieurs étapes successives, et 
      implique presque toujours en premier lieu des prises de sang et le 
      comptage des différents types de cellules du sang périphérique sous 
      microscope. Pour ce faire, on utilise la méthode des frottis sanguins : 
      le sang est mélangé à un colorant ayant une forte affinité pour les 
      noyaux cellulaires, puis une goutte est placée entre lame et lamelle. 
      Chaque échantillon ainsi produit doit être analysé et compté 
      manuellement par les professionnels de santé.

      En dépit de son caractère extrêmement chronophage et répétitif, cette 
      méthode n’a pour le moment que très peu d’alternatives. En outre, 
      l’identification des cellules est soumise à différents biais : certains 
      types cellulaires sont morphologiquement très proches, ou présentent peu 
      de signes distinctifs, l’orientation et le positionnement sur la lame 
      d’une cellule peuvent influencer la décision de l’expérimentateur …  
      
      **Une méthode de traitement automatique et fiable** de cette tâche 
      est donc hautement souhaitable pour un diagnostic rapide des leucémies 
      au sens large. 
      """
    )

    st.markdown(
      """
      ## 2. Objectifs

      L’objectif de ce projet est d’identifier les différents types de 
      cellules du sang à l’aide d'algorithmes de computer vision. La 
      densité et l’abondance relative des cellules du sang dans le frottis 
      est cruciale pour le diagnostic de nombreuses pathologies, comme par 
      exemple pour la leucémie qui repose sur le ratio de lymphocytes. 
      L’identification de leucocytes anormaux dans des pathologies telles que 
      la leucémie pourrait compléter cette première partie.
      
      Développer un outil capable d'analyser les cellules à partir de frottis 
      sanguins pourrait faciliter le diagnostic de certaines pathologies mais 
      aussi être utilisé à but de recherche.
      """
    )
