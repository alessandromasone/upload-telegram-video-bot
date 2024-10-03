import os
import upload_single
import generate_thumbnail
import create_subclips

# Configura i parametri
API_ID = 'XXX'
API_HASH = 'XXX'
BOT_TOKEN = 'XXX'

# Percorsi dei file
LOG_FILE_VIDEOS = 'uploaded_videos.log'
LOG_FILE_SUBCLIPS = 'uploaded_subclips.log'
LOG_FILE_IMAGES = 'uploaded_images.log'  # Log file for images

# Username del canale (può essere il nome utente del canale con '@' o l'ID numerico del canale)
CHANNEL_USERNAME = -1234567890  # Sostituisci con il nome utente del tuo canale

# Specifica l'ID del thread in cui vuoi caricare
THREAD_ID = 1 # Sostituisci con il tuo thread ID

def file_grande(filepath, size_limit_gb):
    size_limit_bytes = size_limit_gb * 1024 * 1024 * 1024  # Convert GB to bytes
    return os.path.getsize(filepath) > size_limit_bytes

def video_caricato(filepath, log_file):
    if not os.path.exists(log_file):
        return False
    with open(log_file, 'r') as log:
        uploaded_files = log.read().splitlines()
    return filepath in uploaded_files

def immagine_caricata(filepath):
    return video_caricato(filepath, LOG_FILE_IMAGES)

def aggiungi_a_log(filepath, log_file):
    with open(log_file, 'a') as log:
        log.write(filepath + '\n')

def crea_cartelle_temporanee():
    os.makedirs('temp/subclips', exist_ok=True)
    os.makedirs('temp/thumbnails', exist_ok=True)

def processa_video_grande(file_path):
    subclips_folder = "temp/subclips/"
    thumbnails_folder = "temp/thumbnails/"
    
    # Crea subclip e thumbnail
    create_subclips.split_video(file_path, subclips_folder)
    generate_thumbnail.generate_thumbnails(subclips_folder, thumbnails_folder)
    
    # Ottieni l'elenco di tutti i file subclip
    subclip_files = [os.path.join(subclips_folder, f) for f in os.listdir(subclips_folder)]
    
    all_subclips_uploaded = True
    
    for subclip in subclip_files:
        subclip_name, _ = os.path.splitext(os.path.basename(subclip))
        thumbnail_path = os.path.join(thumbnails_folder, subclip_name + '_thumbnail.jpeg')
        
        if not video_caricato(subclip, LOG_FILE_SUBCLIPS):
            # Carica il video e il thumbnail del subclip singolarmente
            if upload_single.upload_single_video(API_ID, API_HASH, BOT_TOKEN, CHANNEL_USERNAME, subclip, thumbnail_path, THREAD_ID):
                aggiungi_a_log(subclip, LOG_FILE_SUBCLIPS)
            else:
                all_subclips_uploaded = False
    
    # Se tutti i subclip sono stati caricati con successo, aggiungi il video principale al log
    if all_subclips_uploaded:
        aggiungi_a_log(file_path, LOG_FILE_VIDEOS)

def processa_video_minore(file_path):
    thumbnail_path = "temp/thumbnail.jpeg"
    generate_thumbnail.generate_thumbnail_for_single_video(file_path, thumbnail_path)
    if upload_single.upload_single_video(API_ID, API_HASH, BOT_TOKEN, CHANNEL_USERNAME, file_path, thumbnail_path, THREAD_ID):
        aggiungi_a_log(file_path, LOG_FILE_VIDEOS)

def processa_immagine(file_path):
    if not immagine_caricata(file_path):
        if upload_single.upload_single_image(API_ID, API_HASH, BOT_TOKEN, CHANNEL_USERNAME, file_path, THREAD_ID):
            aggiungi_a_log(file_path, LOG_FILE_IMAGES)

def analizza_cartella(percorso):
    size_limit_gb = 2
    crea_cartelle_temporanee()
    
    for root, dirs, files in os.walk(percorso):
        nome_cartella = os.path.basename(root)
        print(f'Contenuto della cartella: {nome_cartella}')
        
        # Ordina le sottocartelle e i file in ordine alfabetico
        dirs.sort()
        files.sort()
        
        for file in files:
            file_path = os.path.join(root, file)
            if video_caricato(file_path, LOG_FILE_VIDEOS):
                print(f'  Video già caricato: {file}')
                continue
            
            try:
                # Gestisci i video
                if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):  # Aggiungi altri formati video se necessario
                    if video_caricato(file_path, LOG_FILE_VIDEOS):
                        print(f'  Video già caricato: {file}')
                        continue
                    
                    if file_grande(file_path, size_limit_gb):
                        print(f'  File maggiore: {file}')
                        processa_video_grande(file_path)
                    else:
                        print(f'  File minore: {file}')
                        processa_video_minore(file_path)

                # Gestisci le immagini
                elif file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Aggiungi altri formati immagine se necessario
                    print(f'  Immagine: {file}')
                    processa_immagine(file_path)
                    
            except Exception as e:
                print(f'  Errore nel processamento del file {file}: {e}')

# Specifica il percorso della cartella che vuoi analizzare
percorso_cartella = 'folder_name'
analizza_cartella(percorso_cartella)
