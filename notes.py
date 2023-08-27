"""
Notes sur fichiers .odt, et Titres

- *.odt <==> *.zip de fichiers spécifiques
- Texte principale dans content.xml
- Les titres PRINCIPAUX :
    <text:p text:style-name="Title">Titre test0.odt</text:p>
    <text:p text:style-name="Heading">Encore un titre, <text:span text:style-name="T1">mais formaté</text:span></text:p>

    Les titres sont gérés de cette manière :
      <text:list xml:id="list3412654903" text:style-name="Outline">
        <text:list-item>
          <text:h text:style-name="Heading_20_1" text:outline-level="1">Un chapitre</text:h>
          <text:list>
            <text:list-item>
              <text:h text:style-name="Heading_20_2" text:outline-level="2">Ceci</text:h>
            </text:list-item>
            <text:list-item>
              <text:h text:style-name="Heading_20_2" text:outline-level="2">Cela</text:h>
            </text:list-item>
          </text:list>
        </text:list-item>
        <text:list-item>
          <text:h text:style-name="Heading_20_1" text:outline-level="1">Un deuxième</text:h>
          <text:list>
            <text:list-item>
              <text:h text:style-name="Heading_20_2" text:outline-level="2">Ça</text:h>
            </text:list-item>
            <text:list-item>
              <text:h text:style-name="Heading_20_2" text:outline-level="2">Et là</text:h>
            </text:list-item>
          </text:list>
        </text:list-item>
        <text:list-item>
          <text:h text:style-name="Heading_20_1" text:outline-level="1">Le troisième</text:h>
          <text:list>
            <text:list-item>
              <text:h text:style-name="Heading_20_2" text:outline-level="2">Là-bas</text:h>
            </text:list-item>
            <text:list-item>
              <text:h text:style-name="Heading_20_2" text:outline-level="2">là-haut</text:h>
            </text:list-item>
          </text:list>
        </text:list-item>
      </text:list>

"""
