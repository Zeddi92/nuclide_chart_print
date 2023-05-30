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
print_height = 70   # Der maximale Druck soll 50 mm hoch sein

# Optional: Bereich für Massenzahlen
specific_masses_only = True
min_mass = 10
max_mass = 30

# Optional: Gesamthöhe und -breite der Nuklidkarte
use_given_dimensions = True
max_width = 50      # Maximalbreite der Nuklidkarte in mm
max_length = 50     # Maximallänge der Nuklidkarte in mm

# Manuell festgelegte Breite und Länge der Säulen
column_width = 2  # Breite der Säulen in mm
column_length = 2  # Länge der Säulen in mm

# Optional: Allgemeine Druckhöhe für alle Ausschnitte
# Dieses auf True setzen, falls man sich für alle Slices die gleiche
# Dimensionierung wünscht.
set_general_print_height = False
general_print_height = 8794.5555  # Höhe für alle Ausschnitte in keV

# Optional: Setze eine Baseplate
print_base_plate = True

# Dateipfad zur CSV-Datei
csv_datei = 'Data/data.csv'

# Eine leere Liste zum Speichern der Daten erstellen
nuklide_daten = []

# CSV-Daten lesen
nuklide_daten = read_csv_data(csv_datei, specific_masses_only, min_mass, max_mass)

if set_general_print_height:
    max_energy = {'binding': general_print_height}
else:
    max_energy = max(nuklide_daten, key=lambda x: x['binding'])

print(max_energy['binding'])
height_ratio = print_height / max_energy['binding']

# Überprüfe die Gesamthöhe und -breite der Nuklidkarte
if use_given_dimensions:
    # Bestimme die maximale Anzahl der Spalten und Zeilen basierend auf den maximalen Protonen- und Neutronenzahlen
    max_proton = max(nuklid['z'] for nuklid in nuklide_daten)
    max_neutron = max(nuklid['n'] for nuklid in nuklide_daten)

    # Passe die Breite und Länge der Säulen an die gegebenen Dimensionen an
    column_width = max_width / (max_proton + 1)
    column_length = max_length / (max_neutron + 1)

    # Berechne die Breite und Länge der Basisplatte
    base_width = (max_proton + 1) * column_width
    base_length = (max_neutron + 1) * column_length


    # Berechne die Skalierungsfaktoren für die Positionsberechnung
    position_scale_x = column_width
    position_scale_y = column_length
else:
    # Berechne die maximale Anzahl der Spalten und Zeilen basierend auf den eindeutigen Protonen- und Neutronenwerten
    num_columns = max(nuklid['z'] for nuklid in nuklide_daten)
    num_rows = max(nuklid['n'] for nuklid in nuklide_daten)

    # Berechne die Breite und Länge der Basisplatte
    base_width = num_columns * column_width
    base_length = num_rows * column_length

    # Berechne die Skalierungsfaktoren für die Positionsberechnung
    position_scale_x = base_width / num_columns
    position_scale_y = base_length / num_rows

all_cubes = []

if print_base_plate:
    # Erstelle die Basisplatte
    base_dimensions = np.array([base_width, base_length, base_height])
    base_origin = np.array([0+column_width, 0+column_length, 0])
    base_cube = create_cube(base_origin, base_dimensions)
    all_cubes.append(base_cube)

for nuklid in nuklide_daten:
    proton = nuklid['z']
    neutron = nuklid['n']
    energy = nuklid['binding']

    # Ignoriere Zeilen mit Bindungswert von -1 oder Massenzahlen außerhalb des Bereichs
    if energy == -1 or (specific_masses_only and (proton+neutron < min_mass or proton+neutron > max_mass)):
        continue

    # Berechne die verschobene Position basierend auf den Skalierungsfaktoren
    origin = np.array([proton * position_scale_x, neutron * position_scale_y, 0])

    if invertedView:
        if logScale:
            height = (math.log((max_energy['binding'] - energy)+0.01))+ base_height
        else:
            height = (max_energy['binding'] - energy) * height_ratio + base_height
    else:
        if logScale:
            height = (max_energy['binding']) * height_ratio + base_height
        else:
            height = (math.log(max_energy['binding']+0.01)) + base_height

    dimensions = np.array([column_width, column_length, height])
    cube = create_cube(origin, dimensions)
    all_cubes.append(cube)

combined = mesh.Mesh(np.concatenate([c.data for c in all_cubes]))

combined.save('isotope_data.stl')
