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
    "Miglia": 1609.34
}

# Per Dati, rispetto al Byte
FATTORI_DATI_A_BYTE = {
    "Bit": 1/8,
    "Byte": 1.0,
    "Kilobyte": 1024.0,
    "Megabyte": 1024.0**2,
    "Gigabyte": 1024.0**3,
    "Terabyte": 1024.0**4,
    "Petabyte": 1024.0**5
}

# Per Peso/Massa, rispetto al Grammo
FATTORI_PESO_A_GRAMMI = {
    "Milligrammi": 0.001,
    "Centigrammi": 0.01,
    "Decigrammi": 0.1,
    "Grammi": 1.0,
    "Decagrammi": 10.0,
    "Ettogrammi": 100.0,
    "Chilogrammi": 1000.0,
    "Libbre": 453.592,
    "Once": 28.3495
}

# Per Volume, rispetto al Litro
FATTORI_VOLUME_A_LITRI = {
    "Millilitri": 0.001,
    "Centilitri": 0.01,     # NUOVO
    "Decilitri": 0.1,       # NUOVO
    "Centimetri Cubi": 0.001, # 1 cm³ = 1 mL
    "Litri": 1.0,
    "Decalitri": 10.0,      # NUOVO
    "Ettolitri": 100.0,     # NUOVO
    "Metri Cubi": 1000.0,     # 1 m³ = 1000 L
    "Galloni (US)": 3.78541,
    "Pinte (US)": 0.473176
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
    "Dati": [
        "Bit", "Byte", "Kilobyte", "Megabyte",
        "Gigabyte", "Terabyte", "Petabyte"
    ],
    "Peso/Massa": [
        "Milligrammi", "Centigrammi", "Decigrammi", "Grammi",
        "Decagrammi", "Ettogrammi", "Chilogrammi", "Libbre", "Once"
    ],
    "Volume": [ # Lista aggiornata
        "Millilitri", "Centilitri", "Decilitri", "Centimetri Cubi", "Litri",
        "Decalitri", "Ettolitri", "Metri Cubi", "Galloni (US)", "Pinte (US)"
    ]
}

# --- Logica dell'Applicazione ---

