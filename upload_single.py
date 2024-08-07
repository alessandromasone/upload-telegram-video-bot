import os
import logging
from telethon import TelegramClient

# Configura il logger una sola volta
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('telethon').setLevel(logging.WARNING)  # Riduci i log di Telethon per migliorare la leggibilità

def upload_single_video(api_id, api_hash, bot_token, channel_username, video_path, thumbnail_path):
    """
    Carica un singolo video su un canale Telegram con una miniatura.
    
    Args:
        api_id (str): ID API di Telegram.
        api_hash (str): Hash API di Telegram.
        bot_token (str): Token del bot Telegram.
        channel_username (str): Nome utente o ID del canale Telegram.
        video_path (str): Percorso del video da caricare.
        thumbnail_path (str): Percorso della miniatura del video.
        
    Returns:
        bool: True se il video è stato caricato con successo, False altrimenti.
    """
    # Nome del file senza estensione per la didascalia
    file_name_without_extension = os.path.splitext(os.path.basename(video_path))[0]

    # Crea un'istanza del client
    client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    async def main():
        success = False
        try:
            logger.info(f"Inizio dell'upload del video '{video_path}' al canale '{channel_username}'.")

            # Invia il video al canale specificato
            await client.send_file(
                channel_username,
                video_path,
                caption=file_name_without_extension,
                thumb=thumbnail_path,  # Imposta la miniatura del video
                supports_streaming=True  # Abilita lo streaming
            )
            
            logger.info(f"Video '{video_path}' caricato con successo.")
            success = True

        except Exception as e:
            logger.error(f"Errore durante il caricamento del video '{video_path}': {e}", exc_info=True)

        finally:
            logger.info("Disconnessione completata.")
        
        return success

    # Avvia il client ed esegui la funzione principale
    with client:
        return client.loop.run_until_complete(main())
