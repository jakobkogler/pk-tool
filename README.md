# PK-TOOL

Eine nette Gui, die PK-Tutoren während der Übungen unterstützen soll.

![Screenshot](https://raw.githubusercontent.com/jakobkogler/pk-tool/master/screenshot.png)

## Download

Kompilierte Version für Windows 10 (und niedriger?): [pk-tool.exe](https://github.com/jakobkogler/pk-tool/releases/download/0.1/pk-tool.exe)

## Voraussetzungen ##

* Python 3.4
* PyQt 5.2.1

## Benutzung ##

Zuerst benötigt man die Teilnehmerlisten von Tuwel. 
Zu finden sind die unter Programmkonstruktion - Anmeldungen - Übungsanmeldung (Normale Gruppen) - Teilnehmer/innen. 
Dort bei den jeweiligen Gruppen die `.txt` (z.B. `185.A79 Programmkon...so12a_Überblick.txt`) runterladen und direkt neben die `pk-tool.py` ablegen. 

Danach kann man das Program kann man einfach mit `python3 pk-tool.py` starten. 

In einer Combobox kann man die gewünschte Gruppe auswählen. 
Dadurch wird eine interactive Tabelle erstellt. 
Man kann die Anwesenheit eintragen (Häckchen setzen), die Adhoc-Aufgabe bewerten (Zahl zwischen 0 und 100), und auch einen Kommentar eintragen. 

### Eingabe via "Befehlen"

Um keine Zeit beim Namensuchen zu vergäuden, kann man all diese Dinge auch mit "Befehlen" erledigen. 
Die Syntax dafür ist: 

 - `name a`: Der Student `name` ist anwesend. 
 - `name b`: Der Student `name` ist abwesend. 
 - `name zahl`: Der Student `name` bekommt `zahl` Prozent auf den Adhoc-Teil.
 - `name kommentar`: Fügt den Kommentar `kommentar` beim Studenten `name` hinzu. 
 
Dabei genügt es, einen Substring des echten Namens anzugeben. `odo 100` bewertet bei Studenten `Dennis T. Odom` 100%. 
Das funktioniert aber natürlich nur, wenn der Substring nur in einem Namen vorkommt. 

### CSV-Datei exportieren

Die fertige Tabelle kann man anschließend via Button-Click als CSV-Datei exportieren. 
Dabei wird automatisch mit `utf-8` kodiert und Unix Line Endings verwendet (auch unter Windows, ist aber nicht getestet). 

### History - Saves

Jede Änderung an der Tabelle wird automatisch zwischengespeichert. 
Es gehen keine Tabelleneintragungen verloren, wenn man das Programm beendet und neu startet. 
Und falls die GUI katastrophal crashed und sich nicht mehr öffnen lässt, 
kann man sich im `Saves`-Ordner den letzten Stand (`gruppe_datum_uhrzeit.csv`) raussuchen und dort mit einem Editor weiterarbeiten. 

Man kann außerdem die letzten Tabellenänderungen rückgängig machen, bzw. die rückgängig gemachten wiederherstellen. 
Diese History-Funktion ist aber nicht besonders intelligent. 

### Neue Tabelle anfangen

Per Button-Click werden alle Tabelleneinträge gelöscht. Kann man per History-Funktion auch rückgängig machen. 

## Sortieren

Jede Spalte kann per Click auf die Spaltenüberschrift sortiert werden.  

### Neue Studenten der Tabelle hinzufügen

Falls ein Student nicht in der Tabelle erscheint (z.B. weil er aus einer anderen Gruppe ist), kann man per Button-Click eine neue Zeile der Tabelle hinzufügen. 
Fängt man eine neue Tabelle an, wird diese aber wieder entfernt. Welchselt ein Student die Gruppe permanent, wäre es besser wenn man sich eine neue Teilnehmerliste von Tuwel holt. 

## Licence ##

Copyright (C) 2015 Jakob Kogler, [MIT License](https://raw.githubusercontent.com/jakobkogler/pk-tool/master/LICENSE.txt)
