import tkinter as tk
from tkinter import ttk

# --- Fattori di Conversione ---
KM_PER_MIGLIA = 1.60934
MIGLIA_PER_KM = 0.621371

# --- Funzioni di Conversione ---
def celsius_a_fahrenheit(celsius):
    try:
        return (float(celsius) * 9/5) + 32
    except ValueError:
        return "Errore Input"

def fahrenheit_a_celsius(fahrenheit):
    try:
        return (float(fahrenheit) - 32) * 5/9
    except ValueError:
        return "Errore Input"

def kilometri_a_miglia(km):
    try:
        return float(km) * MIGLIA_PER_KM
    except ValueError:
        return "Errore Input"

def miglia_a_kilometri(miglia):
    try:
        return float(miglia) * KM_PER_MIGLIA
    except ValueError:
        return "Errore Input"

# --- Dati per le Unità ---
UNITA_PER_CATEGORIA = {
    "Temperatura": ["Celsius", "Fahrenheit"],
    "Lunghezza": ["Chilometri", "Miglia"]
}

# --- Logica dell'Applicazione ---

def aggiorna_unita_callback(event=None):
    """Aggiorna i menu a tendina delle unità quando la categoria cambia."""
    categoria_selezionata = combo_categoria.get()
    unita_disponibili_categoria = UNITA_PER_CATEGORIA.get(categoria_selezionata, [])
    
    combo_unita_partenza['values'] = unita_disponibili_categoria
    combo_unita_destinazione['values'] = unita_disponibili_categoria
    
    if unita_disponibili_categoria:
        combo_unita_partenza.current(0)
        if len(unita_disponibili_categoria) > 1:
            combo_unita_destinazione.current(1)
        else:
            combo_unita_destinazione.current(0)
    else:
        combo_unita_partenza.set('')
        combo_unita_destinazione.set('')
    
    # Resetta il risultato quando la categoria cambia
    # Ora label_risultato è definito quando questa funzione viene chiamata per la prima volta
    label_risultato.config(text="Risultato: ")


def esegui_conversione():
    valore_input_str = entry_valore.get()
    categoria = combo_categoria.get()
    unita_partenza = combo_unita_partenza.get()
    unita_destinazione = combo_unita_destinazione.get()
    risultato_conversione = ""

    if not valore_input_str:
        risultato_formattato = "Inserisci un valore"
    elif not categoria or not unita_partenza or not unita_destinazione:
        risultato_formattato = "Seleziona categoria/unità"
    else:
        try:
            val_float = float(valore_input_str)

            if unita_partenza == unita_destinazione:
                risultato_conversione = val_float
            
            elif categoria == "Temperatura":
                if unita_partenza == "Celsius" and unita_destinazione == "Fahrenheit":
                    risultato_conversione = celsius_a_fahrenheit(val_float)
                elif unita_partenza == "Fahrenheit" and unita_destinazione == "Celsius":
                    risultato_conversione = fahrenheit_a_celsius(val_float)
                else:
                    risultato_conversione = "Conversione Temp. non supportata"
            
            elif categoria == "Lunghezza":
                if unita_partenza == "Chilometri" and unita_destinazione == "Miglia":
                    risultato_conversione = kilometri_a_miglia(val_float)
                elif unita_partenza == "Miglia" and unita_destinazione == "Chilometri":
                    risultato_conversione = miglia_a_kilometri(val_float)
                else:
                    risultato_conversione = "Conversione Lung. non supportata"
            else:
                risultato_conversione = "Categoria non supportata"

            if isinstance(risultato_conversione, float):
                risultato_formattato = f"{risultato_conversione:.2f}"
            else: 
                risultato_formattato = risultato_conversione
                
        except ValueError:
            risultato_formattato = "Input numerico non valido"

    label_risultato.config(text=f"Risultato: {risultato_formattato}")


# --- Creazione della Finestra Principale ---
finestra = tk.Tk()
finestra.title("Convertitore di Unità")
finestra.geometry("400x300")
finestra.resizable(False, False)

# Frame per organizzare i widget
frame_input = ttk.Frame(finestra, padding="10")
frame_input.pack(pady=5, padx=10, fill="x")

# --- Widget ---

# Selezione Categoria
label_categoria = ttk.Label(frame_input, text="Categoria:")
label_categoria.grid(row=0, column=0, padx=5, pady=5, sticky="w")
categorie_disponibili = list(UNITA_PER_CATEGORIA.keys())
combo_categoria = ttk.Combobox(frame_input, values=categorie_disponibili, width=15, state="readonly")
combo_categoria.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
combo_categoria.current(0)
combo_categoria.bind("<<ComboboxSelected>>", aggiorna_unita_callback)

# Etichetta e Campo di Input per il valore
label_valore = ttk.Label(frame_input, text="Valore da convertire:")
label_valore.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_valore = ttk.Entry(frame_input, width=18)
entry_valore.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
entry_valore.focus()

# Menu a tendina per l'unità di partenza
label_da = ttk.Label(frame_input, text="Da:")
label_da.grid(row=2, column=0, padx=5, pady=5, sticky="w")
combo_unita_partenza = ttk.Combobox(frame_input, width=15, state="readonly")
combo_unita_partenza.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

# Menu a tendina per l'unità di destinazione
label_a = ttk.Label(frame_input, text="A:")
label_a.grid(row=3, column=0, padx=5, pady=5, sticky="w")
combo_unita_destinazione = ttk.Combobox(frame_input, width=15, state="readonly")
combo_unita_destinazione.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

# --- MODIFICA: Definizione di label_risultato spostata QUI ---
# Etichetta per visualizzare il risultato
label_risultato = ttk.Label(finestra, text="Risultato: ", font=("Arial", 12), anchor="center")
# La chiamata a .pack() per label_risultato rimane più in basso per l'ordine di layout

# Chiamata iniziale per popolare i menu delle unità in base alla categoria predefinita
# Ora label_risultato esiste quando questa funzione viene chiamata.
aggiorna_unita_callback()

# Pulsante di Conversione
pulsante_converti = ttk.Button(finestra, text="Converti", command=esegui_conversione, width=15)
pulsante_converti.pack(pady=15)

# Posizionamento dell'etichetta risultato (la chiamata a .pack() rimane qui)
label_risultato.pack(pady=10, fill="x")

# Configura il grid per espandersi
frame_input.columnconfigure(1, weight=1)

# --- Avvio del Loop Principale dell'Interfaccia ---
finestra.mainloop()
