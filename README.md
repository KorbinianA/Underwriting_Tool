Underwriting Tool


Schritte:

# Konzept überlegt, was ich zeigen möchte und was in so kurzer Zeit realistisch umsetzbar ist:
	- Zeitplan: wie lange darf ich pro Task brauchen, um heute fertig zu werden:
	- 2h - Dummy Daten ausdenken und erstellen
	- 1h - Datenbank aufbauen
	- 2h - Python Programm zur Visualisierung drüber bauen (Abfrage Tool, mit dem ich auf die verschiedenen Eigenschaften filtern kann)
	- 1h - weitere Features überlegen 

	
# Dummy Daten erstellen als CSV
	- dabei Personendaten, Firmendaten und Einstufungsdaten in unterschiedlichen Tabellen aufteilen
	- Stammdaten: PK, Nachname, Vorname, Geburtstag, Geschlecht, Zivilstand
	- Arbeitsverhältnis: PK, Beruf, Branche, Beschaeftigungsgrad, Lohn, AG_ID, Eintrittsdatum 
	- Gesundheit: PK, Raucher, Groesse, Gewicht, Psychische_Vorerkrankung, Krankentage, IV-Fall
	- Vorsorgedaten: PK, Versicherter Lohn, Todesfallkapital, PK Einkauf, Risiko-Klasse, WEF-Vorbezug
	- Arbeitgeber: AG_ID, Name, Branche, Stadt
	- Einstufung: --> einfacher in temporäre Tabelle
	
# Python-Projekt erstellen 
	- Daten in DB laden

# App Oberfläche erstellen und testen 
	Streamlit eignet sich hier, da kostenlos und das Projekt klein
	--> Problem mit Zugriff auf Datenbank. Deshalb 
	
# Fachbereichsanforderungen simulieren, die ich darstellen möchte: 

	1. Scoring für einzelnen Versicherten abfragen. Das soll beinhalten, dass verschiedene Merkmale eines Versicherten (z.B. Raucher ja/nein) zu einem hohen Score führen und der Score dann in verschiedene Risikostufen einteilt
	
	2. ein hoher PK Einkauf kann für das Underwriting relevant sein, da ein IV-Fall bevorstehen könnte. Hier eine Heatmap mit den relevanten Attributen Altersklasse und Risiko-Klasse, filterbar auf Arbeitgeber
	
	3. der Fachbereich Sales möchte eine Seite die jeweils die top 10 Arbeitgeber ausgibt, also einstellbar in Bezug auf Anzahl Versicherter, Altersschnitt, Lohn, versicherter Lohn, Todesfallkapital, Invalidenrente
	
	4. Allgemeine Rohdatensuche 
	
# Fachbereichsanforderungen umsetzen

# Testen

# Deploy


