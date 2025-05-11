import tkinter as tk
from tkinter import ttk # ttk offre widget con un aspetto un po' più moderno rispetto a quelli base di tkinter

# --- Funzioni di Conversione ---
def celsius_a_fahrenheit(celsius):
    try:
        return (float(celsius) * 9/5) + 32
    except ValueError:
        return "Errore"

def fahrenheit_a_celsius(fahrenheit):
    try:
        return (float(fahrenheit) - 32) * 5/9
    except ValueError:
        return "Errore"

# --- Logica dell'Applicazione ---
def esegui_conversione():
    valore_input = entry_valore.get()
    unita_partenza = combo_unita_partenza.get()
    unita_destinazione = combo_unita_destinazione.get()
    risultato = ""

    if not valore_input:
        risultato = "Inserisci un valore"
    else:
        try:
            val_float = float(valore_input) # Controlla se è un numero
            if unita_partenza == unita_destinazione:
                risultato = val_float # Nessuna conversione necessaria
            elif unita_partenza == "Celsius" and unita_destinazione == "Fahrenheit":
                risultato = celsius_a_fahrenheit(val_float)
            elif unita_partenza == "Fahrenheit" and unita_destinazione == "Celsius":
                risultato = fahrenheit_a_celsius(val_float)
            else:
                risultato = "Conversione non supportata"

            if isinstance(risultato, float):
                risultato_formattato = f"{risultato:.2f}" # Formatta a due cifre decimali
            else:
                risultato_formattato = str(risultato)

        except ValueError:
            risultato_formattato = "Input non valido"

    label_risultato.config(text=f"Risultato: {risultato_formattato}")


# --- Creazione della Finestra Principale ---
finestra = tk.Tk()
finestra.title("Convertitore di Temperatura")
finestra.geometry("350x250") # Dimensioni della finestra
finestra.resizable(False, False)

# Frame per organizzare i widget
frame_input = ttk.Frame(finestra, padding="10")
frame_input.pack(pady=10)

# --- Widget ---
# Etichetta e Campo di Input per il valore
label_valore = ttk.Label(frame_input, text="Valore da convertire:")
label_valore.grid(row=0, column=0, padx=5, pady=5, sticky="w")

entry_valore = ttk.Entry(frame_input, width=15)
entry_valore.grid(row=0, column=1, padx=5, pady=5)
entry_valore.focus() # Mette il cursore nel campo di input all'avvio

# Menu a tendina per l'unità di partenza
label_da = ttk.Label(frame_input, text="Da:")
label_da.grid(row=1, column=0, padx=5, pady=5, sticky="w")
unita_disponibili = ["Celsius", "Fahrenheit"]
combo_unita_partenza = ttk.Combobox(frame_input, values=unita_disponibili, width=12, state="readonly")
combo_unita_partenza.grid(row=1, column=1, padx=5, pady=5)
combo_unita_partenza.current(0)  # Imposta "Celsius" come predefinito

# Menu a tendina per l'unità di destinazione
label_a = ttk.Label(frame_input, text="A:")
label_a.grid(row=2, column=0, padx=5, pady=5, sticky="w")
combo_unita_destinazione = ttk.Combobox(frame_input, values=unita_disponibili, width=12, state="readonly")
combo_unita_destinazione.grid(row=2, column=1, padx=5, pady=5)
combo_unita_destinazione.current(1)  # Imposta "Fahrenheit" come predefinito


# Pulsante di Conversione
pulsante_converti = ttk.Button(finestra, text="Converti", command=esegui_conversione)
pulsante_converti.pack(pady=10)

# Etichetta per visualizzare il risultato
label_risultato = ttk.Label(finestra, text="Risultato: ", font=("Arial", 12))
label_risultato.pack(pady=10)


# --- Avvio del Loop Principale dell'Interfaccia ---
finestra.mainloop()