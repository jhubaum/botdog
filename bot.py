import os, telegram, time, signal
import urllib.request as req

from classifier import is_hotdog

apikey = open("apikey").read()

def process_message(bot, msg):
    if len(msg.photo) > 0:
        f = bot.getFile(max(msg.photo, key=lambda p:p.file_size).file_id)
        img = req.urlopen(f.file_path).read()
        answer = "Hotdog" if is_hotdog(img) else "Not hotdog"
        bot.sendMessage(msg.chat.id, answer)
        
def handle_update(bot, update):
    process_message(bot, update.message)
    return int(update["update_id"])
    
if __name__ == "__main__":
    bot = telegram.Bot(apikey)

    offset = 0;
    while True:
        for update in bot.getUpdates(offset=offset, timeout=10.0):
            offset = max(handle_update(bot, update)+1, offset)
        time.sleep(0.1)
