import tkinter as tk
from tkinter import ttk
import locale # Importa il modulo locale

# --- Impostazione del Locale ---
# Prova a impostare il locale predefinito del sistema per la formattazione dei numeri.
# Se fallisce (ad es. su alcuni sistemi minimi), la formattazione dei separatori potrebbe non funzionare,
# ma il programma continuerà a girare.
try:
    locale.setlocale(locale.LC_ALL, '') 
except locale.Error as e:
    print(f"Attenzione: Impossibile impostare il locale predefinito del sistema ({e}). "
          "La formattazione dei numeri potrebbe non includere i separatori delle migliaia.")

# --- Fattori di Conversione ---
# (Fattori di conversione invariati rispetto alla versione precedente)
FATTORI_LUNGHEZZA_A_METRI = {
    "Millimetri": 0.001,"Centimetri": 0.01,"Decimetri": 0.1,"Metri": 1.0,
    "Decametri": 10.0,"Ettometri": 100.0,"Chilometri": 1000.0,"Miglia": 1609.34
}
FATTORI_DATI_A_BYTE = {
    "Bit": 1/8,"Byte": 1.0,"Kilobyte": 1024.0,"Megabyte": 1024.0**2,
    "Gigabyte": 1024.0**3,"Terabyte": 1024.0**4,"Petabyte": 1024.0**5
}
FATTORI_PESO_A_GRAMMI = {
    "Milligrammi": 0.001,"Centigrammi": 0.01,"Decigrammi": 0.1,"Grammi": 1.0,
    "Decagrammi": 10.0,"Ettogrammi": 100.0,"Chilogrammi": 1000.0,
    "Quintali": 100000.0,"Tonnellate": 1000000.0,"Libbre": 453.592,"Once": 28.3495
}
FATTORI_VOLUME_A_LITRI = {
    "Millilitri": 0.001,"Centilitri": 0.01,"Decilitri": 0.1,"Centimetri Cubi": 0.001,
    "Litri": 1.0,"Decalitri": 10.0,"Ettolitri": 100.0,"Metri Cubi": 1000.0,
    "Galloni (US)": 3.78541,"Pinte (US)": 0.473176
}
FATTORI_TEMPO_A_SECONDI = {
    "Secondi": 1.0,"Minuti": 60.0,"Ore": 3600.0,"Giorni": 86400.0,
    "Settimane": 604800.0,"Mesi": 2629800.0,"Anni": 31557600.0
}
FATTORI_VELOCITA_A_METRI_PER_SECONDO = {
    "Metri al secondo (m/s)": 1.0,"Chilometri all'ora (km/h)": 1000.0/3600.0,
    "Miglia all'ora (mph)": 1609.34/3600.0,"Nodi (kn)": 1852.0/3600.0
}
FATTORI_AREA_A_METRI_QUADRATI = {
    "Metri Quadrati (m²)": 1.0,"Chilometri Quadrati (km²)": 1000000.0,
    "Ettari (ha)": 10000.0,"Acri (ac)": 4046.86,"Piedi Quadrati (ft²)": 0.092903
}

# --- Funzioni di Conversione Temperatura ---
# (Funzioni di conversione temperatura invariate)
def celsius_a_fahrenheit(celsius):
    try: return (float(celsius) * 9/5) + 32
    except ValueError: return "Errore Input"
def fahrenheit_a_celsius(fahrenheit):
    try: return (float(fahrenheit) - 32) * 5/9
    except ValueError: return "Errore Input"
def celsius_a_kelvin(celsius):
    try: return float(celsius) + 273.15
    except ValueError: return "Errore Input"
def kelvin_a_celsius(kelvin):
    try: return float(kelvin) - 273.15
    except ValueError: return "Errore Input"
def fahrenheit_a_kelvin(fahrenheit):
    celsius = fahrenheit_a_celsius(fahrenheit)
    if isinstance(celsius, str): return celsius
    return celsius_a_kelvin(celsius)