def aggiorna_unita_callback(event=None):
    """Aggiorna i menu a tendina delle unità quando la categoria cambia."""
    categoria_selezionata = combo_categoria.get()
    unita_disponibili_categoria = UNITA_PER_CATEGORIA.get(categoria_selezionata, [])
    
    current_from_unit = combo_unita_partenza.get()
    current_to_unit = combo_unita_destinazione.get()

    combo_unita_partenza['values'] = unita_disponibili_categoria
    combo_unita_destinazione['values'] = unita_disponibili_categoria
    
    if unita_disponibili_categoria:
        if current_from_unit in unita_disponibili_categoria:
            combo_unita_partenza.set(current_from_unit)
        else:
            combo_unita_partenza.current(0)

        if current_to_unit in unita_disponibili_categoria and current_to_unit != combo_unita_partenza.get():
            combo_unita_destinazione.set(current_to_unit)
        elif len(unita_disponibili_categoria) > 1:
            first_unit = combo_unita_partenza.get()
            default_to_index = 0
            for i, unit_val in enumerate(unita_disponibili_categoria):
                if unit_val != first_unit:
                    default_to_index = i
                    break
            combo_unita_destinazione.current(default_to_index)
        elif len(unita_disponibili_categoria) == 1:
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
            
            elif categoria == "Dati":
                if unita_partenza in FATTORI_DATI_A_BYTE and \
                   unita_destinazione in FATTORI_DATI_A_BYTE:
                    valore_in_byte = val_float * FATTORI_DATI_A_BYTE[unita_partenza]
                    risultato_conversione = valore_in_byte / FATTORI_DATI_A_BYTE[unita_destinazione]
                else:
                    risultato_conversione = "Unità Dati non valida"

            elif categoria == "Peso/Massa":
                if unita_partenza in FATTORI_PESO_A_GRAMMI and \
                   unita_destinazione in FATTORI_PESO_A_GRAMMI:
                    valore_in_grammi = val_float * FATTORI_PESO_A_GRAMMI[unita_partenza]
                    risultato_conversione = valore_in_grammi / FATTORI_PESO_A_GRAMMI[unita_destinazione]
                else:
                    risultato_conversione = "Unità Peso/Massa non valida"
            
            elif categoria == "Volume":
                if unita_partenza in FATTORI_VOLUME_A_LITRI and \
                   unita_destinazione in FATTORI_VOLUME_A_LITRI:
                    valore_in_litri = val_float * FATTORI_VOLUME_A_LITRI[unita_partenza]
                    risultato_conversione = valore_in_litri / FATTORI_VOLUME_A_LITRI[unita_destinazione]
                else:
                    risultato_conversione = "Unità Volume non valida"
            else:
                risultato_conversione = "Categoria non supportata"

            if isinstance(risultato_conversione, float):
                if abs(risultato_conversione) < 0.00001 and risultato_conversione != 0:
                     risultato_formattato = f"{risultato_conversione:.8g}" 
                elif abs(risultato_conversione) < 1 and risultato_conversione != 0:
                     risultato_formattato = f"{risultato_conversione:.4f}"
                else:
                     risultato_formattato = f"{risultato_conversione:.2f}"
                
                if '.' in risultato_formattato and 'e' not in risultato_formattato.lower():
                    parti = risultato_formattato.split('.')
                    if len(parti) == 2 and all(c == '0' for c in parti[1]):
                        risultato_formattato = parti[0]
            else: 
                risultato_formattato = risultato_conversione
                
        except ValueError:
            risultato_formattato = "Input numerico non valido"
        except ZeroDivisionError:
            risultato_formattato = "Errore Matematico"

    label_risultato.config(text=f"Risultato: {risultato_formattato}")


# --- Creazione della Finestra Principale ---
finestra = tk.Tk()
finestra.title("Convertitore di Unità Multifunzione")
finestra.geometry("500x300") 
finestra.resizable(False, False)

# Frame per organizzare i widget
frame_input = ttk.Frame(finestra, padding="10")
frame_input.pack(pady=5, padx=10, fill="x")

# --- Widget ---
label_categoria = ttk.Label(frame_input, text="Categoria:")
label_categoria.grid(row=0, column=0, padx=5, pady=5, sticky="w")
categorie_disponibili = list(UNITA_PER_CATEGORIA.keys())
combo_categoria = ttk.Combobox(frame_input, values=categorie_disponibili, width=24, state="readonly")
combo_categoria.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
combo_categoria.current(0)
combo_categoria.bind("<<ComboboxSelected>>", aggiorna_unita_callback)

label_valore = ttk.Label(frame_input, text="Valore da convertire:")
label_valore.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_valore = ttk.Entry(frame_input, width=30) 
entry_valore.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
entry_valore.focus()

label_da = ttk.Label(frame_input, text="Da:")
label_da.grid(row=2, column=0, padx=5, pady=5, sticky="w")
combo_unita_partenza = ttk.Combobox(frame_input, width=24, state="readonly") 
combo_unita_partenza.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

label_a = ttk.Label(frame_input, text="A:")
label_a.grid(row=3, column=0, padx=5, pady=5, sticky="w")
combo_unita_destinazione = ttk.Combobox(frame_input, width=24, state="readonly") 
combo_unita_destinazione.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

label_risultato = ttk.Label(finestra, text="Risultato: ", font=("Arial", 12), anchor="center")

aggiorna_unita_callback()

pulsante_converti = ttk.Button(finestra, text="Converti", command=esegui_conversione, width=15)
pulsante_converti.pack(pady=15)

label_risultato.pack(pady=10, fill="x")

frame_input.columnconfigure(1, weight=1)

finestra.mainloop()
