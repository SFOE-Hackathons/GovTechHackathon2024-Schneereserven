# GovTechHackathon2024-Schneereserven
Wie hoch sind die Schneereserven der Schweizer Stauanlagen?

# Challenge

Neben den Füllständen der Speicherseen sind die Schneemengen über den Speicherseen ein guter Indikator für die verfügbaren Energiereserven und damit für die Versorgungssicherheit. Wir wollen diese Informationen über Daten zugänglich machen und auf dem Energiedashboard publizieren.

### Ressourcen

Für die Challenge verwenden wir:

* [Standorte der Stauanlagen](https://opendata.swiss/de/dataset/stauanlagen-unter-bundesaufsicht)
* [Einzugsgebiete von Gewässern](/data/)
    - https://opendata.swiss/de/dataset/topographische-einzugsgebiete-der-schweizer-gewasser-teileinzugsgebiete-2km2
    - https://opendata.swiss/de/dataset/topographische-einzugsgebiete-der-schweizer-gewasser-teileinzugsgebiete-40-km
* Schneewasseräquivalent Raster basierend auf Satellitenbildern und Bodenbeobachtungen. ([Snow Water - COSMOS | ExoLabs (gitbook.io)](https://exolabs-ch.gitbook.io/cosmos/snow-water))
* Für später bei Bedarf: [Zuleitungen](https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=ch.swisstopo.pixelkarte-grau&layers=ch.bafu.wasser-leitungen,ch.bafu.wasser-rueckgabe,ch.bafu.wasser-entnahme,ch.bafu.wasser-teileinzugsgebiete_2,ch.bafu.wasser-teileinzugsgebiete_40,ch.bafu.wasser-gebietsauslaesse&E=2678533.62&N=1150072.55&zoom=4.965948795623882&layers_opacity=1,1,1,0.75,1,1)

### Ziel

Das Ziel ist eine Machbarkeitsprüfung mit ein paar Anlagen zu machen. Falls erfolgreich kann die Methodik auf alle Anlagen skaliert werden und mittelfristig die Daten als OGD und im Energiedashboard publiziert werden (in welcher Aggregation ist noch abzuklären).

### Resultate

Neben den Füllständen der Speicherseen wären auch die Schneereserven oberhalb der Speicherseen bekannt. Damit stehen mehr Informationen für die Beurteilung der Versorgungssicherheit zur Verfügung. Der einfache Zugang zu diesen Daten bietet zudem einen Mehrwert für Forschung, Politik, Behörden und Stromwirtschaft.

### Ansatz

Die Standorte der Speicherseen liegen als OGD vor. Die Einzugsgebiete der Speicherseen liegen als Polygone im UVEK Geodatenraum vor (1 Polygon pro Stauanlage).
Die Schneewasseräquivalente liegen als 20mx20m Raster vor. Für jede Rasterzelle gibt es einen Wert. Die Idee ist nun alle Werte innerhalb des Polygons zu addieren. Das ergibt das Schneewasseräquivalent innerhalb eines Polygons.

### Verwendung

Falls der Ansatz funktioniert, werden wir die Methodik auf alle Anlagen skalieren und die Daten als Geodaten und im Energiedashboard publizieren.

### Organisation

Bundesamt für Energie BFE

![Schneereserven der Schweizer Stauanlagen](/utils/Folie1.PNG "Schneereserven der Schweizer Stauanlagen")
![Leitfragen](/utils/Folie2.PNG "Leitfragen")
![Ansatz](/utils/Folie3.PNG "Ansatz")