def kelvin_a_fahrenheit(kelvin):
    celsius = kelvin_a_celsius(kelvin)
    if isinstance(celsius, str): return celsius
    return celsius_a_fahrenheit(celsius)

# --- Dati per le Unità ---
# (UNITA_PER_CATEGORIA invariato)
UNITA_PER_CATEGORIA = {
    "Temperatura": ["Celsius", "Fahrenheit", "Kelvin"],
    "Lunghezza": ["Millimetri", "Centimetri", "Decimetri", "Metri", "Decametri", "Ettometri", "Chilometri", "Miglia"],
    "Dati": ["Bit", "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte", "Petabyte"],
    "Peso/Massa": ["Milligrammi", "Centigrammi", "Decigrammi", "Grammi", "Decagrammi", "Ettogrammi", "Chilogrammi", "Quintali", "Tonnellate", "Libbre", "Once"],
    "Volume": ["Millilitri", "Centilitri", "Decilitri", "Centimetri Cubi", "Litri", "Decalitri", "Ettolitri", "Metri Cubi", "Galloni (US)", "Pinte (US)"],
    "Tempo": ["Secondi", "Minuti", "Ore", "Giorni", "Settimane", "Mesi", "Anni"],
    "Velocità": ["Metri al secondo (m/s)", "Chilometri all'ora (km/h)", "Miglia all'ora (mph)", "Nodi (kn)"],
    "Area": ["Metri Quadrati (m²)", "Chilometri Quadrati (km²)", "Ettari (ha)", "Acri (ac)", "Piedi Quadrati (ft²)"]
}

# --- Logica dell'Applicazione ---
# (aggiorna_unita_callback e inverti_unita invariate)
def aggiorna_unita_callback(event=None):
    categoria_selezionata = combo_categoria.get()
    unita_disponibili_categoria = UNITA_PER_CATEGORIA.get(categoria_selezionata, [])
    current_from_unit = combo_unita_partenza.get()
    current_to_unit = combo_unita_destinazione.get()
    combo_unita_partenza['values'] = unita_disponibili_categoria
    combo_unita_destinazione['values'] = unita_disponibili_categoria
    if unita_disponibili_categoria:
        if current_from_unit in unita_disponibili_categoria: combo_unita_partenza.set(current_from_unit)
        else: combo_unita_partenza.current(0)
        if current_to_unit in unita_disponibili_categoria and current_to_unit != combo_unita_partenza.get(): combo_unita_destinazione.set(current_to_unit)
        elif len(unita_disponibili_categoria) > 1:
            first_unit = combo_unita_partenza.get(); default_to_index = 0
            for i, unit_val in enumerate(unita_disponibili_categoria):
                if unit_val != first_unit: default_to_index = i; break
            combo_unita_destinazione.current(default_to_index)
        elif len(unita_disponibili_categoria) == 1: combo_unita_destinazione.current(0)
        else: 
            combo_unita_destinazione.set(''); 
            if unita_disponibili_categoria: combo_unita_destinazione.current(0)
    else: combo_unita_partenza.set(''); combo_unita_destinazione.set('')
    label_risultato.config(text="Risultato: ")

