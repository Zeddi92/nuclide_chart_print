import csv

def read_csv_data(csv_datei, specific_masses_only=False, min_mass=None, max_mass=None):
    nuklide_daten = []

    # CSV-Datei öffnen und Daten lesen
    with open(csv_datei, 'r') as datei:
        csv_reader = csv.DictReader(datei)
        for zeile in csv_reader:
            # Gewünschte Spaltenwerte extrahieren
            z = int(zeile['z'])
            n = int(zeile['n'])
            symbol = zeile['symbol']
            decay_1 = zeile['decay_1']
            decay_1_percent = float(zeile['decay_1_%'].strip()) if zeile['decay_1_%'].strip() else 0
            decay_2 = zeile['decay_2']
            decay_2_percent = float(zeile['decay_2_%'].strip()) if zeile['decay_2_%'].strip() else 0
            decay_3 = zeile['decay_3']
            decay_3_percent = float(zeile['decay_3_%'].strip()) if zeile['decay_3_%'].strip() else 0
            binding = float(zeile['binding'].strip()) if zeile['binding'].strip() else -1
            half_life_sec = float(zeile['half_life_sec'].strip()) if zeile['half_life_sec'].strip() else -1

            # Überprüfe die Massenzahl
            if specific_masses_only and (z < min_mass or z > max_mass):
                continue

            # Nuklid-Daten zum Wörterbuch hinzufügen
            nuklid = {
                'z': z,
                'n': n,
                'symbol': symbol,
                'decay_1': decay_1,
                'decay_1_%': decay_1_percent,
                'decay_2': decay_2,
                'decay_2_%': decay_2_percent,
                'decay_3': decay_3,
                'decay_3_%': decay_3_percent,
                'binding': binding,
                'half_life_sec': half_life_sec,
            }
            nuklide_daten.append(nuklid)

    return nuklide_daten
