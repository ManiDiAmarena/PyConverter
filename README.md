# 🐍 Convertitore di Unità Multifunzione 📐⚖️🌡️💾⏱️💨🗺️

Benvenuto nel mio Convertitore di Unità Multifunzione PyConverter, realizzato con Python e la libreria grafica Tkinter! 🚀 Questa applicazione desktop permette di convertire facilmente valori tra diverse unità di misura in svariate categorie.

## ✨ Caratteristiche Principali

* **Ampia Gamma di Categorie:** Converti unità per:
    * 🌡️ **Temperatura:** Celsius, Fahrenheit, Kelvin
    * 📏 **Lunghezza:** Millimetri, Centimetri, Decimetri, Metri, Decametri, Ettometri, Chilometri, Miglia
    * 💾 **Dati:** Bit, Byte, Kilobyte, Megabyte, Gigabyte, Terabyte, Petabyte
    * ⚖️ **Peso/Massa:** Milligrammi, Centigrammi, Decigrammi, Grammi, Decagrammi, Ettogrammi, Chilogrammi, Quintali, Tonnellate, Libbre, Once
    * 💧 **Volume:** Millilitri, Centilitri, Decilitri, Centimetri Cubi, Litri, Decalitri, Ettolitri, Metri Cubi, Galloni (US), Pinte (US)
    * ⏱️ **Tempo:** Secondi, Minuti, Ore, Giorni, Settimane, Mesi, Anni
    * 💨 **Velocità:** Metri al secondo (m/s), Chilometri all'ora (km/h), Miglia all'ora (mph), Nodi (kn)
    * 🗺️ **Area:** Metri Quadrati (m²), Chilometri Quadrati (km²), Ettari (ha), Acri (ac), Piedi Quadrati (ft²)
* **Interfaccia Utente Intuitiva:**
    * Facile selezione della categoria e delle unità dai menu a tendina.
    * Campo di input per il valore da convertire.
    * Visualizzazione chiara del risultato.
* **Aggiornamento Dinamico delle Unità:** Le liste delle unità disponibili si aggiornano automaticamente quando cambi categoria.
* **Inversione Unità:** Un comodo pulsante "Inverti ↕" per scambiare rapidamente l'unità di partenza e quella di destinazione.
* **Validazione dell'Input:** Il campo di input accetta solo valori numerici (interi o decimali).
* **Formattazione dei Risultati:**
    * I risultati sono mostrati con un numero appropriato di cifre decimali.
    * Vengono utilizzati i separatori delle migliaia (in base alle impostazioni locali del sistema) per una migliore leggibilità dei numeri grandi.
* **Finestra a Dimensione Fissa:** L'applicazione ha una dimensione fissa per garantire una visualizzazione coerente.

## 🚀 Installazione e Avvio

1.  **Python:** Assicurati di avere Python 3 installato sul tuo sistema. Puoi scaricarlo da [python.org](https://www.python.org/).
2.  **Tkinter:** La libreria Tkinter (incluso il modulo `ttk` per widget migliorati) è solitamente inclusa nell'installazione standard di Python, quindi non sono necessarie installazioni aggiuntive.
3.  **Scarica il Progetto:**
    * Scarica o clona questo repository.
4.  **Esegui l'Applicazione:**
    * Apri un terminale o prompt dei comandi nella cartella del progetto.
    * Esegui lo script Python:
        ```bash
        python main.py
        ```

## 🎮 Come Usare

1.  **Seleziona Categoria:** Dal primo menu a tendina, scegli il tipo di conversione (es. "Lunghezza", "Peso/Massa").
2.  **Inserisci Valore:** Nel campo "Valore da convertire", digita il numero che desideri convertire.
3.  **Seleziona Unità di Partenza:** Dal menu a tendina "Da:", scegli l'unità da cui stai convertendo.
4.  **Seleziona Unità di Destinazione:** Dal menu a tendina "A:", scegli l'unità in cui vuoi convertire.
5.  **Inverti (Opzionale):** Clicca il pulsante "Inverti ↕" per scambiare l'unità di partenza e quella di destinazione.
6.  **Converti:** Clicca il pulsante "Converti".
7.  **Risultato:** Il risultato della conversione apparirà sotto il pulsante "Converti".
