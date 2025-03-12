shit = []
for year in [2022, 2023, 2024]:
    for month in range(12):
        shit.append(f"../data/{year}{month+1:02d}_Movilidad_obligada_distritos.csv")

print(shit)