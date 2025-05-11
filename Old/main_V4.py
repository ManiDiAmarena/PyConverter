import tkinter as tk
from tkinter import ttk

# --- Fattori di Conversione ---
# Per Lunghezza, rispetto al Metro
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

# Per Dati, rispetto al Byte (usando prefissi binari: 1 KB = 1024 B)
FATTORI_DATI_A_BYTE = {
    "Bit": 1/8,  # 1 bit = 0.125 Byte
    "Byte": 1.0,
    "Kilobyte": 1024.0,
    "Megabyte": 1024.0**2,
    "Gigabyte": 1024.0**3,
    "Terabyte": 1024.0**4,
    "Petabyte": 1024.0**5
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
    ],
    "Dati": [ # Nuova categoria
        "Bit", "Byte", "Kilobyte", "Megabyte",
        "Gigabyte", "Terabyte", "Petabyte"
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
                if unita_partenza in FATTORI_LUNGHEZZA_A_METRI and \
                   unita_destinazione in FATTORI_LUNGHEZZA_A_METRI:
                    valore_in_metri = val_float * FATTORI_LUNGHEZZA_A_METRI[unita_partenza]
                    risultato_conversione = valore_in_metri / FATTORI_LUNGHEZZA_A_METRI[unita_destinazione]
                else:
                    risultato_conversione = "Unità di Lunghezza non valida"
            
            elif categoria == "Dati": # Nuova logica per la categoria Dati
                if unita_partenza in FATTORI_DATI_A_BYTE and \
                   unita_destinazione in FATTORI_DATI_A_BYTE:
                    valore_in_byte = val_float * FATTORI_DATI_A_BYTE[unita_partenza]
                    risultato_conversione = valore_in_byte / FATTORI_DATI_A_BYTE[unita_destinazione]
                else:
                    risultato_conversione = "Unità Dati non valida"
            else:
                risultato_conversione = "Categoria non supportata"

            # Formattazione del risultato
            if isinstance(risultato_conversione, float):
                if categoria == "Lunghezza" and risultato_conversione != 0:
                    if abs(risultato_conversione) < 0.0001:
                         risultato_formattato = f"{risultato_conversione:.8f}"
                    elif abs(risultato_conversione) < 1:
                         risultato_formattato = f"{risultato_conversione:.4f}"
                    else:
                         risultato_formattato = f"{risultato_conversione:.2f}"
                elif categoria == "Dati":
                    # Per i dati, potremmo volere più precisione o nessuna se il numero è grande
                    if unita_destinazione == "Bit" or unita_destinazione == "Byte" or \
                       (unita_partenza == "Bit" and unita_destinazione != "Bit"): # Se convertiamo da bit a qualcosa di più grande
                        if abs(risultato_conversione) < 1 and risultato_conversione != 0:
                             risultato_formattato = f"{risultato_conversione:.3f}" # es. 0.125 Byte
                        elif risultato_conversione == int(risultato_conversione): # Se è un intero
                             risultato_formattato = f"{int(risultato_conversione)}"
                        else:
                             risultato_formattato = f"{risultato_conversione:.2f}" # Altrimenti 2 decimali
                    elif risultato_conversione == int(risultato_conversione): # Se è un intero
                        risultato_formattato = f"{int(risultato_conversione)}"
                    else: # Per KB, MB, GB, TB, PB, mostra alcuni decimali se necessario
                        risultato_formattato = f"{risultato_conversione:.2f}"
                else: # Per temperatura o se il risultato è 0
                    risultato_formattato = f"{risultato_conversione:.2f}"

                # Rimuovi zeri decimali non necessari se il numero è intero dopo la formattazione
                # (questo è utile per tutti i casi)
                if '.' in risultato_formattato:
                    parti = risultato_formattato.split('.')
                    if len(parti) == 2 and all(c == '0' for c in parti[1]):
                        risultato_formattato = parti[0]
            else: 
                risultato_formattato = risultato_conversione
                
        except ValueError:
            risultato_formattato = "Input numerico non valido"
        except ZeroDivisionError: # Anche se improbabile con i fattori attuali
            risultato_formattato = "Errore Matematico"

    label_risultato.config(text=f"Risultato: {risultato_formattato}")


# --- Creazione della Finestra Principale ---
finestra = tk.Tk()
finestra.title("Convertitore di Unità Multifunzione")
# La larghezza potrebbe aver bisogno di un ulteriore aggiustamento
finestra.geometry("450x300") # Aumentata leggermente per la nuova categoria
finestra.resizable(False, False)

# Frame per organizzare i widget
frame_input = ttk.Frame(finestra, padding="10")
frame_input.pack(pady=5, padx=10, fill="x")

# --- Widget ---

# Selezione Categoria
label_categoria = ttk.Label(frame_input, text="Categoria:")
label_categoria.grid(row=0, column=0, padx=5, pady=5, sticky="w")
categorie_disponibili = list(UNITA_PER_CATEGORIA.keys())
combo_categoria = ttk.Combobox(frame_input, values=categorie_disponibili, width=20, state="readonly") # Larghezza aumentata
combo_categoria.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
combo_categoria.current(0)
combo_categoria.bind("<<ComboboxSelected>>", aggiorna_unita_callback)

# Etichetta e Campo di Input per il valore
label_valore = ttk.Label(frame_input, text="Valore da convertire:")
label_valore.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_valore = ttk.Entry(frame_input, width=25) # Larghezza aumentata
entry_valore.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
entry_valore.focus()

# Menu a tendina per l'unità di partenza
label_da = ttk.Label(frame_input, text="Da:")
label_da.grid(row=2, column=0, padx=5, pady=5, sticky="w")
combo_unita_partenza = ttk.Combobox(frame_input, width=20, state="readonly") # Larghezza aumentata
combo_unita_partenza.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

# Menu a tendina per l'unità di destinazione
label_a = ttk.Label(frame_input, text="A:")
label_a.grid(row=3, column=0, padx=5, pady=5, sticky="w")
combo_unita_destinazione = ttk.Combobox(frame_input, width=20, state="readonly") # Larghezza aumentata
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
