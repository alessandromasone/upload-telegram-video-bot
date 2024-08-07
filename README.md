
# Upload Telegram Video Bot

Questo repository contiene uno script Python per caricare video su un canale Telegram. Lo script gestisce automaticamente video di grandi dimensioni, dividendoli in subclip, generando miniature e caricando ogni parte su Telegram.

## Requisiti

- Python 3.x
- [Telethon](https://pypi.org/project/Telethon/)
- [ffmpeg-python](https://pypi.org/project/ffmpeg-python/)
- FFmpeg (deve essere installato separatamente, vedere [qui](https://ffmpeg.org/download.html) per le istruzioni di installazione)

## Installazione

1. Clona il repository:

   ```bash
   git clone https://github.com/alessandromasone/upload-telegram-video-bot.git
   cd upload-telegram-video-bot
   ```

2. Crea un ambiente virtuale e attivalo:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows usa `venv\Scripts\activate`
   ```

3. Installa le dipendenze richieste:

   ```bash
   pip install -r requirements.txt
   ```

4. Assicurati di avere FFmpeg installato sul tuo sistema. Puoi verificare l'installazione eseguendo:

   ```bash
   ffmpeg -version
   ```

## Configurazione

Modifica il file `main.py` in `config.py` per inserire le tue credenziali API di Telegram e il nome utente o l'ID del tuo canale:

   ```python
   API_ID = 'YOUR_API_ID'
   API_HASH = 'YOUR_API_HASH'
   BOT_TOKEN = 'YOUR_BOT_TOKEN'
   CHANNEL_USERNAME = 'YOUR_CHANNEL_USERNAME'  # Può essere l'username del canale con '@' o l'ID numerico del canale

   #...

   percorso_cartella = 'YOUR_FOLDER'
   ```

## Utilizzo

### Eseguire lo script principale

Lo script principale è `main.py`. Esegue l'analisi di una cartella specificata, carica i video su Telegram, li divide in subclip se superano una certa dimensione e genera miniature per ciascun subclip.

## Struttura del repository

- `main.py`: Script principale che gestisce l'intero processo.
- `upload_single.py`: Funzione per caricare un singolo video su Telegram.
- `generate_thumbnail.py`: Funzioni per generare miniature per i video.
- `create_subclips.py`: Funzioni per dividere un video in subclip.
- `config_example.py`: Esempio di file di configurazione. Da rinominare in `config.py` e modificare con le proprie credenziali.
- `uploaded_videos.log`: File di log per tenere traccia dei video caricati.
- `uploaded_subclips.log`: File di log per tenere traccia dei subclip caricati.