def inverti_unita():
    unita_da = combo_unita_partenza.get(); unita_a = combo_unita_destinazione.get()
    if unita_da and unita_a: 
        combo_unita_partenza.set(unita_a); combo_unita_destinazione.set(unita_da)
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
            # ... (logica di conversione per ogni categoria invariata) ...
            elif categoria == "Temperatura":
                if unita_partenza == "Celsius" and unita_destinazione == "Fahrenheit": risultato_conversione = celsius_a_fahrenheit(val_float)
                elif unita_partenza == "Fahrenheit" and unita_destinazione == "Celsius": risultato_conversione = fahrenheit_a_celsius(val_float)
                elif unita_partenza == "Celsius" and unita_destinazione == "Kelvin": risultato_conversione = celsius_a_kelvin(val_float)
                elif unita_partenza == "Kelvin" and unita_destinazione == "Celsius": risultato_conversione = kelvin_a_celsius(val_float)
                elif unita_partenza == "Fahrenheit" and unita_destinazione == "Kelvin": risultato_conversione = fahrenheit_a_kelvin(val_float)
                elif unita_partenza == "Kelvin" and unita_destinazione == "Fahrenheit": risultato_conversione = kelvin_a_fahrenheit(val_float)
                else: risultato_conversione = "Conversione Temp. non supportata"
            elif categoria == "Lunghezza":
                if unita_partenza in FATTORI_LUNGHEZZA_A_METRI and unita_destinazione in FATTORI_LUNGHEZZA_A_METRI:
                    val_in_base = val_float * FATTORI_LUNGHEZZA_A_METRI[unita_partenza]
                    risultato_conversione = val_in_base / FATTORI_LUNGHEZZA_A_METRI[unita_destinazione]
                else: risultato_conversione = "Unità di Lunghezza non valida"
            elif categoria == "Dati":
                if unita_partenza in FATTORI_DATI_A_BYTE and unita_destinazione in FATTORI_DATI_A_BYTE:
                    val_in_base = val_float * FATTORI_DATI_A_BYTE[unita_partenza]
                    risultato_conversione = val_in_base / FATTORI_DATI_A_BYTE[unita_destinazione]
                else: risultato_conversione = "Unità Dati non valida"
            elif categoria == "Peso/Massa":
                if unita_partenza in FATTORI_PESO_A_GRAMMI and unita_destinazione in FATTORI_PESO_A_GRAMMI:
                    val_in_base = val_float * FATTORI_PESO_A_GRAMMI[unita_partenza]
                    risultato_conversione = val_in_base / FATTORI_PESO_A_GRAMMI[unita_destinazione]
                else: risultato_conversione = "Unità Peso/Massa non valida"
            elif categoria == "Volume":
                if unita_partenza in FATTORI_VOLUME_A_LITRI and unita_destinazione in FATTORI_VOLUME_A_LITRI:
                    val_in_base = val_float * FATTORI_VOLUME_A_LITRI[unita_partenza]
                    risultato_conversione = val_in_base / FATTORI_VOLUME_A_LITRI[unita_destinazione]
                else: risultato_conversione = "Unità Volume non valida"
            elif categoria == "Tempo":
                if unita_partenza in FATTORI_TEMPO_A_SECONDI and unita_destinazione in FATTORI_TEMPO_A_SECONDI:
                    val_in_base = val_float * FATTORI_TEMPO_A_SECONDI[unita_partenza]
                    risultato_conversione = val_in_base / FATTORI_TEMPO_A_SECONDI[unita_destinazione]
                else: risultato_conversione = "Unità Tempo non valida"
            elif categoria == "Velocità":
                if unita_partenza in FATTORI_VELOCITA_A_METRI_PER_SECONDO and unita_destinazione in FATTORI_VELOCITA_A_METRI_PER_SECONDO:
                    val_in_base = val_float * FATTORI_VELOCITA_A_METRI_PER_SECONDO[unita_partenza]
                    risultato_conversione = val_in_base / FATTORI_VELOCITA_A_METRI_PER_SECONDO[unita_destinazione]
                else: risultato_conversione = "Unità Velocità non valida"
            elif categoria == "Area":
                if unita_partenza in FATTORI_AREA_A_METRI_QUADRATI and unita_destinazione in FATTORI_AREA_A_METRI_QUADRATI:
                    val_in_base = val_float * FATTORI_AREA_A_METRI_QUADRATI[unita_partenza]
                    risultato_conversione = val_in_base / FATTORI_AREA_A_METRI_QUADRATI[unita_destinazione]
                else: risultato_conversione = "Unità Area non valida"
            else:
                risultato_conversione = "Categoria non supportata"

            # --- MODIFICA: Formattazione del risultato ---
            if isinstance(risultato_conversione, float):
                # Per numeri molto piccoli o molto grandi, la notazione scientifica ('g') è spesso migliore.
                # Soglie per decidere quando usare 'g'.
                if (abs(risultato_conversione) < 0.0001 and risultato_conversione != 0) or \
                   abs(risultato_conversione) >= 1_000_000_000: # 1 miliardo
                    risultato_formattato = f"{risultato_conversione:.4g}" 
                    # .4g usa fino a 4 cifre significative e sceglie tra notazione fissa o scientifica.
                else:
                    # Altrimenti, formatta con separatori delle migliaia e un numero ragionevole di decimali.
                    # Determina la precisione.
                    if abs(risultato_conversione - round(risultato_conversione)) < 1e-9: # È praticamente un intero
                        precisione = 0
                    elif abs(risultato_conversione) < 1: # Numeri piccoli ma non piccolissimi
                        precisione = 4 
                    else: # Default per altri numeri
                        precisione = 2
                    
                    # La f-string con ',' usa il separatore delle migliaia del locale corrente.
                    risultato_formattato = f"{risultato_conversione:,.{precisione}f}"
            else: 
                # Se non è un float (es. "Errore Input"), converti semplicemente in stringa.
                risultato_formattato = str(risultato_conversione)
            # --- FINE MODIFICA ---
                
        except ValueError:
            risultato_formattato = "Input numerico non valido"
        except ZeroDivisionError:
            risultato_formattato = "Errore Matematico"

    label_risultato.config(text=f"Risultato: {risultato_formattato}")

