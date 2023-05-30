# Nuklidkarte 3D-Druck

Dieses Projekt erstellt eine 3D-Druckversion der Nuklidkarte, die auf den Daten der "IAEA - Nuclear Data Section" basiert. Es dient als Visualisierungswerkzeug für den 3D-Druck und wurde inspiriert von dem Paper "3D-Druck im Physikunterricht" von Alexander Pusch und Stefan Heusler.

## Quellen

- Nuklidkarten-Daten: IAEA - Nuclear Data Section [Link zur Quelle](https://www-nds.iaea.org/relnsd/vcharthtml/VChartHTML.html)
- Inspiration: "3D-Druck im Physikunterricht" von Alexander Pusch und Stefan Heusler [Link zum Paper](https://www.pro-physik.de/restricted-files/143556)

## Anleitung

1. Installiere die erforderlichen Python-Pakete: numpy, stl, numpy_stl
2. Lade die Nuklidkarten-Daten herunter und speichere sie in das Verzeichnis `Data/` als `data.csv` (Alternativ nutze die API: https://www-nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=all)
3. Passe die Parameter in der Datei `clean_data.py` an, um die Ausgabe zu individualisieren:
   - `invertedView`: Bestimmt die Anzeige der Nuklidkarte (invertierte Ansicht oder nicht)
   - `logScale`: Bestimmt die Skalierung der Höhe (logarithmische Skala oder nicht - noch nicht gut implementiert)
   - `base_height`: Die Dicke der unterliegenden Platte in mm
   - `print_height`: Die maximale Druckhöhe in mm
   - `specific_masses_only`: Begrenzt die Nuklide auf einen bestimmten Massenzahlenbereich
   - `min_mass`: Minimale Massenzahl für die Berücksichtigung der Nuklide
   - `max_mass`: Maximale Massenzahl für die Berücksichtigung der Nuklide
   - `use_given_dimensions`: Verwendet vorgegebene Gesamthöhe und -breite der Nuklidkarte
   - `max_width`: Maximale Breite der Nuklidkarte in mm
   - `max_length`: Maximale Länge der Nuklidkarte in mm
   - `column_width`: Manuell festgelegte Breite der Säulen in mm
   - `column_length`: Manuell festgelegte Länge der Säulen in mm
4. Führe das Skript `clean_data.py` aus, um die 3D-Druckdatei `isotope_data.stl` zu generieren
5. Verwende die generierte STL-Datei, um die Nuklidkarte auf einem 3D-Drucker zu drucken

Weitere Anpassungen und Optionen können im Skript vorgenommen werden, um die Ausgabe anzupassen.
