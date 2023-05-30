import numpy as np
from stl import mesh
import csv
import math
from geometry import create_cube
from csv_reader import read_csv_data

# Setze Parameter
invertedView = True
logScale = False
base_height = 5     # Die Dicke der Platte soll 5mm sein
print_height = 50   # Der maximale Druck soll 50 mm hoch sein

# Optional: Bereich für Massenzahlen
specific_masses_only = True
min_mass = 0
max_mass = 12

# Optional: Gesamthöhe und -breite der Nuklidkarte
use_given_dimensions = False
max_width = 20      # Maximalbreite der Nuklidkarte in mm
max_length = 20     # Maximallänge der Nuklidkarte in mm

# Manuell festgelegte Breite und Länge der Säulen
column_width = 2  # Breite der Säulen in mm
column_length = 2  # Länge der Säulen in mm

# Dateipfad zur CSV-Datei
csv_datei = 'Data/data.csv'

# Eine leere Liste zum Speichern der Daten erstellen
nuklide_daten = []

# CSV-Daten lesen
nuklide_daten = read_csv_data(csv_datei, specific_masses_only, min_mass, max_mass)

max_energy = max(nuklide_daten, key=lambda x: x['binding'])
height_ratio = print_height / max_energy['binding']

# Überprüfe die Gesamthöhe und -breite der Nuklidkarte
if use_given_dimensions:
    # Bestimme die maximale Anzahl der Spalten und Zeilen basierend auf den maximalen Protonen- und Neutronenzahlen
    max_proton = max(nuklid['z'] for nuklid in nuklide_daten)
    max_neutron = max(nuklid['n'] for nuklid in nuklide_daten)
    num_columns = max_proton + 1
    num_rows = max_neutron + 1

    # Berechne die Spaltenbreite und -länge basierend auf den gegebenen Dimensionen
    column_width = max_width / num_columns
    column_length = max_length / num_rows

    # Berechne die Skalierungsfaktoren für die Positionsberechnung
    position_scale_x = max_width / num_columns
    position_scale_y = max_length / num_rows
else:
    # Extrahiere eindeutige Protonen- und Neutronenwerte aus nuklide_daten
    unique_protons = sorted(list(set(nuklid['z'] for nuklid in nuklide_daten)))
    unique_neutrons = sorted(list(set(nuklid['n'] for nuklid in nuklide_daten)))

    # Berechne die Skalierungsfaktoren für die Positionsberechnung
    position_scale_x = column_width
    position_scale_y = column_length


all_cubes = []
for nuklid in nuklide_daten:
    proton = nuklid['z']
    neutron = nuklid['n']
    energy = nuklid['binding']

    # Ignoriere Zeilen mit Bindungswert von -1 oder Massenzahlen außerhalb des Bereichs
    if energy == -1 or (specific_masses_only and (proton < min_mass or proton > max_mass)):
        continue

    # Berechne die verschobene Position basierend auf den Skalierungsfaktoren
    origin = np.array([proton * position_scale_x, neutron * position_scale_y, 0])

    if invertedView:
        # Lineare Korrektur basierend auf print_height
        height = (max_energy['binding'] - energy) * height_ratio + base_height
    else:
        height = (max_energy['binding']) * height_ratio + base_height

    if logScale:
        height = math.log((height) * 10000)  # Adding 1 to avoid log(0) situation

    dimensions = np.array([column_width, column_length, height])
    cube = create_cube(origin, dimensions)
    all_cubes.append(cube)

combined = mesh.Mesh(np.concatenate([c.data for c in all_cubes]))

combined.save('isotope_data.stl')
