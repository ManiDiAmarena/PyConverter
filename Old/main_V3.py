import tkinter as tk
from tkinter import ttk

# --- Fattori di Conversione (per Lunghezza, rispetto al Metro) ---
FATTORI_LUNGHEZZA_A_METRI = {
    "Millimetri": 0.001,
    "Centimetri": 0.01,
    "Decimetri": 0.1,
    "Metri": 1.0,
    "Decametri": 10.0,
    "Ettometri": 100.0,
    "Chilometri": 1000.0,
    "Miglia": 1609.34  # 1 miglio = 1609.34 metri
}

# --- Funzioni di Conversione Temperatura (invariate) ---
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

# --- Dati per le Unità ---
UNITA_PER_CATEGORIA = {
    "Temperatura": ["Celsius", "Fahrenheit"],
    "Lunghezza": [
        "Millimetri", "Centimetri", "Decimetri", "Metri",
        "Decametri", "Ettometri", "Chilometri", "Miglia"
    ]
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
                # Logica di conversione generalizzata per la lunghezza
                if unita_partenza in FATTORI_LUNGHEZZA_A_METRI and \
                   unita_destinazione in FATTORI_LUNGHEZZA_A_METRI:
                    
                    valore_in_metri = val_float * FATTORI_LUNGHEZZA_A_METRI[unita_partenza]
                    risultato_conversione = valore_in_metri / FATTORI_LUNGHEZZA_A_METRI[unita_destinazione]
                else:
                    risultato_conversione = "Unità di Lunghezza non valida"
            else:
                risultato_conversione = "Categoria non supportata"

            if isinstance(risultato_conversione, float):
                # Per numeri molto piccoli o molto grandi, la notazione scientifica potrebbe essere migliore,
                # ma per ora usiamo una formattazione standard.
                # Aumentiamo le cifre decimali per maggiore precisione nelle conversioni di lunghezza.
                if categoria == "Lunghezza" and risultato_conversione != 0:
                     # Se il risultato è molto piccolo, mostra più decimali, altrimenti meno
                    if abs(risultato_conversione) < 0.0001:
                         risultato_formattato = f"{risultato_conversione:.8f}" # Più precisione per valori piccoli
                    elif abs(risultato_conversione) < 1:
                         risultato_formattato = f"{risultato_conversione:.4f}"
                    else:
                         risultato_formattato = f"{risultato_conversione:.2f}"
                else: # Per temperatura o se il risultato è 0
                    risultato_formattato = f"{risultato_conversione:.2f}"

                # Rimuovi zeri decimali non necessari se il numero è intero dopo la formattazione
                if '.' in risultato_formattato:
                    parte_decimale = risultato_formattato.split('.')[1]
                    if all(c == '0' for c in parte_decimale):
                        risultato_formattato = risultato_formattato.split('.')[0]

            else: 
                risultato_formattato = risultato_conversione
                
        except ValueError:
            risultato_formattato = "Input numerico non valido"
        except ZeroDivisionError:
            risultato_formattato = "Errore: Divisione per zero"


    label_risultato.config(text=f"Risultato: {risultato_formattato}")


# --- Creazione della Finestra Principale ---
finestra = tk.Tk()
finestra.title("Convertitore di Unità")
# Potrebbe essere necessario aggiustare la geometria se i nomi delle unità sono lunghi
finestra.geometry("420x300") # Leggermente più larga per i nomi delle unità
finestra.resizable(False, False)

# Frame per organizzare i widget
frame_input = ttk.Frame(finestra, padding="10")
frame_input.pack(pady=5, padx=10, fill="x")

# --- Widget ---

# Selezione Categoria
label_categoria = ttk.Label(frame_input, text="Categoria:")
label_categoria.grid(row=0, column=0, padx=5, pady=5, sticky="w")
categorie_disponibili = list(UNITA_PER_CATEGORIA.keys())
# Aumentata leggermente la larghezza del combobox categoria
combo_categoria = ttk.Combobox(frame_input, values=categorie_disponibili, width=18, state="readonly")
combo_categoria.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
combo_categoria.current(0)
combo_categoria.bind("<<ComboboxSelected>>", aggiorna_unita_callback)

# Etichetta e Campo di Input per il valore
label_valore = ttk.Label(frame_input, text="Valore da convertire:")
label_valore.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_valore = ttk.Entry(frame_input, width=22) # Aumentata leggermente la larghezza
entry_valore.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
entry_valore.focus()

# Menu a tendina per l'unità di partenza
label_da = ttk.Label(frame_input, text="Da:")
label_da.grid(row=2, column=0, padx=5, pady=5, sticky="w")
# Aumentata leggermente la larghezza dei combobox unità
combo_unita_partenza = ttk.Combobox(frame_input, width=18, state="readonly")
combo_unita_partenza.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

# Menu a tendina per l'unità di destinazione
label_a = ttk.Label(frame_input, text="A:")
label_a.grid(row=3, column=0, padx=5, pady=5, sticky="w")
combo_unita_destinazione = ttk.Combobox(frame_input, width=18, state="readonly")
combo_unita_destinazione.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

# Etichetta per visualizzare il risultato
label_risultato = ttk.Label(finestra, text="Risultato: ", font=("Arial", 12), anchor="center")

# Chiamata iniziale per popolare i menu delle unità
aggiorna_unita_callback()

# Pulsante di Conversione
pulsante_converti = ttk.Button(finestra, text="Converti", command=esegui_conversione, width=15)
pulsante_converti.pack(pady=15)

# Posizionamento dell'etichetta risultato
label_risultato.pack(pady=10, fill="x")

# Configura il grid per espandersi
frame_input.columnconfigure(1, weight=1)

# --- Avvio del Loop Principale dell'Interfaccia ---
finestra.mainloop()
