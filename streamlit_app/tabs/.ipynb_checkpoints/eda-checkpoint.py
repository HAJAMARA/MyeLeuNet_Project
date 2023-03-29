import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px

# Import custom utilities scripts
import sys
sys.path.append("..")
import bcc_utilities as bcc


title = "Exploration des données"
sidebar_name = "Exploration des données"


def run():

    df = pd.read_csv('../data/BCC_dataset_final.csv', index_col = 0)
    df.head()

    st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        ## 1. Sources de données

        Pour ce projet, nous nous sommes intéressés au développement récent 
        d’une technique de DeepLearning pour l’identification des lames, 
        publiée dans deux articles de recherche 
        ([Acevedo et al., 2019](https://www.sciencedirect.com/science/article/abs/pii/S0169260719303578?via%3Dihub); 
        [Boldú et al., 2021](https://www.sciencedirect.com/science/article/abs/pii/S0169260721000742?via%3Dihub)). 
        Nous avons utilisé le 
        [dataset](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7182702/) 
        fourni dans la première publication 
        ([Acevedo et al., 2019](https://www.sciencedirect.com/science/article/abs/pii/S0169260719303578?via%3Dihub)), 
        et y avons joints un second dataset obtenu sur le site 
        [Kaggle](https://www.kaggle.com/datasets/eugeneshenderov/acute-promyelocytic-leukemia-apl). 

        Bien que l’origine de ce dataset nous soit inconnue, il comporte une 
        grande quantité de photos de frottis sanguins d’excellente qualité, 
        pour des patients souffrant d’AML ou d’APL. 
        
        A ces deux datasets, nous avons décidé d’ajouter deux jeux de données 
        supplémentaires. Le premier publié sur le site 
        [Cancer Imaging Archive](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=61080958#61080958168cfd58d3c042fcbec1277728bd03e1) 
        et issus de la publication 
        [Matek, C. et al., 2019](https://www.nature.com/articles/s42256-019-0101-9).
        
        Le second publié en libre accès sur le site de preprint 
        scientifique Biorxiv et issus de la publication par 
        [Mousavi Kouzehkanan et al., 2021](https://www.biorxiv.org/content/10.1101/2021.05.02.442287v4). Nous 
        avons choisi de n'utiliser que 
        [les images de patient sains](https://raabindata.com/free-data/#double-labeled-cropped-cells).

        Nomenclature des datasets :  
            Dataset A : [Données de (Acevedo et al., 2019), patients sains]()  
            Dataset B : [Données Kaggle, patients malades AML et APL]()  
            Dataset C : [Munich](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=61080958#61080958168cfd58d3c042fcbec1277728bd03e1)  
            Dataset D : [Raabin, patients sains uniquement](https://raabindata.com/free-data/#double-labeled-cropped-cells)
        
        Le regroupement de ces différents dataset nous a permis de constitué 
        une base d'image d'un peu moins de 80000 clichés de frottis sanguins.
        """
    )

    st.markdown(
        """
        ## 2. Re-catégorisation des types cellulaires

        En parcourant nos jeux de données, nous avons constaté une disparité 
        dans la quantité de classes cellulaires observées (5 pour Raabin, 8 
        pour Barcelone, 15 pour Munich et 20 pour Kaggle). Ceci s’explique par 
        une différence de choix de catégorisation entre les auteurs. Dans un 
        souci de cohérence et de simplicité pour la mise en place du modèle, 
        nous avons donc décidé d’opérer une recatégorisation des classes, en 
        regroupant ensemble les types cellulaires ayant une origine ou une 
        fonction proche. Se retrouvent ainsi groupés les neutrophiles en bande 
        et segmentés dans la même catégorie « neutrophile », les thrombocytes, 
        agrégats de thrombocytes et plaquettes dans la même catégorie 
        « platelet », etc. Nous passons ainsi de 47 classes initiales à 15. 
        """
    )

    st.markdown(
        """
        ## 3. Analyse exploratoire des données

        ### 3.1. Distribution des classes

        Notre première étape a été de vérifier la distribution brute des 
        classes.
        """
    )

    cells_count = df[['source', 'blood_cell']].value_counts()
    cells_count = cells_count.rename_axis(['source', 'blood_cell']).reset_index(name='counts')
    
    fig_bar = px.bar(
        cells_count, 
        x = 'blood_cell',
        y = 'counts',
        color = 'source',
    )
    fig_bar.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    
    fig_bar.update_traces(
        hovertemplate = '%{x}: %{y}'
    )

    fig_bar.update_layout(
        xaxis_title = 'Cellule sanguine',
        yaxis_title = 'Nombre d\'images',
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption('Figure 1 : Distribution des images par catégorie')

    st.markdown(
        """
        Il est apparût qu'une proportion significative des images n'étaient 
        pas labelisées (*unsigned*). De plus, certaines catégories englobaient 
        trop de type de cellules (*artifact*, *unknown_precursor*) pour être 
        exploitables. Nous avons donc écartées environs 15000 images de la 
        base.
        
        Ce qui nous à laisser avec un peu moins de 65000 images labélisées, 
        avec la distribution ci-dessous :
        """
    )

    cell_cat_to_remove = ['UNS', 'UNP']
    labeled_df = df[~df['blood_cell'].isin(cell_cat_to_remove)]
    labeled_df['blood_cell'] = labeled_df['blood_cell'].replace(['IG', 'MMC', 'MYC', 'PYC'], 'IG')
    
    cells_count = labeled_df[['source', 'blood_cell']].value_counts()
    cells_count = cells_count.rename_axis(['source', 'blood_cell']).reset_index(name='counts')

    fig_bar = px.bar(
        cells_count, 
        x = 'blood_cell',
        y = 'counts',
        color = 'source',
    )
    fig_bar.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

    fig_bar.update_traces(
        hovertemplate = '%{x}: %{y}'
    )

    fig_bar.update_layout(
        xaxis_title = 'Cellule sanguine',
        yaxis_title = 'Nombre d\'images',
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption('Figure 2 : Distribution après tri')

    st.markdown(
        """
        La première observation est que les différentes classes sont très 
        déséquilibrées. Certaines ne sont même quasiment pas représentées 
        (*myélocytes* et *métamyélocytes*). Ce qui est confirmé par le tableau 
        ci-dessous.
        """
    )

    # Create a pivoted DataFrame with a total row and a total column
    pivot_cells_count = cells_count.pivot(index='blood_cell', columns='source', values='counts')
    pivot_cells_count['Total'] = pivot_cells_count.apply(lambda r: r.sum(), axis=1)
    total_row = pd.DataFrame({col: pivot_cells_count[col].sum() for col in pivot_cells_count.columns}, index=['Total'])
    pivot_cells_count = pd.concat([pivot_cells_count, total_row], axis=0)

    st.dataframe(pivot_cells_count, use_container_width=True, height=493)
    st.caption('Tableau 1 : Répartition des images par cellule sanguine et par source')

    st.markdown(
        """
        ### 3.2. Distribution cellulaire chez les patients sains et les patients atteins d'AML

        Après recatégorisation, nous avons étudié la distribution des classes 
        dans les jeux de données, en regroupant les patients par catégorie 
        (sain ou malade AML /APL). Pour cette première analyse, nous avons 
        exclu le jeu de donnée de Munich pour lequel l’information de 
        diagnostique fait défaut. 
        """
    )

    total, healthy, ill = st.tabs(['Tous les patients', 'Patients sains', 'Patients atteins d\'AML'])
    with total:
        # Bar chart of the total dataset
        sub_cells_count = cells_count

        total_cells = cells_count['counts'].sum()
        sub_cells_count = sub_cells_count.sort_values(by=['counts'], ascending=False)
        sub_cells_count['counts'] = sub_cells_count['counts'].apply(lambda c: c/total_cells)

        fig_bar = px.bar(
            sub_cells_count, 
            x = 'blood_cell',
            y = 'counts',
            color = 'source',
        )
        fig_bar.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        fig_bar.update_traces(
            hovertemplate = '%{x}: %{y:.01%}',
        )

        fig_bar.update_layout(
            yaxis_tickformat = '.0%',
            xaxis_title = 'Cellule sanguine',
            yaxis_title = 'Nombre d\'images',
        )
        fig_bar.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with healthy:
        # Bar chart of healthy patients
        sub_cells_count = cells_count[(cells_count['source'] == 'Barcelona') | (cells_count['source'] == 'Raabin')]

        total_cells = sub_cells_count['counts'].sum()
        sub_cells_count = sub_cells_count.sort_values(by=['counts'], ascending=False)
        sub_cells_count['counts'] = sub_cells_count['counts'].apply(lambda c: c/total_cells)

        fig_bar = px.bar(
            sub_cells_count, 
            x = 'blood_cell',
            y = 'counts',
            color = 'source'
        )
        fig_bar.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        
        fig_bar.update_traces(
            hovertemplate = '%{x}: %{y:.01%}',
        )

        fig_bar.update_layout(
            yaxis_tickformat = '.0%',
            xaxis_title = 'Cellule sanguine',
            yaxis_title = 'Nombre d\'images',
        )
        fig_bar.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with ill:
        # Bar chart of ill patients
        sub_cells_count = cells_count[cells_count['source'] == 'Kaggle']

        total_cells = sub_cells_count['counts'].sum()
        sub_cells_count = sub_cells_count.sort_values(by=['counts'], ascending=False)
        sub_cells_count['counts'] = sub_cells_count['counts'].apply(lambda c: c/total_cells)

        fig_bar = px.bar(
            sub_cells_count, 
            x = 'blood_cell',
            y = 'counts',
            color = 'source'
        )
        fig_bar.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        fig_bar.update_traces(
            hovertemplate = '%{x}: %{y:.01%}',
        )

        fig_bar.update_layout(
            yaxis_tickformat = '.0%',
            xaxis_title = 'Cellule sanguine',
            yaxis_title = 'Nombre d\'images',
        )
        fig_bar.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    st.caption('Figure 3 : Distribution par cellule, source et typologie de patient')

    st.markdown(
        """
        TODO : vérifier les résultats obtenus pour les patient sains.
        
        Chez les patients sains (Barcelone et Raabin), 
        nous constatons que les *neutrophiles* représentent le type cellulaire 
        majoritaire avec ~ 42% des photos, suivi par les *éosinophiles* (14%) et 
        les *granulocytes immatures* (12,4%). 

        Chez les patients atteints de leucémie (dataset Kaggle), le premier 
        constat est l’effondrement de la population de granulocytes 
        (*neutrophiles*, *éosinophiles* et *basophiles*). Une diminution de la 
        quantité de *plaquettes* et d’*érythrocytes* (globules rouges) est 
        également observée. Parallèlement, nous constatons l’apparition d’une 
        classe, les *myéloblastes* (entre 20 et 26%), occupant la 2e fraction 
        après les *lymphocytes*. Il est important de noter que ce type 
        cellulaire, ainsi que les types minoritaires *myélocytes*, 
        *promyélocytes* et *métamyélocytes*, peuvent tous être considérés 
        comme appartenant à la famille des 'granulocytes immatures'. Dans le 
        dataset de Barcelone, cette distinction n’a pas été faite, et les 4 
        classes sont regroupées  en une seule. En prenant en compte cette 
        classification, nous pouvons constater que la quantité de 
        *granulocytes immatures* est doublée chez les patients malades du 
        dataset Kaggle en comparaison aux patients sains des datasets 
        Barcelone et Raabin.
        """
    )

    st.markdown(
        """
        ### 3.4. Analyse des images

        #### 3.4.1. Outliers suivant la Luminance & la Brightness
        
        """
         )
    luminance, brightness = st.tabs(['Luminance outliers', 'Brightness outliers'])
    
    with luminance: 
        luminance_box, luminance_img = st.tabs(['Luminance box-plots', 'Outliers examples'])
        with luminance_box: 
            st.image(
              Image.open("assets/Luminance_boxplots.png"),
              caption = "Figure 3-1 : Luminances Box-plots"
            )
        with luminance_img: 
            st.image(
              Image.open("assets/Outliers_Luminance.png"),
              caption = "Figure 3-2 : Luminance outliers examples"
            )
    with brightness: 
        brightness_box, brightness_img = st.tabs(['Brightness box-plots', 'Outliers examples'])
        with brightness_box: 
            st.image(
              Image.open("assets/Brightness_boxplots.png"),
              caption = "Figure 4-1 : Brightnesses Box-plots"
            )
        with brightness_img: 
            st.image(
              Image.open("assets/Outliers_Brightness.png"),
              caption = "Figure 4-2 : Brightness outliers examples"
            )
        
        
    st.markdown(
        """
        #### 3.4.2. Colorimétrie moyenne par type de cellule sanguine
        """
        
    )
    
    


    st.markdown(
        """
        #### 3.4.4. Analyse de la position des cellules dans les images
        TODO
        """
    )
