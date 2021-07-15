# Covid19: Impfung und Inzidenz

In diesem Dokument soll die Inzidenz der Bundesländer in Relation zu ihrer Impfrate dargestellt werden.
Genauer gesagt, zur Nicht-Geimpft-Rate.




In diesen Daten wurde nicht berücksichtigt, ob die jeweilige Impfung schon wirksam ist (nach ca. 14 Tagen), sondern lediglich ob geimpft wurde.

----

#### Datenquellen und Lizenz

Die erhobenen Daten stammen vom Robert Koch Institut und stehen unter [Datenlizenz Deutschland – Namensnennung – Version 2.0](https://www.govdata.de/dl-de/by-2-0)

#### Benutzung

Die Datei collect_data.py läd die aktuellen Daten zur Inzidenz und zur Impfung von impfdashboard.de und vom COVID-19 Datenhub herunter und verbindet sie.
Anschließend wird **diese Readme** hier erzeugt und die ermittelten Daten in einer Datei (nach Datum benannt) weggespeichert. Damit könnte man später Verlaufsgraphen generieren.
Abschließend wird automatisch `git push` durchgeführt, damit die Daten aktualisiert werden.

Es werden ein paar Daten mehr erhoben als hier dargestellt werden, mit der Absicht später "Genesene" zu den Teilgeimpften zu zählen und ggf. die "Verstorbenen" von der Gesamtbevölkerung abzuziehen (falls die Bevölkerungszahl nicht ohnehin in den Daten aktualisiert wird, was ich noch beobachten muss)
