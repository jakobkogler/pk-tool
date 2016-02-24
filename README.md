# pk-tool

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/15d009b4ae1f4b8f948010be53a73746/badge.svg)](https://www.quantifiedcode.com/app/project/15d009b4ae1f4b8f948010be53a73746)

Eine kleine Gui, die PK-Tutoren während der Übungen unterstützen soll. Sie dient zum  effizienten Eintragen der Anwesenheit und der Adhocbewertungen. 

![Screenshot](https://raw.githubusercontent.com/jakobkogler/pk-tool/master/screenshot.png)

## Download

Kompilierte Version für Windows 10: [pk-tool.exe](https://github.com/jakobkogler/pk-tool/releases/download/0.3/pk-tool.exe)

## Voraussetzungen ##

* Python 3.4
* PyQt 5.2.1
* GitPython, falls man Git-Interaktionen wünscht (`pip install gitpython`)

## Benutzung ##

Das Programm startet man mit `python3 pk-tool.py`. 
Nach dem ersten Start des Programmes muss man ein paar Einstellungen vornehmen.
Den Einstellungs-Dialog findet man unter `Datei - Einstellungen`. 
Dort muss man den Pfad zum PK-Repository angeben, und kann außerdem seinen Usernamen festlegen, um eine bessere Übersicht über seine Gruppen zu bekommen. 

Mit Hilfe von Comboboxen kann man die gewünschte Gruppe auswählen und die gewünschte Übung auswählen. 
Dadurch wird eine interactive Tabelle erstellt. 
Man kann die Anwesenheit eintragen (Häckchen setzen), die Adhoc-Aufgabe bewerten (Zahl zwischen 0 und 100), und auch einen Kommentar eintragen. 

### Eingabe via "Befehlen"

Um keine Zeit beim Namensuchen zu vergeuden, kann man all diese Dinge auch mit "Befehlen" erledigen.
Die Syntax dafür ist: 

 - `name a`: Der Student `name` ist anwesend. 
 - `name b`: Der Student `name` ist abwesend. 
 - `name zahl`: Der Student `name` bekommt `zahl` Prozent auf den Adhoc-Teil.
 - `name kommentar`: Fügt den Kommentar `kommentar` beim Studenten `name` hinzu. 
 
Dabei genügt es, einen Substring des echten Namens anzugeben. `odo 100` bewertet bei Studenten `Dennis T. Odom` 100%. 
Das funktioniert aber natürlich nur, wenn der Substring nur in einem Namen vorkommt. 

Anstatt dem Namen kann man auch die Matrikelnummer angeben. Z.B. `1234567 ist krank`. 

### CSV-Datei exportieren

Jede Änderung wird automatisch gespeichert im PK-Repo-Ordner gespeichert. 
Dabei wird automatisch mit `utf-8` kodiert und Unix Line Endings verwendet (auch unter Windows). 
Nach dem Bearbeiten der Files muss man aber manuell die Dateien ins Git-Repo einchecken und pushen. 

### Neue Tabelle anfangen

Per Klick auf `Datei - Neu` wird eine neue CSV-Datei für die aktuell ausgewählte Gruppe erstellt. 
Diese wird automatisch im richtigen Ordner gespeichert. 

### Sortieren

Jede Spalte kann per Klick auf die Spaltenüberschrift sortiert werden.  

### Neue Studenten der Tabelle hinzufügen

Falls ein Student nicht in der Tabelle erscheint (z.B. weil er aus einer anderen Gruppe ist), kann man via `Bearbeiten - Student hinzufügen` eine neue Zeile der Tabelle hinzufügen.
 
### History

Man kann die letzten Änderungen rückgängig machen, bzw. die rückgängig gemachten Schritte wiederherstellen. 
Allerdings geht die History verloren, sobald man auf eine andere CSV-Datei wechselt oder man das Programm schließt.  
Zu finden sind die Befehle unter `Bearbeiten - Zurück` bzw. `Bearbeiten - Vor`. 

### Git-Interaktionen

Man kann unter Einstellungen den experimentelle Git-Interaktionen einstellen. 
Experimentell deswegen, weil es noch nicht auf mehreren Systemen getestet wurde. 
Falls man diesen Modus aktiviert, wird automatisch beim Starten des Programmes das PK-Repository gepullt, sodass man die neuesten Studentendaten bekommt. 
Außerdem kann man nach dem Bearbeiten der Anwesenheitslisten die Änderungen direkt aus dem Programm heraus ins Git einchecken und pushen. 

### Studenten-E-Mails

Man kann außerdem eine Liste der E-Mails aller Stundenten einer Gruppe generieren. 
Diese Liste wird automatisch in die Zwischenablage gelegt und kann anschließend mit `Strg-V` in ein Mail-Programm eingefügt werden. 
Zu finden ist dieser Befehl unter `Bearbeiten - Studenten-E-Mails`. 

## Licence ##

Copyright (C) 2015 Jakob Kogler, [MIT License](https://raw.githubusercontent.com/jakobkogler/pk-tool/master/LICENSE.txt)