# (Funzione validate_numeric_input invariata)
def validate_numeric_input(P):
    if P == "": return True
    try:
        if P.count('.') <= 1 and all(char.isdigit() or char == '.' for char in P):
            if P == ".": return False
            return True
        else: return False
    except ValueError: return False

# --- Creazione della Finestra Principale ---
# (Creazione finestra e widget invariata, tranne la registrazione del comando di validazione)
finestra = tk.Tk()
finestra.title("Convertitore di Unità Multifunzione")
finestra.geometry("540x330") 
finestra.resizable(False, False)

frame_input = ttk.Frame(finestra, padding="10")
frame_input.pack(pady=5, padx=10, fill="x")

label_categoria = ttk.Label(frame_input, text="Categoria:")
label_categoria.grid(row=0, column=0, padx=5, pady=5, sticky="w")
categorie_disponibili = list(UNITA_PER_CATEGORIA.keys())
combo_categoria = ttk.Combobox(frame_input, values=categorie_disponibili, width=28, state="readonly")
combo_categoria.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew") 
combo_categoria.current(0)
combo_categoria.bind("<<ComboboxSelected>>", aggiorna_unita_callback)

label_valore = ttk.Label(frame_input, text="Valore da convertire:")
label_valore.grid(row=1, column=0, padx=5, pady=5, sticky="w")
validate_cmd = finestra.register(validate_numeric_input)
entry_valore = ttk.Entry(frame_input, width=34, validate="key", validatecommand=(validate_cmd, '%P'))
entry_valore.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew") 
entry_valore.focus()

label_da = ttk.Label(frame_input, text="Da:")
label_da.grid(row=2, column=0, padx=5, pady=5, sticky="w")
combo_unita_partenza = ttk.Combobox(frame_input, width=28, state="readonly") 
combo_unita_partenza.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew") 

pulsante_inverti = ttk.Button(frame_input, text="Inverti ↕", command=inverti_unita, width=10)
pulsante_inverti.grid(row=3, column=0, columnspan=3, padx=5, pady=(5,0), sticky="n") 

label_a = ttk.Label(frame_input, text="A:")
label_a.grid(row=4, column=0, padx=5, pady=5, sticky="w")
combo_unita_destinazione = ttk.Combobox(frame_input, width=28, state="readonly") 
combo_unita_destinazione.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="ew") 

label_risultato = ttk.Label(finestra, text="Risultato: ", font=("Arial", 12), anchor="center")
aggiorna_unita_callback() 
pulsante_converti = ttk.Button(finestra, text="Converti", command=esegui_conversione, width=15)
pulsante_converti.pack(pady=10) 
label_risultato.pack(pady=5, fill="x") 
frame_input.columnconfigure(1, weight=1)
finestra.mainloop()
