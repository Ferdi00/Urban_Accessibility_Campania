import csv
import numpy as np
import matplotlib.pyplot as plt


def conta_intervalli(file_path, colonna):
    intervalli = {
        "0-0.3": 0,
        "0.3-0.5": 0,
        "0.5-0.7": 0,
        "0.7-1": 0,
        "errori": 0,
    }
    valori_validi = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if colonna not in reader.fieldnames:
            raise ValueError(f"Colonna {colonna} non trovata")

        for row in reader:
            try:
                valore = float(row[colonna])
                if valore < 0.0 or valore > 1:
                    intervalli["errori"] += 1
                    continue
                valori_validi.append(valore)

                if 0 <= valore < 0.3:
                    intervalli["0-0.3"] += 1
                elif valore < 0.5:
                    intervalli["0.3-0.5"] += 1
                elif valore < 0.7:
                    intervalli["0.5-0.7"] += 1
                elif valore < 1:
                    intervalli["0.7-1"] += 1
        

            except (ValueError, TypeError):
                intervalli["errori"] += 1

    return intervalli, valori_validi


def statistiche_base(valori):
    stats = {
        "Media": np.mean(valori),
        "Mediana": np.median(valori),
        "Deviazione Standard": np.std(valori),
        "Varianza": np.var(valori),
        "Minimo": np.min(valori),
        "Massimo": np.max(valori),
        "Intervallo": np.ptp(valori),
    }
    return stats


def plot_confronto_bar(salerno, napoli, colonna):
    categorie = [k for k in salerno.keys() if k != "errori"]
    totale_salerno = sum([salerno[k] for k in categorie])
    totale_napoli = sum([napoli[k] for k in categorie])

    # Calcolo percentuali
    percentuali_salerno = [salerno[k] / totale_salerno * 100 for k in categorie]
    percentuali_napoli = [napoli[k] / totale_napoli * 100 for k in categorie]

    x = np.arange(len(categorie))
    width = 0.35

    plt.figure(figsize=(12, 6))
    bars_salerno = plt.bar(
        x - width / 2, percentuali_salerno, width, label="Salerno", color="#4CAF50"
    )
    bars_napoli = plt.bar(
        x + width / 2, percentuali_napoli, width, label="Napoli", color="#2196F3"
    )

    # Aggiungi etichette sopra le barre
    for bar in bars_salerno:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f"{height:.2f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    for bar in bars_napoli:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f"{height:.2f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.xticks(x, categorie, fontsize=10)
    plt.ylabel("Percentuale (%)", fontsize=12)
    plt.title(
        f"Distribuzione % {colonna} per intervallo (Napoli vs Salerno)",
        fontsize=14,
        pad=15,
    )
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

    categorie = [k for k in salerno.keys() if k != "errori"]
    totale_salerno = sum([salerno[k] for k in categorie])
    totale_napoli = sum([napoli[k] for k in categorie])

    # Calcolo percentuali
    percentuali_salerno = [salerno[k] / totale_salerno * 100 for k in categorie]
    percentuali_napoli = [napoli[k] / totale_napoli * 100 for k in categorie]

    x = np.arange(len(categorie))
    width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(x - width / 2, percentuali_salerno, width, label="Salerno", color="#4CAF50")
    plt.bar(x + width / 2, percentuali_napoli, width, label="Napoli", color="#2196F3")

    plt.xticks(x, categorie, fontsize=10)
    plt.ylabel("Percentuale (%)", fontsize=12)
    plt.title(
        "Distribuzione % IAU per intervallo (Napoli vs Salerno)", fontsize=14, pad=15
    )
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()

    categorie = [k for k in salerno.keys() if k != "errori"]
    valori_salerno = [salerno[k] for k in categorie]
    valori_napoli = [napoli[k] for k in categorie]

    x = np.arange(len(categorie))
    width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(x - width / 2, valori_salerno, width, label="Salerno", color="#4CAF50")
    plt.bar(x + width / 2, valori_napoli, width, label="Napoli", color="#2196F3")

    plt.xticks(x, categorie, fontsize=10)
    plt.ylabel("Numero di elementi", fontsize=12)
    plt.title("Confronto distribuzione IAU (5 classi)", fontsize=14, pad=15)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


# --- MAIN ---
try:
    file_salerno = "Dataset_Salerno.csv"
    file_napoli = "Dataset_Napoli.csv"
    colonna = "IAU_famiglie"

    risultati_salerno, valori_salerno = conta_intervalli(file_salerno, colonna)
    risultati_napoli, valori_napoli = conta_intervalli(file_napoli, colonna)

    totale_salerno = len(valori_salerno)
    totale_napoli = len(valori_napoli)

    print(">> Salerno")
    print(f"Totale elementi validi: {totale_salerno}")
    for intervallo in risultati_salerno:
        if intervallo != "errori":
            percentuale = risultati_salerno[intervallo] / totale_salerno * 100
            print(
                f"{intervallo}: {risultati_salerno[intervallo]} valori ({percentuale:.2f}%)"
            )
    print(f"Valori non validi/errori: {risultati_salerno['errori']}")
    print("\nStatistiche Salerno:")
    for k, v in statistiche_base(valori_salerno).items():
        print(f"{k}: {v:.4f}")

    print("\n>> Napoli")
    print(f"Totale elementi validi: {totale_napoli}")
    for intervallo in risultati_napoli:
        if intervallo != "errori":
            percentuale = risultati_napoli[intervallo] / totale_napoli * 100
            print(
                f"{intervallo}: {risultati_napoli[intervallo]} valori ({percentuale:.2f}%)"
            )
    print(f"Valori non validi/errori: {risultati_napoli['errori']}")
    print("\nStatistiche Napoli:")
    for k, v in statistiche_base(valori_napoli).items():
        print(f"{k}: {v:.4f}")

    # Grafico comparativo
    plot_confronto_bar(risultati_salerno, risultati_napoli, colonna)

except Exception as e:
    print(f"Errore: {str(e)}")
