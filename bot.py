import os, telegram, time, signal
import urllib.request as req

from classifier import is_hotdog

apikey = open("apikey").read()
intro_video_link = "https://www.youtube.com/watch?v=ACmydtFDTGs"

def process_command(bot, msg, command, *args):
    if command == "start" or command == "help":
        bot.sendMessage(msg.chat.id, intro_video_link);

def process_photo(bot, msg):
    bot.sendMessage(msg.chat.id, "Evaluating...")
    f = bot.getFile(max(msg.photo, key=lambda p:p.file_size).file_id)
    img = req.urlopen(f.file_path).read()
    answer = "Hotdog" if is_hotdog(img) else "Not hotdog"
    bot.sendMessage(msg.chat.id, answer)
        
def handle_update(bot, update):
    msg = update.message
    if msg.text != None and msg.text[0] == '/':
        argsparts = msg.text[1:].split(' ')
        process_command(bot, msg, argsparts[0], *argsparts[1:])
    else:
        process_photo(bot, msg)
        
    return int(update["update_id"])
    
if __name__ == "__main__":
    bot = telegram.Bot(apikey)

    offset = 0;
    while True:
        for update in bot.getUpdates(offset=offset, timeout=10.0):
            offset = max(handle_update(bot, update)+1, offset)
        time.sleep(0.1)
