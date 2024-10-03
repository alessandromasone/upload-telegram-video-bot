import os
import logging
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
import ffmpeg

# Configura il logger una sola volta
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('telethon').setLevel(logging.WARNING)  # Riduci i log di Telethon per migliorare la leggibilità

def progress(current, total):
    percent = (current / total) * 100
    logger.info(f"Caricamento: {percent:.2f}% completato ({current} su {total} bytes)")

def extract_video_metadata(video_path):
    """
    Estrae i metadati dal video utilizzando ffmpeg.
    
    Args:
        video_path (str): Percorso del video.
        
    Returns:
        dict: Un dizionario contenente i metadati del video.
    """
    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        raise ValueError("Nessun stream video trovato")
    
    duration = float(video_stream['duration'])
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    
    return {
        'duration': int(duration),
        'width': width,
        'height': height
    }

async def upload_video(client, channel_username, video_path, thumbnail_path, reply_to=None):
    """
    Carica un video su un canale Telegram con una miniatura e metadati estratti automaticamente.
    
    Args:
        client (TelegramClient): Istanza del client Telegram.
        channel_username (str): Nome utente o ID del canale Telegram.
        video_path (str): Percorso del video da caricare.
        thumbnail_path (str): Percorso della miniatura del video.
        reply_to (int, optional): ID del thread in cui caricare il video.
        
    Returns:
        bool: True se il video è stato caricato con successo, False altrimenti.
    """
    file_name_without_extension = os.path.splitext(os.path.basename(video_path))[0]
    success = False
    try:
        logger.info(f"Estrazione dei metadati dal video '{video_path}' in corso...")
        metadata = extract_video_metadata(video_path)
        
        logger.info(f"Inizio dell'upload del video '{video_path}' al canale '{channel_username}'.")

        # Invia il video al canale specificato con metadati
        await client.send_file(
            channel_username,
            video_path,
            caption=file_name_without_extension,
            thumb=thumbnail_path,
            supports_streaming=True,
            attributes=[
                DocumentAttributeVideo(
                    duration=metadata['duration'],
                    w=metadata['width'],
                    h=metadata['height'],
                    supports_streaming=True
                )
            ],
            progress_callback=progress,
            reply_to=reply_to  # Specifica il reply_to qui
        )
        
        logger.info(f"Video '{video_path}' caricato con successo.")
        success = True

    except Exception as e:
        logger.error(f"Errore durante il caricamento del video '{video_path}': {e}", exc_info=True)

    return success

def upload_single_video(api_id, api_hash, bot_token, channel_username, video_path, thumbnail_path, reply_to=None):
    """
    Carica un singolo video su un canale Telegram con una miniatura.
    
    Args:
        api_id (str): ID API di Telegram.
        api_hash (str): Hash API di Telegram.
        bot_token (str): Token del bot Telegram.
        channel_username (str): Nome utente o ID del canale Telegram.
        video_path (str): Percorso del video da caricare.
        thumbnail_path (str): Percorso della miniatura del video.
        reply_to (int, optional): ID del thread in cui caricare il video.
        
    Returns:
        bool: True se il video è stato caricato con successo, False altrimenti.
    """
    # Crea un'istanza del client
    client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    async def main():
        return await upload_video(client, channel_username, video_path, thumbnail_path, reply_to)

    # Avvia il client ed esegui la funzione principale
    with client:
        return client.loop.run_until_complete(main())

def upload_single_image(api_id, api_hash, bot_token, channel_username, image_path, reply_to=None):
    """
    Carica un singolo file immagine su un canale Telegram.
    
    Args:
        api_id (str): ID API di Telegram.
        api_hash (str): Hash API di Telegram.
        bot_token (str): Token del bot Telegram.
        channel_username (str): Nome utente o ID del canale Telegram.
        image_path (str): Percorso dell'immagine da caricare.
        reply_to (int, optional): ID del thread in cui caricare l'immagine.
        
    Returns:
        bool: True se l'immagine è stata caricata con successo, False altrimenti.
    """
    # Crea un'istanza del client
    client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    async def main():
        # Carica l'immagine sul canale
        try:
            await client.send_file(channel_username, image_path, reply_to=reply_to)  # Specifica il reply_to qui
            logger.info(f'Immagine caricata con successo: {image_path}')
            return True
        except Exception as e:
            logger.error(f'Errore nel caricamento dell\'immagine {image_path}: {e}', exc_info=True)
            return False

    # Avvia il client ed esegui la funzione principale
    with client:
        return client.loop.run_until_complete(main())
