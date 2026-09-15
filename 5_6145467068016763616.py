#المطور السفاح المصري اليوتيوبر 
import requests
import json
import time
import datetime
import os

API_TOKEN = '8785295428:AAGpWOWAdl0BlGBaD6AJJOR4G2sFSj-xG1o' # توكنك 
SUDO_ID = '8781438214' # iD المطور 
BOT_ID = '8785295428' # iD بوتك
ANTI_SAFE_BOT_USERNAME = "@ALBOTDATABOT" # يوزر بوتك

DEV_BUTTONS = {
    'inline_keyboard': [
        [{'text': 'القناه', 'url': 'https://t.me/dataALKooool'}],
        [{'text': 'المطور', 'url': 'https://t.me/HAMo_ALKING_9'}]
    ]


def bot_request(method, datas={}):
    url = f"https://api.telegram.org/bot{API_TOKEN}/{method}"
    try:
        response = requests.post(url, data=datas)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in bot_request: {e}")
        return None

def get_chat_member_status(chat_id, user_id):
    response = bot_request('getChatMember', {'chat_id': chat_id, 'user_id': user_id})
    if response and response.get('ok'):
        return response['result']['status']
    return None

def load_file_content(filepath, default_value=""):
    try:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return default_value
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
        return default_value

def save_file_content(filepath, content):
    try:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file {filepath}: {e}")
        return False

def append_file_content(filepath, content):
    try:
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error appending to file {filepath}: {e}")
        return False

def delete_file(filepath):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {filepath}: {e}")
        return False

def handle_message(update):
    message = update.get('message')
    if not message:
        return

    message_id = message.get('message_id')
    chat_id = message.get('chat', {}).get('id')
    from_id = message.get('from', {}).get('id')
    text = message.get('text')
    chat_type = message.get('chat', {}).get('type')
    new_chat_member = message.get('new_chat_member')
    left_chat_member = message.get('left_chat_member')
    reply_to_message = message.get('reply_to_message')
    
    user_name = message.get('from', {}).get('first_name')
    user_username = message.get('from', {}).get('username')
    
    if reply_to_message:
        re_msgid = reply_to_message.get('message_id')
        re_id = reply_to_message.get('from', {}).get('id')
        re_user = reply_to_message.get('from', {}).get('username')
    else:
        re_msgid = None
        re_id = None
        re_user = None

    # Load settings
    settings_file = f"data/{chat_id}.txt"
    settings_lines = load_file_content(settings_file).split('\n')
    
    photo_lock = settings_lines[0] if len(settings_lines) > 0 else 'o'
    sticker_lock = settings_lines[1] if len(settings_lines) > 1 else 'o'
    contact_lock = settings_lines[2] if len(settings_lines) > 2 else 'o'
    doc_lock = settings_lines[3] if len(settings_lines) > 3 else 'o'
    fwd_lock = settings_lines[4] if len(settings_lines) > 4 else 'o'
    voice_lock = settings_lines[5] if len(settings_lines) > 5 else 'o'
    link_lock = settings_lines[6] if len(settings_lines) > 6 else 'o'
    audio_lock = settings_lines[7] if len(settings_lines) > 7 else 'o'
    video_lock = settings_lines[8] if len(settings_lines) > 8 else 'o'
    tag_lock = settings_lines[9] if len(settings_lines) > 9 else 'o'
    markdown_lock = settings_lines[10] if len(settings_lines) > 10 else 'o'
    bots_lock = settings_lines[11] if len(settings_lines) > 11 else 'o'
    
    group_status = get_chat_member_status(chat_id, from_id)
    bot_group_status = get_chat_member_status(chat_id, BOT_ID)
    
    groups_data = load_file_content("data/groups.txt").split('\n')
    groups = [g for g in groups_data if g]
    
    # Message count
    msgs_data = json.loads(load_file_content('msgs.json', '{}'))
    if 'msgs' not in msgs_data:
        msgs_data['msgs'] = {}
    if str(chat_id) not in msgs_data['msgs']:
        msgs_data['msgs'][str(chat_id)] = {}
    if str(from_id) not in msgs_data['msgs'][str(chat_id)]:
        msgs_data['msgs'][str(chat_id)][str(from_id)] = 0
    
    msgs_data['msgs'][str(chat_id)][str(from_id)] += 1
    save_file_content('msgs.json', json.dumps(msgs_data))
    
    user_message_count = msgs_data['msgs'][str(chat_id)][str(from_id)]

    commands = ['/add', '/lock photo', '/lock voice', '/lock audio', '/lock video', '/lock link', '/lock user', '/lock sticker', '/lock contact', '/lock doc', '/promote', '/ban', '/kick', '/pin', '/setname', "قفل الصور", "قفل البصمات", "قفل الصوت", "قفل الفيديو", "قفل الروابط", "قفل الجهات", "قفل الملفات", "حظر", "طرد", "رفع ادمن", "ضع اسم", "تثبيت", "/link", "الرابط"]
    if text in commands and bot_group_status != "administrator":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "🚫┇للأسف البوت ليس ادمن في المجموعة",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Start command in private chat
    if text == "/start" and chat_type == "private":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "💯¦ مـرحبآ آنآ اسمي بوت حمايه A.L 🎖\n"
                "💰¦ آختصـآصـي: حـمـايهہ‌‏ آلمـجمـوعآت \n"
                "📌¦ من السبام، التوجيه، التكرار والمخلفات.\n"
                "🚸¦ البوت خدمي ومتاح للكل \n"
                "👷🏽¦ فقط اضف البوت لمجموعتك وارفعه مشرف  \n"
                "  ثم ارسل تفعيل\n\n"
              
            ),
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
        
        # Log to sudo
        current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=3)))
        time_str = current_time.strftime("%H:%M")
        date_str = current_time.strftime("%Y/%m/%d")
        
        bot_request('sendMessage', {
            'chat_id': SUDO_ID,
            'text': (
                "شخص قام بالدخول إلى البوت\n"
                "ــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n"
                "ℓ☯️- المعرف الخاص بالعضو\n"
                f"ℓ🅿️- @{user_username}\n"
                "➖➖\n"
                "ℓ✳️- الاسم الخاص بالعضو\n"
                f"ℓ📳- {user_name}\n"
                "➖➖\n"
                "ℓ🚹- الايدي الخاص بالعضو\n"
                f"ℓ🆔- {from_id}\n"
                "➖➖\n"
                "ـ➖➖➖➖\n"
                f"⏰┇الساعة :: {time_str}\n"
                f"📆┇التاريخ :: {date_str}\n"
                "ـ➖➖➖➖\n"
                "📮"
            ),
            'parse_mode': "Markdown",
            'disable_web_page_preview': True
        })
        
        # Add to private chat members list
        priv_members = load_file_content("data/memomemb.txt").split('\n')
        if str(chat_id) not in priv_members:
            append_file_content("data/memomemb.txt", f"{chat_id}\n")

    # Bot added to group
    if new_chat_member and new_chat_member.get('id') == BOT_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "💯 مـرحبآ آنآ بوت حمايه\n"
                "¦ آختصـآصـي حمـآيهہ‏‏ آلمـجمـوعآت\n"
                "¦ مـن آلسـبآم وآلتوجيهہ‏‏ وآلتگرآر وآلخ...\n"
                
            ),
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Group protection based on locks
    if chat_type == "supergroup" and str(chat_id) in groups:
        if group_status != "creator" and group_status != "administrator" and from_id != SUDO_ID:
            if message.get('photo') and photo_lock == "l":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if message.get('voice') and voice_lock == "l":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if message.get('audio') and audio_lock == "l":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if message.get('video') and video_lock == "l":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if link_lock == "l" and text and requests.utils.urlparse(text).scheme in ['http', 'https', 't.me']: # Simplified link detection
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if tag_lock == "l" and text and ('@' in text or '#' in text):
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if message.get('document') and doc_lock == "l":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if message.get('sticker') and sticker_lock == "l":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if message.get('forward_from') and fwd_lock == "l":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if message.get('entities') and markdown_lock == "l":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})
            if new_chat_member and new_chat_member.get('is_bot') and bots_lock == "l":
                if new_chat_member.get('id') != BOT_ID:
                    bot_request('kickChatMember', {'chat_id': chat_id, 'user_id': new_chat_member.get('id')})

    # Admin commands
    if bot_group_status == "administrator":
        is_admin_or_creator = (group_status == "creator" or group_status == "administrator" or from_id == SUDO_ID)

        if is_admin_or_creator:
            if reply_to_message and text == "حذف":
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': re_msgid})

            if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and (text in ["/ban", "حظر", "/kick", "طرد"]):
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': (
                        f"¦ العضو » @{re_user}\n"
                        f"¦ الايدي » ( {re_id} )\n"
                        "¦ تم الحظر \n✓️"
                    ),
                    'reply_to_message_id': message_id,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
                bot_request('kickChatMember', {'chat_id': chat_id, 'user_id': re_id})

            if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and (text in ["/unban", "الغاء الحظر"]):
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': (
                        f"¦ العضو » @{re_user}\n"
                        f"¦ الايدي » ( {re_id} )\n"
                        "¦ تم الغاء الحظر \n✓️"
                    ),
                    'reply_to_message_id': message_id,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
                bot_request('unbanChatMember', {'chat_id': chat_id, 'user_id': re_id})

            if reply_to_message and (text == "/promote" or text == "رفع ادمن"):
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': (
                        f"¦ العضو » @{re_user}\n"
                        f"¦ الايدي » ( {re_id} )\n"
                        "¦ تمت ترقيته ليصبح ادمن \n✓️"
                    ),
                    'reply_to_message_id': message_id,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
                bot_request('promoteChatMember', {'chat_id': chat_id, 'user_id': re_id, 'can_manage_chat': True, 'can_delete_messages': True, 'can_invite_users': True, 'can_restrict_members': True, 'can_pin_messages': True, 'can_promote_members': False})

            if text and (text.startswith("/setname ") or text.startswith("ضع اسم ")):
                new_title = text.replace("/setname ", "").replace("ضع اسم ", "").strip()
                bot_request('setChatTitle', {'chat_id': chat_id, 'title': new_title})
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': f"تم تغيير اسم المجموعة إلى: {new_title}",
                    'reply_to_message_id': message_id,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })

            if reply_to_message and (text == "pin" or text == "تثبيت"):
                bot_request('pinChatMessage', {
                    'chat_id': chat_id,
                    'message_id': re_msgid
                })
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': "¦ أهلا  \n¦ تم تثبيت الرساله \n✓",
                    'reply_to_message_id': message_id,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })

            # Lock/Unlock commands (Refactored for brevity)
            lock_commands = {
                "/lock photo": "o\nl\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل الصور": "l\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open photo": "o\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح الصور": "o\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock sticker": "$photo_lock\nl\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل الملصقات": "$photo_lock\nl\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open sticker": "$photo_lock\no\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح الملصقات": "$photo_lock\no\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock contact": "$photo_lock\n$sticker_lock\nl\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل الجهات": "$photo_lock\n$sticker_lock\nl\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open contact": "$photo_lock\n$sticker_lock\no\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح الجهات": "$photo_lock\n$sticker_lock\no\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock doc": "$photo_lock\n$sticker_lock\n$contact_lock\nl\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل الملفات": "$photo_lock\n$sticker_lock\n$contact_lock\nl\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open doc": "$photo_lock\n$sticker_lock\n$contact_lock\no\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح الملفات": "$photo_lock\n$sticker_lock\n$contact_lock\no\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock fwd": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\nl\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل التوجيه": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\nl\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open fwd": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\no\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح التوجيه": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\no\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock voice": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\nl\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل البصمات": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\nl\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open voice": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\no\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح البصمات": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\no\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock link": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\nl\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل الروابط": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\nl\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open link": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\no\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح الروابط": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\no\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock audio": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\nl\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل الصوت": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\nl\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open audio": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\no\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح الصوت": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\no\n$video_lock\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock video": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\nl\n$tag_lock\n$markdown_lock\n$bots_lock",
                "قفل الفيديو": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\nl\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/open video": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\no\n$tag_lock\n$markdown_lock\n$bots_lock",
                "فتح الفيديو": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\no\n$tag_lock\n$markdown_lock\n$bots_lock",
                "/lock user": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\nl\n$markdown_lock\n$bots_lock",
                "قفل المعرفات": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\nl\n$markdown_lock\n$bots_lock",
                "/open user": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\no\n$markdown_lock\n$bots_lock",
                "فتح المعرفات": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\no\n$markdown_lock\n$bots_lock",
                "/lock mark": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\nl\n$bots_lock",
                "قفل الماركدون": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\nl\n$bots_lock",
                "/open mark": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\no\n$bots_lock",
                "فتح الماركدون": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\no\n$bots_lock",
                "/lock bots": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\nl",
                "قفل البوتات": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\nl",
                "/open bots": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\no",
                "فتح البوتات": "$photo_lock\n$sticker_lock\n$contact_lock\n$doc_lock\n$fwd_lock\n$voice_lock\n$link_lock\n$audio_lock\n$video_lock\n$tag_lock\n$markdown_lock\no",
                "/lock all": "l\nl\nl\nl\nl\nl\nl\nl\nl\nl\nl\nl", # All locks to 'l'
                "قفل الكل": "l\nl\nl\nl\nl\nl\nl\nl\nl\nl\nl\nl",
                "/open all": "o\no\no\no\no\no\no\no\no\no\no\no", # All locks to 'o'
                "فتح الكل": "o\no\no\no\no\no\no\no\no\no\no\no",
                "قفل المتحرك": f"{photo_lock}\n{sticker_lock}\n{contact_lock}\n{doc_lock}\n{fwd_lock}\nl\n{link_lock}\n{audio_lock}\n{voice_lock}\n{tag_lock}\n{markdown_lock}\n{bots_lock}\n1", # assuming 'bsma1' and 'cha1' were placeholders
                "فتح المتحرك": f"{photo_lock}\n{sticker_lock}\n{contact_lock}\n{doc_lock}\n{fwd_lock}\no\n{link_lock}\n{audio_lock}\n{voice_lock}\n{tag_lock}\n{markdown_lock}\n{bots_lock}\no",
                "قفل التاك": f"{photo_lock}\n{sticker_lock}\n{contact_lock}\n{doc_lock}\n{fwd_lock}\n{voice_lock}\n{link_lock}\n{audio_lock}\n{video_lock}\nl\n{markdown_lock}\n{bots_lock}",
                "فتح التاك": f"{photo_lock}\n{sticker_lock}\n{contact_lock}\n{doc_lock}\n{fwd_lock}\n{voice_lock}\n{link_lock}\n{audio_lock}\n{video_lock}\no\n{markdown_lock}\n{bots_lock}",
                "قفل الدردشه": f"{photo_lock}\n{sticker_lock}\n{contact_lock}\n{doc_lock}\n{fwd_lock}\n{voice_lock}\n{link_lock}\n{audio_lock}\n{video_lock}\n{tag_lock}\n{markdown_lock}\n{bots_lock}\nl",
                "فتح الدردشه": f"{photo_lock}\n{sticker_lock}\n{contact_lock}\n{doc_lock}\n$fwd_lock\n{voice_lock}\n{link_lock}\n{audio_lock}\n{video_lock}\n{tag_lock}\n{markdown_lock}\n{bots_lock}\no"
            }

            for cmd, new_settings in lock_commands.items():
                if text == cmd:
                    new_settings_formatted = new_settings.replace('$photo_lock', photo_lock).replace('$sticker_lock', sticker_lock).replace('$contact_lock', contact_lock).replace('$doc_lock', doc_lock).replace('$fwd_lock', fwd_lock).replace('$voice_lock', voice_lock).replace('$link_lock', link_lock).replace('$audio_lock', audio_lock).replace('$video_lock', video_lock).replace('$tag_lock', tag_lock).replace('$markdown_lock', markdown_lock).replace('$bots_lock', bots_lock)
                    
                    save_file_content(settings_file, new_settings_formatted)
                    
                    status = "قفل" if "lock" in cmd or "قفل" in cmd else "فتح"
                    item = cmd.replace("/lock ", "").replace("/open ", "").replace("قفل ", "").replace("فتح ", "").replace("ال", "").replace("ات", "").replace(" ", "")
                    
                    bot_request('sendMessage', {
                        'chat_id': chat_id,
                        'text': f"🙋🏼‍♂️¦ أهلا عزيزي \n📡¦ تم {status} ال{item} \n✓",
                        'reply_to_message_id': message_id,
                        'parse_mode': 'MARKDOWN',
                        'disable_web_page_preview': True,
                        'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                    break # Exit loop after handling command

            # Commands menu
            if text == "الاوامر":
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': (
                        "❂\n\n"
                        " ‌‌‏❋¦ مـسـآرت آلآوآمـر آلعآمـهہ‌‏ ⇊\n\n"
                        "👨‍⚖️¦ م1 » آوآمـر آلآدآرهہ‌‏\n"
                        "📟¦ م2 » آوآمـر آعدآدآت آلمـجمـوعهہ‌‏\n"
                        "🛡¦ م3 » آوآمـر آلحمـآيهہ‌‏\n"
                        "🕹¦ م المطور »  آوآمـر آلمـطـور\n\n"
                        
                    ),
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })

            # Show group settings
            if text in ["/نذنبنينين", "/setting", "/setting" + ANTI_SAFE_BOT_USERNAME, "تبنبنبنن"]:
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': (
                        "➖➖➖\n"
                        "👮🏾¦ اعدادات المجموعه : \n\n\n"
                        "✔️¦ مقفول » l\n"
                        "✖️¦ مفتوح » o\n\n"
                        "➖➖➖\n\n"
                        f"📸¦ الصور : {photo_lock}\n"
                        f"🀄️¦ الملصقات : {sticker_lock}\n\n"
                        f"📹¦ الفيديو : {video_lock}\n"
                        f"📡¦ الروابط :  {link_lock}\n\n"
                        f"☎️¦ الجهات : {contact_lock}\n"
                        f"🗂¦ الملفات :  {doc_lock}\n\n"
                        f"↩️¦ التوجيه : {fwd_lock}\n"
                        f"🎙¦ البصمات : {voice_lock}\n\n"
                        f"🔊¦ الصوت : {audio_lock}\n"
                        f"Ⓜ️¦ المعرف : {tag_lock}\n\n"
                        f"🔖¦ الماركدون : {markdown_lock}\n"
                        f"📟¦ البوتات : {bots_lock}\n\n"
                        "➖➖➖\n"
                        
                    ),
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        else: # Not admin/creator
            if text in commands and text not in ["/link", "الرابط"]: # Specific commands restricted to admins
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': "📡¦ هذا الامر يخص الادمنيه فقط  🚶",
                    'reply_to_message_id': message_id,
                    'parse_mode': 'MARKDOWN',
                    'disable_web_page_preview': True,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
    
    # Activation command
    if bot_group_status == "administrator" and (group_status == "creator" or group_status == "administrator"):
        if text in ["/add", "/add" + ANTI_SAFE_BOT_USERNAME, "تفعيل"]:
            if str(chat_id) not in groups:
                append_file_content("data/groups.txt", f"{chat_id}\n")
                save_file_content(settings_file, "o\no\no\no\nl\no\nl\no\no\nl\no\no") # Default locks on activation
                
                chat_title = message.get('chat', {}).get('title', 'N/A')
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': (
                        "📮¦ تـم تـفـعـيـل الـمـجـمـوعـه ✓️ \n"
                        "👨🏽‍🔧¦¦ وتم رفع جمـيع آلآدمـنيهہ‌‌‏ آلگروب بآلبوت \n✓"
                    ),
                    'reply_to_message_id': message_id,
                    'parse_mode': 'MARKDOWN',
                    'disable_web_page_preview': True,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })

                # Log to sudo for activation
                current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=3)))
                time_str = current_time.strftime("%H:%M")
                date_str = current_time.strftime("%Y/%m/%d")
                
                chat_members_count = bot_request('getChatMembersCount', {'chat_id': chat_id})
                members_count = chat_members_count['result'] if chat_members_count and chat_members_count.get('ok') else 'N/A'
                
                export_link_response = bot_request('exportChatInviteLink', {'chat_id': chat_id})
                invite_link = export_link_response['result'] if export_link_response and export_link_response.get('ok') else 'N/A'

                bot_request('sendMessage', {
                    'chat_id': SUDO_ID,
                    'text': (
                        "\n👮🏽¦ قام شخص بتفعيل البوت ...\n"
                        "ــــــــــــــــــــــــــــــــــــــــــ\n"
                        "📑¦ معلومات المجموعه\n"
                        f"🗯¦ الاسم •⊱ {chat_title} ⊰• \n"
                        f"📊¦ رابط المجموعة • {invite_link} •\n"
                        f"📛¦ الايدي •⊱{chat_id}⊰•\n"
                        f"🙋🏻‍♂¦ ألاعـضـاء •⊱{{{members_count}}}⊰• \n"
                        "ــــــــــــــــــــــــــــــــــــــــــ\n"
                        "⚖️¦ معلومات الشخص \n"
                        f"👨🏽‍💻¦ الاسـم •⊱{{ {user_name} }}⊰•\n\n"
                        f"🎟¦ الـمعرف  •⊱ @{user_username} ⊰•\n"
                        "ــــــــــــــــــــــــــــــــــــــــــ\n"
                        f"⏱¦ الساعه •⊱ {time_str} ⊰•\n"
                        f"📆¦ التاريخ •⊱ {date_str} ⊰•\n"
                    ),
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
            elif str(chat_id) in groups:
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': "🎗¦ المجموعه بالتأكيد ✓️ تم تفعيلها",
                    'reply_to_message_id': message_id,
                    'parse_mode': 'MARKDOWN',
                    'disable_web_page_preview': True,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })

    # Group counts (requires access to groups.txt)
    if text == "المجموعات":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"📮¦ عدد المجموعات المفعلة » {len(groups)}  ➼",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Broadcast (SUDO only)
    if text == "اذاعه" and from_id == SUDO_ID:
        save_file_content("mode.txt", "bc")
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📭¦ حسننا الان ارسل الكليشه للاذاعه للمجموعات \n🔛",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    mode = load_file_content("mode.txt")
    if text != "اذاعه" and mode == "bc" and from_id == SUDO_ID:
        for group_id in groups:
            if group_id:
                bot_request('sendMessage', {
                    'chat_id': int(group_id),
                    'text': text,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        delete_file("mode.txt")

    # My Status command
    if text == "موقعي":
        rank = "عضو"
        if from_id == SUDO_ID:
            rank = "مطور اساسي 👨🏻‍⚕️"
        elif group_status == "creator":
            rank = "المنشىء 👷🏼‍⚕️"
        elif group_status == "administrator":
            rank = "ادمن في البوت 👨🏼‍🎓🏼‍⚕️"
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "👨🏽‍🔧¦ اهـلا بـك عزيزي في معلوماتك 🥀 \n"
                "ـ.——————————\n"
                f"🗯¦ الاســم •⊱{{{user_name}}}⊰•\n"
                f"💠¦ المعرف •⊱ @{user_username} ⊰•\n"
                f"⚜️¦ الايـدي •⊱ {{ {from_id} }} ⊰•\n"
                f"🚸¦ رتبتــك •⊱ {rank} ⊰•\n"
                f"🔰¦ ــ •⊱ {{ {chat_id} }} ⊰•\n"
                "ـ.——————————\n"
               
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # My Info with Photo (Various placeholders for original code, consolidating)
    if text in ["تبنيمين", "خلمبةذ", "بمكينذو", "نبنينسن"]:
        caption_text = ""
        user_profile_photos = bot_request("getUserProfilePhotos", {"user_id": from_id, "limit": 1, "offset": 0})
        file_id = user_profile_photos["result"]["photos"][0][0]["file_id"] if user_profile_photos and user_profile_photos.get("ok") and user_profile_photos["result"]["photos"] else None
        
        if from_id == SUDO_ID:
            caption_text = (
                f"👤¦ أســمـك •⊱ {{  {user_name}  }} •\n"
                f"🎟¦ ايديــك •⊱ {from_id} ⊰•\n"
                f"🎫¦ مـعرفك •⊱ @{user_username} ⊰•\n"
                f"📡¦ رتبتـــك •⊱ مطور اساسي 👨🏻‍✈️ ⊰•\n"
                f"💬¦ رسائلك • {{ *{user_message_count}* }} •\n"
                "➖"
            )
        elif group_status == "creator" and from_id != SUDO_ID:
            caption_text = (
                f"👤¦ أســمـك •⊱ {{  {user_name}  }} •\n"
                f"🎟¦ ايديــك •⊱ {from_id} ⊰•\n"
                f"🎫¦ مـعرفك •⊱ @{user_username} ⊰•\n"
                f"📡¦ رتبتـــك •⊱ المنشىء 👷🏽 ⊰•\n"
                f"💬¦ رسائلك • {{ *{user_message_count}* }} •\n"
                "➖"
            )
        elif group_status == "administrator" and from_id != SUDO_ID:
            caption_text = (
                f"👤¦ أســمـك •⊱ {{  {user_name}  }} •\n"
                f"🎟¦ ايديــك •⊱ {from_id} ⊰•\n"
                f"🎫¦ مـعرفك •⊱ @{user_username} ⊰•\n"
                f"📡¦ رتبتـــك •⊱ ادمن في البوت 👨🏼‍🎓 ⊰•\n"
                f"💬¦ رسائلك • {{ *{user_message_count}* }} •\n"
                "➖"
            )
        elif group_status == "member" and from_id != SUDO_ID:
            caption_text = (
                f"👤¦ أســمـك •⊱ {{  {user_name}  }} •\n"
                f"🎟¦ ايديــك •⊱ {from_id} ⊰•\n"
                f"🎫¦ مـعرفك •⊱ @{user_username} ⊰• \n"
                f"📡¦ رتبتـــك •⊱ فقط عضو 🙍🏼‍♂️ ⊰•\n"
                f"💬¦ رسائلك • {{ *{user_message_count}* }} •\n"
                "➖"
            )

        if file_id:
            bot_request("sendPhoto", {
                "chat_id": chat_id,
                "caption": caption_text,
                'parse_mode': "MarkDown",
                "photo": file_id,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request("sendMessage", {
                "chat_id": chat_id,
                "text": "🚸¦ لا يوجد صوره في بروفايلك ...!\n" + caption_text,
                'parse_mode': "MarkDown",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # 'صورتي' and 'hjvdgh' commands (requires local file storage and a web server, which is simplified here)
    if text in ["صورتي", "hjvdgh", "dgvxx"]:
        user_profile_photos = bot_request("getUserProfilePhotos", {"user_id": from_id, "limit": 1, "offset": 0})
        if user_profile_photos and user_profile_photos.get("ok") and user_profile_photos["result"]["photos"]:
            file_id = user_profile_photos["result"]["photos"][0][-1]["file_id"] # Get largest size
            
            # This part of the original PHP code relies on downloading the file and serving it from a web server.
            # In a webhookless Python bot, you would usually send the file_id directly.
            # If the image truly needs to be re-uploaded from a web host, that external hosting setup is outside the bot.
            # For direct sending:
            caption = ""
            if text in ["hjvdgh", "dgvxx"]:
                caption = (
                    f"👤¦ اسمـك » {user_name}\n"
                    f"🎫¦ معرفك » @{user_username}\n"
                    f"🏷¦ ايديك  » {from_id}\n"
                    f"📨¦ رسائل المجموعة »  {message_id}\n"
                    f"🎫¦ ايدي المجموعة » {chat_id}\n"
                    "➖"
                )
            
            bot_request("sendPhoto", {
                'chat_id': chat_id,
                "photo": file_id,
                'caption': caption,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "لا توجد صورة شخصية لعرضها.",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })


    # Link command
    if text == "/link" or text == "الرابط":
        export_link_response = bot_request("exportChatInviteLink", {"chat_id": chat_id})
        if export_link_response and export_link_response.get("ok"):
            link = export_link_response["result"]
            chat_title = message.get('chat', {}).get('title', 'N/A')
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "🔖¦رابـط مجمـــوعة: 💯\n"
                    f"🌿¦ {chat_title} :\n\n"
                    f"{link}"
                ),
                'disable_web_page_preview': True,
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
             bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "حدث خطأ عند جلب رابط المجموعة. تأكد من أن البوت مسؤول ويمكنه دعوة المستخدمين.",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Kick bots on new chat member
    if new_chat_member and new_chat_member.get('is_bot') and new_chat_member.get('id') != BOT_ID:
        if group_status == "member": # Original logic was only for members
            bot_request('kickChatMember', {
                'chat_id': chat_id,
                'user_id': new_chat_member.get('id')
            })
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    f"👤¦ آلعضـو : @{new_chat_member.get('username')}\n"
                    f"👤¦ الايدي : {new_chat_member.get('id')} \n"
                    "🚫¦ مـمـنوع آضـآفهہ آلبوتآت \n"
                    "📛¦ تم طـرد آلبوت \n✘"
                ),
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Delete messages by count (SUDO only)
    if text and text.startswith("مسح ") and from_id == SUDO_ID:
        try:
            count_to_delete = int(text.split("مسح ")[1])
            for h in range(message_id, message_id - count_to_delete, -1):
                bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': h})
        except ValueError:
            pass # Ignore if not a valid number

    # Edited messages (Original PHP just sends empty message, Python sends placeholder)
    edited_message = update.get('edited_message')
    if edited_message:
        bot_request('sendMessage', {
            'chat_id': edited_message.get('chat', {}).get('id'),
            'text': "تم تعديل رسالة.",
            'reply_to_message_id': edited_message.get('message_id'),
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Reply with ID
    if reply_to_message and (text == "ايدي" or text == "ايديه"):
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f" {re_id} ",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Command menus (m1, m2, m3)
    if text == "م1":
        if is_admin_or_creator:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "•⊱ {  آوآمر الرفع والتنزيل  } ⊰•\n\n\n"
                    "📿¦ رفع ادمن ‿ تنزيل ادمن  \n\n \n"
                    "⦅آوآمـر آلحظـر وآلطــرد وآلتقييـد  ⦆\n      \n"
                    "🔱¦ حظر (بالرد/بالمعرف) •⊱ لحظر العضو\n"
                    "⚜¦ طرد ( بالرد/بالمعرف) •⊱ لطرد العضو \n"
                    "🔅¦ كتم (بالرد/بالمعرف) •⊱ لكتم العضو \n"
                    "🌀¦ تقييد (بالرد/بالمعرف) •⊱ لتقييد العضو\n"
                    "🚸¦ الغاء الحظر (بالرد/بالمعرف) •⊱ لالغاء الحظر \n"
                    "🔆¦ الغاء الكتم (بالرد/بالمعرف) •⊱ لالغاء الكتم \n"
                    "〰¦ الغاء التقييد (بالرد/بالمعرف) •⊱ لالغاء تقييد العضو \n\n"
                    
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "📡¦ هذا الامر يخص الادمنيه فقط  🚶",
                'reply_to_message_id': message_id,
                'parse_mode': 'MARKDOWN',
                'disable_web_page_preview': True,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    if text == "م2":
        if is_admin_or_creator:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "👨🏽‍✈️¦  اوامر الوضع للمجموعه ::\n\n"
                    "📮¦ـ➖➖➖➖➖  \n"
                    "💭¦ ضع اسم  ↜ لوضع اسم المحموعة\n  \n"
                    "💭¦ الـرابـط :↜  لعرض الرابط  \n"
                    "📮¦ـ➖➖➖➖➖\n\n"
                    "👨🏽‍💻¦  اوامر رؤية الاعدادات ::\n\n"
                    "🗯¦ الادمنيه : لعرض  الادمنيه \n"
                    "🗯¦ المطور : لعرض معلومات المطور \n"
                    "🗯¦ موقعي :↜لعرض معلوماتك  \n\n"
                    "➖➖➖➖➖➖➖\n"
                    
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "📡¦ هذا الامر يخص الادمنيه فقط  🚶",
                'reply_to_message_id': message_id,
                'parse_mode': 'MARKDOWN',
                'disable_web_page_preview': True,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    if text == "تبنيمسوسنسن":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "⚡️ اوامر حماية المجموعه ⚡️\n"
                "🗯|ـ➖➖➖➖\n"
                "🗯|️ قفل ~ فتح :  الصوت\n"
                "🗯| قفل ~ فتح :  الــفيديو\n"
                "🗯| قفل ~ فتح :  الـصــور \n"
                "🗯| قفل ~ فتح :  الملصقات\n"
                "🗯| قفل ~ فتح : الروابط\n"
                "🗯| قفل ~ فتح : البوتات\n"
                "🗯| ️قفل ~ فتح : المعرفات\n"
                "🗯|| قفل ~ فتح :  التوجيه\n"
                "🗯| قفل ~ فتح : الجهات \n"
                "🗯| قفل ~ فتح : الملفات\n"
                " 🗯| قفل ~ فتح : الماركدون\n"
                " 🗯| قفل ~ فتح : البصمات\n"
                "🔅|ـ➖➖➖➖➖\n"
                
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    if text == "م3":
        if is_admin_or_creator:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "⚡️ اوامر حماية المجموعه ⚡️\n"
                    "🗯¦ـ➖➖➖➖\n"
                    "🗯¦️ قفل «» فتح •⊱ البصمات ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الــفيديو ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الفيديو ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الـصــور ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الملصقات ⊰•\n\n"
                    "🗯¦ قفل «» فتح •⊱ المتحركه ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الدردشه ⊰•\n\n"
                    "🗯¦ قفل «» فتح •⊱ الروابط ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ التاك ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ البوتات ⊰•\n"
                    "🗯¦ ️قفل «» فتح •⊱ المعرفات ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ البوتات  ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ التوجيه ⊰•\n\n"
                    "🗯¦ قفل «» فتح •⊱ الجهات ⊰•\n"
                    "🗯¦ قفل «» فتح •⊱ الــكـــل ⊰•\n"
                    "🔅¦ـ➖➖➖➖➖\n"
                    "🗯┇ راسلني للاستفسار 💡↭@ "
                ),
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "📡¦ هذا الامر يخص الادمنيه فقط  🚶",
                'reply_to_message_id': message_id,
                'parse_mode': 'MARKDOWN',
                'disable_web_page_preview': True,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Sudo menu
    if text == "م المطور" and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "🎖¦ آهہ‏‏لآ عزيزي آلمـطـور 🍃\n"
                "💰¦ آنتهہ‏‏ آلمـطـور آلآسـآسـي هہ‏‏نآ 🛠\n"
                "...\n\n"
                "🚸¦ تسـتطـيع‏‏ آلتحگم بگل آلآوآمـر آلمـمـوجودهہ‏‏\n\n"
                "🔅¦ تفعيل : لتفعيل البوت \n"
                "🔅¦ اذاعه : لنشر كلمه لكل المجموعات\n"
                "🔅¦ استخدم /admin في خاص البوت فقط : لعرض كيبود الخاص بك 💯 \n"
                "🔅¦ تحديث: لتحديث ملفات البوت\n"
                "🔅¦ غادر : لمغادرة  البوت \n"
                "🔅¦ حظر عام : لحظر العضو من البوت عام\n"
                "🔅¦ـ➖➖➖➖➖\n"
                
            ),
            'parse_mode': 'MarkDown',
            'disable_web_page_preview': True,
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif text == "م المطور" and from_id != SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "🔅¦ للمطور الاساسي فقط  🎖",
            'reply_to_message_id': message_id,
            'parse_mode': 'MARKDOWN',
            'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Broadcast restricted
    if text == "اذاعه" and from_id != SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📛¦ هذا الامر يخص {المطور} فقط  \n🚶",
            'reply_to_message_id': message_id,
            'parse_mode': 'MARKDOWN',
            'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Update command (SUDO only)
    if text == "تحديث ♻️" and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "🎖\n🗂¦ تم تحديث الملفات\n√",
            'parse_mode': 'MarkDown',
            'disable_web_page_preview': True,
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif text == "تحديث ♻️" and from_id != SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📛¦ هذا الامر يخص {المطور الاساسي} فقط  \n🚶",
            'reply_to_message_id': message_id,
            'parse_mode': 'MARKDOWN',
            'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Dev Contact (Replaced with@HAMo_ALKING_9)
    if text == 'ارردبلتود' or text == "نكتلقفبظ":
        bot_request('sendContact', {
            'chat_id': chat_id,
            'phone_number': "+9647815864486", # Original number retained
            'first_name': "@avetaar", # Replaced
            'last_name': "ٵڵٵڼـࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲٞ࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫҉ৡـࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲٞ࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫ैۖـښـࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲٞ࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫࣫҉ৡـࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲࣲैۖـٱڹ 📿 ٵلڕجُيُـُैُۖـُـُـُـُࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣧࣧࣧࣧࣧࣧࣧࣧࣧࣧࣧۖـُـُـُـُࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣩࣧࣧࣧࣧࣧࣧࣧࣧࣧࣧࣧۖـم",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # My Rank
    if text == "رتبتي":
        if group_status == "creator":
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "🎫¦ رتبتك » المنشىء 🏌🏻\n🌿",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif group_status == "administrator":
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "🎫¦ رتبتك » ادمن في البوت 🎖\n🌿",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif group_status == "member":
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "🎫¦ رتبتك » فقط عضو 🙍🏼‍♂️\n🌿",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # "انجب" command responses
    if text == "انجب":
        if group_status == "creator":
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "حاظر تاج راسي انجبيت 😇",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif group_status == "administrator":
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "فوك ما مصعدك ادمن و تكلي انجب 😏 ",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif group_status == "member":
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "انجب انته لا تندفر 😒",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # 'كله' and 'كول' commands
    if text and text.startswith("كله ") and reply_to_message:
        reply_text = text.replace("كله ", "")
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': reply_text,
            'reply_to_message_id': re_msgid, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    if text and text.startswith("كول "):
        say_text = text.replace("كول ", "")
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': say_text, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Admin keyboard in private chat (SUDO only)
    if text == '/admin' and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                '🎖¦ آهہ‏‏لآ عزيزي آلمـطـور 🍃\n'
                '💰¦ آنتهہ‏‏ آلمـطـور آلآسـآسـي هہ‏‏نآ 🛠\n'
                '...\n\n'
                '🚸¦ تسـتطـيع‏‏ آلتحگم بگل آلآوآمـر آلمـمـوجودهہ‏‏ بآلگيبورد\n'
                '⚖️¦ فقط آضـغط ع آلآمـر آلذي تريد تنفيذهہ‏‏'
            ),
            'reply_markup': json.dumps({
                'keyboard': [
                    [{'text': '🆔¦ ايديك •'}],
                    [{'text': '💯¦ المشتركين •'}, {'text': '☑️¦ المجموعات •'}],
                    [{'text': '🚸¦ اسمك •'}],
                    [{'text': '💢¦ معرفك •'}],
                    [{'text': '📊¦ الاحصائيات •'}],
                    [{'text': '🔂¦ اذاعة •'}],
                    [{'text': '🛠¦ المطور •'}],
                    [{'text': '📡¦ قناة المطور •'}, {'text': '🛠¦ المساعدة •'}],
                ],
                'resize_keyboard': True
            })
        })

    # Broadcast with admin keyboard (SUDO only)
    if text == "🔂¦ اذاعة •" and from_id == SUDO_ID:
        save_file_content("mode.txt", "bc_key") # Use a different mode for keyboard broadcast
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📭¦ حسننا الان ارسل الكليشه للاذاعه للمجموعات \n🔛",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    if text != "🔂¦ اذاعة •" and mode == "bc_key" and from_id == SUDO_ID:
        for group_id in groups:
            if group_id:
                bot_request('sendMessage', {
                    'chat_id': int(group_id),
                    'text': text,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        delete_file("mode.txt")

    # Group count from keyboard
    if text == "☑️¦ المجموعات •":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"📮¦ عدد المجموعات المفعلة » {len(groups)}  ➼",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # My info from keyboard
    if text == "🆔¦ ايديك •":
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f" {from_id} ",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    if text == "🚸¦ اسمك •":
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f" {user_name} ",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    if text == "💢¦ معرفك •":
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f" @{user_username} ",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Dev info from keyboard
    if text == "🛠¦ المطور •" and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f" 🏌🏻¦ مـطـور البوت : @{user_username} 👨🏽‍🔧 ",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Subscribers count (SUDO only)
    if text == "💯¦ المشتركين •" and from_id == SUDO_ID:
        members_pv = load_file_content("data/memomemb.txt").split('\n')
        members_pv = [m for m in members_pv if m]
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"💯¦ عدد مشتركين البوت :- {{ {len(members_pv)} }}",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Stats from keyboard
    if text == "📊¦ الاحصائيات •":
        members_pv = load_file_content("data/memomemb.txt").split('\n')
        members_pv = [m for m in members_pv if m]
        
        groups_list = load_file_content("data/groups.txt").split('\n')
        groups_list = [g for g in groups_list if g]
        
        left_groups_list = load_file_content("data/left.txt").split('\n')
        left_groups_list = [g for g in left_groups_list if g]

        active_groups_count = len(groups_list)
        left_groups_count = len(left_groups_list)
        correct_groups_count = active_groups_count - left_groups_count # Logic from original code

        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                " الاحصائيات : 📈 \n\n"
                f"📊¦ عدد المجموعات المفعله : {active_groups_count} \n"
                f"📊¦ عدد المشتركين في البوت : {len(members_pv)}\n"
                "📡 "
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Dev Channel from keyboard (Replaced with @Vl_HI)
    if text == "📡¦ قناة المطور •":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "🛠¦   قناة مـطـور الملف : @Vl_HI☑️ ",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Help from keyboard (Replaced with@HAMo_ALKING_9)
    if text == "🛠¦ المساعدة •":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "💯¦ للمساعدة او اي أراء او افكار تواصل مع مطور الملف@HAMo_ALKING_9 √",
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Minimum group members check (original variable names `API_KEY` and `admin` were reused in PHP, mapping to `API_TOKEN` and `SUDO_ID` in Python for consistency)
    minimum_members_file = "dev_start.txt"
    dev_start_limit = load_file_content(minimum_members_file, "0")
    try:
        dev_start_limit = int(dev_start_limit.strip())
    except ValueError:
        dev_start_limit = 0 # Default if file content is not an int

    if from_id == SUDO_ID:
        if text and text.startswith("العدد المقبول "):
            new_limit = text.replace("العدد المقبول ", "").strip()
            save_file_content(minimum_members_file, new_limit)
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "تم الحفظ",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # The next block about leaving group if member count is low is based on `homsi` which is `group_status` in Python, and `ALOOSH080` which is `chat_members_count`.
    if group_status in ["creator", "administrator"] and chat_type == "supergroup":
        chat_members_count_response = bot_request('getChatMembersCount', {'chat_id': chat_id})
        current_members_count = chat_members_count_response['result'] if chat_members_count_response and chat_members_count_response.get('ok') else 0

        if current_members_count <= dev_start_limit:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': (
                    "عذرا لا يمكنني حماية هذا المجموعة\n"
                    f"لأن عدد أعضائها أقل من【 {dev_start_limit}】\n"
                    f"عدد أعضاء المجموعة الحالي:【 {current_members_count} 】"
                ),
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('leaveChat', {'chat_id': chat_id})


    # Welcome new member
    if new_chat_member and not new_chat_member.get('is_bot'):
        new_member_id = new_chat_member.get('id')
        new_member_name = new_chat_member.get('first_name')
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                f"<a href='tg://user?id={new_member_id}'>{new_member_name}</a>\n\n"
                "🔖¦ مرحباً عزيزي\n"
                "🔖¦ نورت المجموعة \n"
                "💂🏼‍♀️"
            ),
            'reply_to_message_id': message_id,
            'parse_mode': "html",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Source command (Replaced with @Vl_HI)
    if text == "السورس":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "┇ تنصـيب سـورس @Vl_HI  🔎\n\n"
                " ⇓⇓⇓ \n\n"
                "`git clone https://github.com/TH3BS/BOSS.git ;cd BOSS;chmod +x ins;./ins`\n\n"
                "» فقط أضغط على الكود ☝️ ليتم النسخ \n"
                "» ثم الصقه بالترمنال وانتر تتنظر يتنصب \n"
                "» بعدهہ‌‏آ يطـلب مـعلومـآت بآلترمـنآل .\n"
                "» تدخل مـعلومـآتگ مـن توگن ومـعرفگ \n"
                "» وسـوف يعمـل آلبوت بالسـگرين تلقآئيآ ...\n\n"
                "💭┇ قناة السورس ☜ @Vl_HI"
            ),
            'reply_to_message_id': message_id,
            'parse_mode': 'MARKDOWN',
            'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Time command
    if text in ["الساعة", "الزمن", "الساعه", "الوقت"]:
        current_time = datetime.datetime.now(datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=3)))
        time_str = current_time.strftime("%H:%M")
        ampm = "ص" if current_time.strftime("%p") == "AM" else "م"
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"🎖*{time_str} {ampm}*",
            'parse_mode': 'MarkDown',
            'disable_web_page_preview': True,
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # File management (SUDO only)
    if from_id == SUDO_ID:
        if text == 'الملف':
            # This requires the script itself to be sent, or a specific file
            # Assuming it meant "the current script file" as in PHP's __FILE__
            try:
                with open(__file__, 'rb') as f:
                    bot_request('sendDocument', {
                        'chat_id': chat_id,
                        'document': f # This will work with python-telegram-bot or a direct API POST with 'files'
                    })
            except Exception as e:
                bot_request('sendMessage', {'chat_id': chat_id, 'text': f"خطأ في إرسال الملف: {e}"})

        if text and text.startswith('جلب ملف '):
            filepath_to_send = text.replace('جلب ملف ', '').strip()
            if os.path.exists(filepath_to_send) and os.path.isfile(filepath_to_send):
                try:
                    with open(filepath_to_send, 'rb') as f:
                        bot_request('sendDocument', {
                            'chat_id': chat_id,
                            'document': f
                        })
                except Exception as e:
                    bot_request('sendMessage', {'chat_id': chat_id, 'text': f"خطأ في إرسال الملف: {e}"})
            else:
                bot_request('sendMessage', {'chat_id': chat_id, 'text': "الملف غير موجود."})

        if text == 'جلب الكل':
            for filename in os.listdir('.'):
                if os.path.isfile(filename):
                    try:
                        with open(filename, 'rb') as f:
                            bot_request('sendDocument', {
                                'chat_id': chat_id,
                                'document': f
                            })
                    except Exception as e:
                        bot_request('sendMessage', {'chat_id': chat_id, 'text': f"خطأ في إرسال الملف {filename}: {e}"})

        if text == 'الملفات':
            files_and_dirs = os.listdir('.')
            response_text = ""
            for i, item in enumerate(files_and_dirs):
                item_type = "(مجلد)" if os.path.isdir(item) else "(ملف)"
                response_text += f"{i + 1}- {item} {item_type}\n"
            
            if response_text:
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': response_text,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
            else:
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': "لا توجد ملفات أو مجلدات في المسار الحالي.",
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })

        if reply_to_message and reply_to_message.get('document') and text == 'رفع الملف':
            doc_file_id = reply_to_message['document']['file_id']
            doc_file_name = reply_to_message['document']['file_name']
            
            file_info = bot_request('getFile', {'file_id': doc_file_id})
            if file_info and file_info.get('ok'):
                file_path_on_telegram = file_info['result']['file_path']
                download_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path_on_telegram}"
                
                try:
                    file_content = requests.get(download_url).content
                    with open(doc_file_name, 'wb') as f:
                        f.write(file_content)
                    bot_request('sendMessage', {
                        'chat_id': chat_id,
                        'text': f"تم رفع الملف ؛ {doc_file_name}",
                        'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                except Exception as e:
                    bot_request('sendMessage', {'chat_id': chat_id, 'text': f"خطأ في تحميل أو حفظ الملف: {e}", 'reply_markup': json.dumps(DEV_BUTTONS)})
            else:
                bot_request('sendMessage', {'chat_id': chat_id, 'text': "لم يتم العثور على معلومات الملف.", 'reply_markup': json.dumps(DEV_BUTTONS)})

    # Decoration (زخرف) command
    if text and text.startswith("زخرف "):
        text_to_decorate = text.replace("زخرف ", "").strip()
        try:
            # Replaced original API with a generic placeholder, assume it returns decorated text
            # If the original API is still active, it can be used. Otherwise, a Python library or local function would be needed.
            decorated_text = requests.get(f'http://www.api-hany.cf/zgrfa/get.php?text={requests.utils.quote(text_to_decorate)}').text
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"{decorated_text}\n تم زخرفه : {text_to_decorate} يمكنك الضغط ع الاسم ليتم نسخه",
                'parse_mode': 'MarkDown',
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        except Exception as e:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': f"حدث خطأ أثناء الزخرفة: {e}",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # Delete new chat members join message
    if new_chat_member:
        bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})

    # Group Info (Replaced with @Vl_HI)
    if text == "/Group":
        group_info = bot_request('getChat', {'chat_id': chat_id})
        if group_info and group_info.get('ok'):
            group_title = group_info['result']['title']
            group_id = group_info['result']['id']
            member_count_res = bot_request('getChatMembersCount', {'chat_id': chat_id})
            member_count = member_count_res['result'] if member_count_res and member_count_res.get('ok') else 'N/A'

            bot_request('sendPhoto', {
                'chat_id': chat_id,
                'photo': "https://t.me/HAMo_ALKING_9", # Replaced with Vl_HI channel
                'caption': (
                    f"الاسم :⪼ {group_title}\n"
                    f"الايدي :⪼ {group_id}\n"
                    f"عدد الاعضاء :⪼ {member_count}"
                ),
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request('sendMessage', {
                'chat_id': chat_id,
                'text': "حدث خطأ أثناء جلب معلومات المجموعة.",
                'reply_to_message_id': message_id,
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Sudo Private /start menu
    if text == '/start' and from_id == SUDO_ID and chat_type == "private":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                'مـرحبآ بگ سـيدي آلمـطـور ⚄1�7 ؛\n\n'
                'آليگ قآئمـهہ آلآعدآدآت آلخآصـهہ في بوت الردود\n\n'
                'يمـگنگ تغيير آلآعدآدآت و تخصـيصـهآ گمـآ تشـآء �1�7�️ ؛'
            ),
            'reply_markup': json.dumps({
                'keyboard': [
                    [{'text': 'تغير اسم البوت'}, {'text': 'ضع كليشه المطور'}],
                    [{'text': 'الاحصائيات'}, {'text': 'المجموعات'}, {'text': 'المشتركين'}],
                    [{'text': 'اذاعه'}, {'text': 'اذاعه خاص'}, {'text': 'اذاعه بالتوجيه'}, {'text': 'اذاعه خاص بالتوجيه'}],
                    [{'text': 'مسح الردود العامه'}, {'text': 'الردود العامه'}],
                    [{'text': 'اسم البوت الحالي'}]
                ],
                'resize_keyboard': True
            })
        })

    # Bot name change (SUDO only)
    namebots_file = "data/namebot.txt"
    set_name_mode_file = "data/setengss.txt"
    if from_id == SUDO_ID:
        if text == "تغير اسم البوت":
            save_file_content(set_name_mode_file, "set")
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': " ارسل الاسم",
                'parse_mode': "MARKDOWN", 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif text and load_file_content(set_name_mode_file) == "set":
            save_file_content(namebots_file, text)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"تم التغير الى :- {text}",
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            delete_file(set_name_mode_file)
    
    # Sudo message change (SUDO only)
    sudo_message_file = "data/sudo.txt"
    set_sudo_mode_file = "data/setengs.txt"
    if from_id == SUDO_ID:
        if text == "ضع كليشه المطور":
            save_file_content(set_sudo_mode_file, "set")
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "ارسل الكليشه",
                'parse_mode': "MARKDOWN", 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        elif text and load_file_content(set_sudo_mode_file) == "set":
            save_file_content(sudo_message_file, text)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"تم التغير الى :- {text}",
                'reply_markup': json.dumps(DEV_BUTTONS)
            })
            delete_file(set_sudo_mode_file)

    # Display Sudo Message
    if text in ["المطور", "مطور"]:
        sudo_message_content = load_file_content(sudo_message_file)
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': sudo_message_content,
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Bot name trigger (This seems incomplete in original PHP, assuming it should echo the name)
    current_bot_name = load_file_content(namebots_file)
    if text == current_bot_name:
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f"اسمي {current_bot_name}", # Adjusted for clarity
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Stats for Sudo (private chat)
    if text == "الاحصائيات" and from_id == SUDO_ID:
        members_pv = load_file_content("data/memomemb.txt").split('\n')
        members_pv = [m for m in members_pv if m]
        
        groups_list = load_file_content("data/groups.txt").split('\n')
        groups_list = [g for g in groups_list if g]
        
        left_groups_list = load_file_content("data/left.txt").split('\n')
        left_groups_list = [g for g in left_groups_list if g]

        active_groups_count = len(groups_list)
        left_groups_count = len(left_groups_list)
        correct_groups_count = active_groups_count - left_groups_count # Logic from original code

        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                f"🗳¦ عدد الكلي للمجموعات « *{active_groups_count}* »\n"
                f"📈¦ عدد المجموعات المطرودة « *{left_groups_count}* »\n"
                f"📊¦ عدد المجموعات الصحيح « *{correct_groups_count}* »\n\n"
                f"عدد المشتركين :- {len(members_pv)}"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Members count (SUDO private chat)
    if text == "المشتركين" and from_id == SUDO_ID:
        members_pv = load_file_content("data/memomemb.txt").split('\n')
        members_pv = [m for m in members_pv if m]
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f"عدد المشتركين :- {len(members_pv)}",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Private Broadcast (SUDO only)
    memo_usr_file = "data/memousr.txt"
    if text == "اذاعه خاص" and from_id == SUDO_ID:
        save_file_content(memo_usr_file, "onvp")
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': "دز الاذاعة",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif text and load_file_content(memo_usr_file) == "onvp" and from_id == SUDO_ID:
        members_pv = load_file_content("data/memomemb.txt").split('\n')
        members_pv = [m for m in members_pv if m]
        
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f"تم ارسال الرسالة الى {len(members_pv)} .",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
        for member_id in members_pv:
            if member_id:
                bot_request('sendMessage', {
                    'chat_id': int(member_id), 'text': text,
                    'parse_mode': "MarkDown", 'disable_web_page_preview': True,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        save_file_content(memo_usr_file, "memo")

    # Group Broadcast (SUDO only)
    if text == "اذاعه" and from_id == SUDO_ID:
        save_file_content(memo_usr_file, "gp")
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': "دز الاذاعة",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif text and load_file_content(memo_usr_file) == "gp" and from_id == SUDO_ID:
        groups_list = load_file_content("data/groups.txt").split('\n')
        groups_list = [g for g in groups_list if g]
        
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f"تم ارسال الرسالة الى {len(groups_list)} .",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
        for group_id in groups_list:
            if group_id:
                bot_request('sendMessage', {
                    'chat_id': int(group_id), 'text': text,
                    'parse_mode': "MarkDown", 'disable_web_page_preview': True,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        save_file_content(memo_usr_file, "memo")

    # Broadcast with Forward (SUDO only)
    if text == "اذاعه بالتوجيه" and from_id == SUDO_ID:
        save_file_content(memo_usr_file, "gpf")
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': "دز الاذاعة",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif message and load_file_content(memo_usr_file) == "gpf" and from_id == SUDO_ID:
        groups_list = load_file_content("data/groups.txt").split('\n')
        groups_list = [g for g in groups_list if g]
        
        for group_id in groups_list:
            if group_id:
                bot_request('forwardMessage', {
                    'chat_id': int(group_id),
                    'from_chat_id': chat_id,
                    'message_id': message_id
                })
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f"تم ارسال الرسالة الى {len(groups_list)} .",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
        save_file_content(memo_usr_file, "memo")

    # Private Broadcast with Forward (SUDO only)
    if text == "اذاعه خاص بالتوجيه" and from_id == SUDO_ID:
        save_file_content(memo_usr_file, "pvf")
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': "دز الاذاعة",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif message and load_file_content(memo_usr_file) == "pvf" and from_id == SUDO_ID:
        members_pv = load_file_content("data/memomemb.txt").split('\n')
        members_pv = [m for m in members_pv if m]
        
        for member_id in members_pv:
            if member_id:
                bot_request('forwardMessage', {
                    'chat_id': int(member_id),
                    'from_chat_id': chat_id,
                    'message_id': message_id
                })
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f"تم ارسال الرسالة الى {len(members_pv)} .",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
        save_file_content(memo_usr_file, "memo")

    # Public Replies list (SUDO only, incomplete logic from original)
    if text == "الردود العامه" and from_id == SUDO_ID:
        # The PHP code seems to reference 'data/rd.txt' but it's not populated in this script.
        # Assuming `filter.txt` was meant, or a dedicated replies file
        # For now, it will be empty if 'rd.txt' doesn't exist
        public_replies = load_file_content("data/rd.txt")
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f"قائمة الردود \n{public_replies}",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Current Bot Name (SUDO only)
    if text == "اسم البوت الحالي" and from_id == SUDO_ID:
        current_bot_name = load_file_content(namebots_file)
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': f"اسم البوت الان \n{current_bot_name}",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # "هه" and similar laugh responses
    if text and any(laugh_text in text for laugh_text in ["هه", "ههه", "هههه", "ههههه", "هههههه", ".◦° =D °◦н̲h̲нн̲h̲нн̲h н̲h̲нн̲h̲нн̲h◦° =D °◦.", "=D (..هَّـَِـَِہْہْـَِہْـَِہْـَِہْہْـَِـَِ[X_X]ـَِـَِہْہْـَِہْـَِہْہْـَِـَِاٌاُاّيٌَ..) =))", "=D {..هہہہہہہـ( =)) )ـہہہہہہہٱٱٱي..} (y) =D", "=)) «--- فآاآطِسّ :D ضِحّگـٌے---» =)) ", "هَْـٍََْ =)) ہٌهہٌ{ گــفگ يآلخبل} ہٌهـٍََْ =)) ـٍََْاْاْي", "ھَھٍھَھٍھَھٍـٌ( =)) )ـّھٍھَھٍھَھٍٱإيّےٌ "]):
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': "⌣{دِْۈۈۈۈ/يّارٌبْ_مـْو_يـّوّمٌ/ۈۈۈۈمْ}⌣",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Pin message
    if is_admin_or_creator and reply_to_message and text == "تثبيت":
        bot_request("pinChatMessage", {'chat_id': chat_id, 'message_id': re_msgid})
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': " 🙋🏼‍♂️¦ أهلا عزيزي  \n📌¦ تم تثبيت الرساله\n✓",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif text == "تثبيت" and from_id != SUDO_ID and group_status == "member": # For members, notify restriction
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': "📛¦ هذا الامر يخص {الادمن,المدير,المنشئ,المطور} فقط  \n🚶",
            'reply_to_message_id': message_id, 'parse_mode': 'MARKDOWN', 'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Restrict/Unrestrict
    if is_admin_or_creator:
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text == "تقييد":
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': (
                    f"👤¦ العضو » @{re_user}\n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تم تقييده \n✓️"
                ), 'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('restrictChatMember', {
                'chat_id': chat_id, 'user_id': re_id,
                'permissions': {'can_send_messages': False}
            })
        elif reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and (text == "/unban" or text == "الغاء التقييد"): # "/unban" is a typo from PHP
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': (
                    f"👤¦ العضو » @{re_user} \n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تم الغاء تقييده \n✓️"
                ), 'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('restrictChatMember', {
                'chat_id': chat_id, 'user_id': re_id,
                'permissions': {'can_send_messages': True, 'can_send_audios': True, 'can_send_documents': True, 'can_send_photos': True, 'can_send_videos': True, 'can_send_video_notes': True, 'can_send_voice_notes': True, 'can_send_other_messages': True}
            })

    # Mute/Unmute (PHP uses `deleteMessage` on user ID, which is not mute. This will be an actual mute/unmute)
    if is_admin_or_creator:
        if reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and text == "كتم": # "لتدل" was the original trigger, changing to "كتم"
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': (
                    f"👤¦ العضو » @{re_user}\n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تم كتمه\n✓️"
                ), 'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('restrictChatMember', {
                'chat_id': chat_id, 'user_id': re_id,
                'permissions': {'can_send_messages': False, 'can_send_media_messages': False, 'can_send_polls': False, 'can_send_other_messages': False, 'can_add_web_page_previews': False, 'can_change_info': False, 'can_invite_users': False, 'can_pin_messages': False}
            })
        elif reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and (text == "الغاء الكتم" or text == "/unmute"): # "الغاء بازد" original
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': (
                    f"👤¦ العضو » @{re_user}\n"
                    f"🎫¦ الايدي » ( {re_id} )\n"
                    "🛠¦ تم الغاء كتمه\n✓"
                ), 'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('restrictChatMember', {
                'chat_id': chat_id, 'user_id': re_id,
                'permissions': {'can_send_messages': True, 'can_send_media_messages': True, 'can_send_polls': True, 'can_send_other_messages': True, 'can_add_web_page_previews': True, 'can_change_info': True, 'can_invite_users': True, 'can_pin_messages': True}
            })
    
    # "رفع الادمنيه" - unclear what this was for in PHP, seems to be a generic message
    if is_admin_or_creator and text == "رفع الادمنيه":
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': "📊┇ تم رفع ادمنيه المجموعه في البوت",
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
    elif text == "رفع الادمنيه" and from_id != SUDO_ID and group_status == "member":
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': "📡¦ هذا الامر يخص الادمنيه فقط  🚶",
            'reply_to_message_id': message_id, 'parse_mode': 'MARKDOWN', 'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # List Admins (original used external API)
    if text == "الادمنيه":
        chat_administrators = bot_request('getChatAdministrators', {'chat_id': chat_id})
        admin_list = []
        if chat_administrators and chat_administrators.get('ok'):
            for admin in chat_administrators['result']:
                admin_name = admin['user']['first_name']
                admin_id = admin['user']['id']
                admin_list.append(f"- {admin_name} ({admin_id})")
        
        response_text = "قائمة المشرفين:\n" + "\n".join(admin_list) if admin_list else "لا يوجد مشرفون."
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': response_text,
            'parse_mode': 'MarkDown', 'disable_web_page_preview': True, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Set/Delete Chat Photo
    if is_admin_or_creator:
        if text == 'ضع صورة' and message.get('reply_to_message') and message['reply_to_message'].get('photo'):
            photo_file_id = message['reply_to_message']['photo'][-1]['file_id']
            bot_request('setChatPhoto', {'chat_id': chat_id, 'photo': photo_file_id})
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "✅┇ تم وضع صورة للمجموعة بنجاح\n✔️ ",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        if text == 'حذف الصورة':
            bot_request('deleteChatPhoto', {'chat_id': chat_id})
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "❌┇ تم حذف صورة المجموعة بنجاح\n❌ ",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Leave Group (SUDO only)
    if text and text.startswith("غادر ") and from_id == SUDO_ID:
        target_chat_id = text.replace("غادر ", "").strip()
        try:
            target_chat_id = int(target_chat_id)
            bot_request('sendMessage', {'chat_id': target_chat_id, 'text': "عذرا لا يمكنني حماية هذا المجموعة", 'reply_markup': json.dumps(DEV_BUTTONS)})
            bot_request('leaveChat', {'chat_id': target_chat_id})
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"تم الخروج من المجموعة\n—\nID : {target_chat_id}",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        except ValueError:
            bot_request('sendMessage', {'chat_id': chat_id, 'text': "معرف المجموعة غير صالح.", 'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)})

    # Kick Myself ("اطردني")
    if text == "اطردني":
        if group_status == "member":
            export_link_response = bot_request('exportChatInviteLink', {'chat_id': chat_id})
            invite_link = export_link_response['result'] if export_link_response and export_link_response.get('ok') else 'N/A'
            
            bot_request('kickChatMember', {'chat_id': chat_id, 'user_id': from_id})
            # Unban immediately to allow rejoining
            bot_request('unbanChatMember', {'chat_id': chat_id, 'user_id': from_id}) 
            
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "🚸| لقد تم طردك بنجاح , ارسلت لك رابط المجموعه في الخاص اذا وصلت لك تستطيع الرجوع متى شئت🏻",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
            bot_request('sendMessage', {
                'chat_id': from_id, 'text': (
                    "👨🏼‍⚕️| اهلا عزيزي , لقد تم طردك من المجموعه بامر منك \n"
                    "🔖| اذا كان هذا بالخطأ او اردت الرجوع للمجموعه \n\n"
                    "🔖¦فهذا رابط المجموعه 💯\n\n"
                    f"🌿¦{invite_link} :"
                ), 'parse_mode': "HTML", 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else: # Admin, Creator, Sudo
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': "📛¦ لا استطيع طرد المدراء والادمنيه والمنشئين  \n🚶",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # "بووتي" (SUDO only)
    if text == 'بووتي' and from_id == SUDO_ID:
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': " نعم حبيبي المطور 🌝❤ ",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Restricted commands for members
    restricted_cmds_for_members = {
        "حظر عام": "{المطور الاساسي}", "تثبيت": "{الادمن,المدير,المنشئ,المطور}",
        "م المطور": "{المطور الاساسي}", "اذاعه": "{المطور}",
        "كتم": "{الادمن,المدير,المنشئ,المطور}", "تقييد": "{الادمن,المدير,المنشئ,المطور}",
        "رفع ادمن": "{الادمن,المدير,المنشئ,المطور}", "الغاء التقييد": "{الادمن,المدير,المنشئ,المطور}",
        "الغاء الكتم": "{الادمن,المدير,المنشئ,المطور}", "حظر": "{الادمن,المدير,المنشئ,المطور}",
        "الغاء الحظر": "{الادمن,المدير,المنشئ,المطور}", "طرد": "{الادمن,المدير,المنشئ,المطور}",
        "تحديث ♻": "{المطور الاساسي}",
        "ضع اسم ": "{الادمن,المدير,المنشئ,المطور}", # Special handling
        "/kool": "{الادمن,المدير,المنشئ,المطور}", "تنزيل ادمن": "{الادمن,المدير,المنشئ,المطور}"
    }

    if group_status == "member" and from_id != SUDO_ID:
        for cmd, role in restricted_cmds_for_members.items():
            if (cmd in text and cmd != "ضع اسم ") or (cmd == "ضع اسم " and text.startswith("ضع اسم ")):
                bot_request('sendMessage', {
                    'chat_id': chat_id,
                    'text': f"📛¦ هذا الامر يخص {role} فقط  \n🚶",
                    'reply_to_message_id': message_id,
                    'parse_mode': 'MARKDOWN',
                    'disable_web_page_preview': True,
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
                break

    # "تنزيل ادمن" command
    if is_admin_or_creator and reply_to_message and re_id != BOT_ID and re_id != SUDO_ID and (text == "/kool" or text == "تنزيل ادمن"): # /kool is typo from PHP
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': (
                f"👤¦ العضو » @{re_user} \n"
                f"🎫¦ الايدي » ( {re_id} )\n"
                "🛠¦ تمت تنزيل الادمن \n✓️"
            ), 'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })
        # Demote user to regular member
        bot_request('promoteChatMember', {'chat_id': chat_id, 'user_id': re_id, 'can_manage_chat': False, 'can_delete_messages': False, 'can_invite_users': False, 'can_restrict_members': False, 'can_pin_messages': False, 'can_promote_members': False})


    # "كشف" command (user info by reply)
    if reply_to_message and text == "كشف":
        re_id = reply_to_message.get('from', {}).get('id')
        re_user_status = get_chat_member_status(chat_id, re_id)
        re_user_name = reply_to_message.get('from', {}).get('first_name')
        re_user_username = reply_to_message.get('from', {}).get('username')

        rank_map = {
            "creator": "المنشىء 👷",
            "administrator": "ادمن في البوت 👨🏼‍🎓",
            "member": "فقط عضو 🙍🏼‍♂️",
            str(SUDO_ID): "مطور اساسي 👨🏻‍⚕"
        }
        
        actual_rank = rank_map.get(str(re_id)) if re_id == SUDO_ID else rank_map.get(re_user_status, "عضو")

        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                f"🤵🏼¦ الاسم » {{ {re_user_name} }}\n"
                f"🎫¦ الايدي » {{ {re_id} }} \n"
                f"🎟¦ المعرف »{{ @{re_user_username} }}\n"
                f"📮¦ الرتبه » {actual_rank}\n"
                "🕵🏻️‍♀️¦ نوع الكشف » بالرد\n"
                "➖"
            ),
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Filter commands
    filter_dir = f"data/filter"
    filter_file = f"{filter_dir}/s{chat_id}.json"
    
    current_filters = []
    if os.path.exists(filter_file):
        current_filters = load_file_content(filter_file).split('\n')
        current_filters = [f.strip() for f in current_filters if f.strip()]

    if is_admin_or_creator:
        if text and text.startswith("منع "):
            keyword = text.replace("منع ", "").strip()
            if keyword in current_filters:
                bot_request('sendMessage', {
                    'chat_id': chat_id, 'parse_mode': "markdown", 'text': f"تـم 🚷 منـ؏ الـ({keyword}) 💯",
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
            else:
                append_file_content(filter_file, f"{keyword}\n")
                bot_request('sendMessage', {
                    'chat_id': chat_id, 'parse_mode': "markdown", 'text': f"تـم 🚷 منـ؏ الـ({keyword}) 💯",
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })

        if text and text.startswith("الغاء منع "):
            keyword = text.replace("الغاء منع ", "").strip()
            if keyword not in current_filters:
                bot_request('sendMessage', {
                    'chat_id': chat_id, 'parse_mode': "markdown", 'text': f"تـم 🚷 إلغـاء منـ؏ الـ({keyword}) 💯",
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
            else:
                new_filters = [f for f in current_filters if f != keyword]
                save_file_content(filter_file, "\n".join(new_filters) + "\n" if new_filters else "")
                bot_request('sendMessage', {
                    'chat_id': chat_id, 'parse_mode': "markdown", 'text': f"تـم 🚷 إلغـاء منـ؏ الـ({keyword}) 💯",
                    'reply_markup': json.dumps(DEV_BUTTONS)
                })
        
        if text == "قائمة المنع":
            filter_list_content = "\n".join(current_filters) if current_filters else "لا توجد كلمات ممنوعة."
            bot_request('sendMessage', {
                'chat_id': chat_id, 'parse_mode': "markdown",
                'text': f"_قائمة الكلمات الممنوعة ☑️_\n{filter_list_content}\n\n]📡┊Channel Bots](https://t.me/dataALKooool)",
                'disable_web_page_preview': True, 'reply_markup': json.dumps(DEV_BUTTONS)
            })

        if text == "مسح قائمة المنع":
            if not os.path.exists(filter_file) or not current_filters:
                bot_request('sendMessage', {'chat_id': chat_id, 'text': "لايـوجد 🚸  قائمـة منـ؏ للحـذف ‼️", 'reply_markup': json.dumps(DEV_BUTTONS)})
            else:
                delete_file(filter_file)
                bot_request('sendMessage', {'chat_id': chat_id, 'text': "تـم 🚸 حـذف قائمـة المنـ؏ ‼️", 'reply_markup': json.dumps(DEV_BUTTONS)})
    
    # Generic filter logic for members
    if text and current_filters and group_status == "member" and text.strip() in current_filters:
        bot_request('deleteMessage', {'chat_id': chat_id, 'message_id': message_id})


    # User ID info (duplicate logic, consolidating)
    # The original PHP had many 'if text == "ايدي"' blocks, this will handle it based on status.
    if text == "ايدي":
        caption_text = ""
        user_profile_photos = bot_request("getUserProfilePhotos", {"user_id": from_id, "limit": 1, "offset": 0})
        file_id = user_profile_photos["result"]["photos"][0][0]["file_id"] if user_profile_photos and user_profile_photos.get("ok") and user_profile_photos["result"]["photos"] else None
        
        rank_text = ""
        # Custom ranks are handled by files, check those first
        memo_devs = load_file_content("data/memo.txt").split('\n')
        memo_devs = [m.strip() for m in memo_devs if m.strip()]
        
        cretor_ids = load_file_content(f"data/{chat_id}/cretor.txt").split('\n')
        cretor_ids = [c.strip() for c in cretor_ids if c.strip()]
        
        onair_ids = load_file_content(f"data/{chat_id}/onair.txt").split('\n')
        onair_ids = [o.strip() for o in onair_ids if o.strip()]
        
        admin_ids = load_file_content(f"data/{chat_id}/admin.txt").split('\n')
        admin_ids = [a.strip() for a in admin_ids if a.strip()]
        
        memberil_ids = load_file_content(f"data/{chat_id}/memberil.txt").split('\n')
        memberil_ids = [m.strip() for m in memberil_ids if m.strip()]

        if from_id == SUDO_ID:
            rank_text = "مطور اساسي 👨🏻‍✈️"
        elif str(from_id) in memo_devs:
            rank_text = "مطور البوت 🗳" # Assuming this means sub-developer
        elif str(from_id) in cretor_ids:
            rank_text = "المنشئ  🗳"
        elif str(from_id) in onair_ids:
            rank_text = "المدير  🗳"
        elif str(from_id) in admin_ids:
            rank_text = "ادمن 🗳"
        elif str(from_id) in memberil_ids:
            rank_text = "عضو مميز بالبوت 🗳"
        else: # Fallback to Telegram API status
            if group_status == "creator":
                rank_text = "المنشىء 👷🏽"
            elif group_status == "administrator":
                rank_text = "ادمن في البوت 👨🏼‍🎓"
            else: # member, restricted, left, etc.
                rank_text = "فقط عضو 🙍🏼‍♂️"
        
        caption_text = (
            f"👤¦ أســمـك •⊱ {{  {user_name}  }} •\n"
            f"🎫¦ مـعرفك •⊱ @{user_username} ⊰• \n"
            f"🏷¦ ايديــك •⊱ {{  {from_id}  }} ⊰•\n"
            f"📮¦ رتبتـــك •⊱ {rank_text} ⊰•\n"
            f"💬¦ رسائلك • {{ *{user_message_count}* }} •\n"
            "➖"
        )
        if file_id:
            bot_request("sendPhoto", {
                "chat_id": chat_id, "caption": caption_text,
                'parse_mode': "MarkDown", "photo": file_id,
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        else:
            bot_request("sendMessage", {
                "chat_id": chat_id, "text": "🚸¦ لا يوجد صوره في بروفايلك ...!\n" + caption_text,
                'parse_mode': "MarkDown", 'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })

    # "نقاطي" command
    user_points_file = f"data/{chat_id}-{from_id}.txt"
    user_points = load_file_content(user_points_file, "0")
    if text == "نقاطي":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"📬¦ عدد نقاطك من اللعبه هي {{ {user_points} }}",
            'reply_to_message_id': message_id, 'parse_mode': 'MARKDOWN', 'disable_web_page_preview': True,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Role Management (SUDO/Custom Admins only)
    # The PHP logic relies on `strstr` for checking membership in file-based roles.
    # This translates to `str(from_id) in list_of_ids` in Python.
    
    # Custom Admins
    admin_roles_file = f"data/{chat_id}/admin.txt"
    current_admin_roles = load_file_content(admin_roles_file).split('\n')
    current_admin_roles = [r.strip() for r in current_admin_roles if r.strip()]

    can_manage_roles = (from_id == SUDO_ID or str(from_id) in memo_devs or str(from_id) in onair_ids or str(from_id) in cretor_ids)

    if can_manage_roles:
        if reply_to_message:
            target_id = str(re_id)
            if text == "رفع ادمن":
                if target_id in current_admin_roles:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه ادمن بالفعل\n✓️",
                        'reply_to_message_id': message_id, 'parse_mode': 'MARKDOWN', 'disable_web_page_preview': True,
                        'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    append_file_content(admin_roles_file, f"{target_id}\n")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه ادمن \n✓️",
                        'reply_to_message_id': message_id, 'parse_mode': 'MARKDOWN', 'disable_web_page_preview': True,
                        'reply_markup': json.dumps(DEV_BUTTONS)
                    })
            elif text == "تنزيل ادمن":
                if target_id in current_admin_roles:
                    new_admin_roles = [r for r in current_admin_roles if r != target_id]
                    save_file_content(admin_roles_file, "\n".join(new_admin_roles) + "\n" if new_admin_roles else "")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم تنزيله من الادمنيه\n✓️",
                        'reply_to_message_id': message_id, 'parse_mode': 'MARKDOWN', 'disable_web_page_preview': True,
                        'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ ليس في قائمه الادمنيه\n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })

    # Custom Developers (SUDO only can manage)
    memo_devs_file = "data/memo.txt"
    memo_devs = load_file_content(memo_devs_file).split('\n')
    memo_devs = [m.strip() for m in memo_devs if m.strip()]
    if from_id == SUDO_ID and bot_group_status == "administrator": # Original condition
        if reply_to_message:
            target_id = str(re_id)
            if text in ["اضف مطور", "رفع مطور"]:
                if target_id in memo_devs:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه مطور مسبقاً\n✓️",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    append_file_content(memo_devs_file, f"{target_id}\n")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه مطور\n✓️",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
            elif text in ["حذف مطور", "تنزيل مطور"]:
                if target_id in memo_devs:
                    new_memo_devs = [d for d in memo_devs if d != target_id]
                    save_file_content(memo_devs_file, "\n".join(new_memo_devs) + "\n" if new_memo_devs else "")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم تنزيله من قائمه المطورين\n✓️",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ ليس في قائمه المطورين\n✓️",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })

    # Custom Managers (مدراء)
    onair_file = f"data/{chat_id}/onair.txt"
    onair_ids = load_file_content(onair_file).split('\n')
    onair_ids = [o.strip() for o in onair_ids if o.strip()]
    
    can_manage_onair = (from_id == SUDO_ID or str(from_id) in memo_devs or str(from_id) in cretor_ids)

    if can_manage_onair:
        if reply_to_message:
            target_id = str(re_id)
            if text == "رفع مدير":
                if target_id in onair_ids:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه مدير مسبقا\n✓️",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    append_file_content(onair_file, f"{target_id}\n")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ العضو تم رفعه مدير \n✓️",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
            elif text == "تنزيل مدير":
                if target_id in onair_ids:
                    new_onair_ids = [o for o in onair_ids if o != target_id]
                    save_file_content(onair_file, "\n".join(new_onair_ids) + "\n" if new_onair_ids else "")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦تم تنزيله من قائمه المدراء\n✓️",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ليس في قائمه المدراء\n✓️",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })

    # Custom Creators (منشئين)
    cretor_file = f"data/{chat_id}/cretor.txt"
    cretor_ids = load_file_content(cretor_file).split('\n')
    cretor_ids = [c.strip() for c in cretor_ids if c.strip()]
    
    can_manage_cretor = (from_id == SUDO_ID or str(from_id) in memo_devs)

    if can_manage_cretor:
        if reply_to_message:
            target_id = str(re_id)
            if text == "رفع منشى":
                if target_id in cretor_ids:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه منشى مسبقاً\n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    append_file_content(cretor_file, f"{target_id}\n")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه الى منشى\n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
            elif text == "تنزيل منشى":
                if target_id in cretor_ids:
                    new_cretor_ids = [c for c in cretor_ids if c != target_id]
                    save_file_content(cretor_file, "\n".join(new_cretor_ids) + "\n" if new_cretor_ids else "")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم تنزيله من قائمه المنشئين \n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ ليس في قائمه المنشئين \n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
    
    # Custom Distinguished Members (مميز)
    memberil_file = f"data/{chat_id}/memberil.txt"
    memberil_ids = load_file_content(memberil_file).split('\n')
    memberil_ids = [m.strip() for m in memberil_ids if m.strip()]
    
    can_manage_memberil = (from_id == SUDO_ID or str(from_id) in memo_devs or str(from_id) in onair_ids or str(from_id) in cretor_ids)

    if can_manage_memberil:
        if reply_to_message:
            target_id = str(re_id)
            if text == "رفع عضو مميز":
                if target_id in memberil_ids:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه عضو مميز مسبقاً \n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    append_file_content(memberil_file, f"{target_id}\n")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم رفعه عضو مميز \n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
            elif text == "تنزيل عضو مميز":
                if target_id in memberil_ids:
                    new_memberil_ids = [m for m in memberil_ids if m != target_id]
                    save_file_content(memberil_file, "\n".join(new_memberil_ids) + "\n" if new_memberil_ids else "")
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ تم تنزيله من قائمه الاعضاء المميزين\n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })
                else:
                    bot_request("sendMessage", {
                        "chat_id": chat_id, "text": f"👤¦ العضو » •⊱ [{target_id}](tg://user?id={target_id}) \n🛠¦ ليس في قائمه الاعضاء المميزين\n√",
                        "parse_mode": "markdown", 'reply_markup': json.dumps(DEV_BUTTONS)
                    })

    # List custom roles
    if chat_type == "supergroup":
        if from_id == SUDO_ID and text == "المطورين":
            memo_devs_list_str = "\n".join(memo_devs)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"🔱¦ أليك قائمة المطورين بالأيديات 📮؛\n\n<b>{memo_devs_list_str}</b>\n\n➖",
                'reply_to_message_id': message_id, 'parse_mode': "html", 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        
        if can_manage_roles and text == "المنشئين":
            cretor_ids_list_str = "\n".join(cretor_ids)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"🔱¦ أليك قائمة المنشئين بالأيديات 📮؛\n\n<b>{cretor_ids_list_str}</b>\n\n➖",
                'reply_to_message_id': message_id, 'parse_mode': "html", 'reply_markup': json.dumps(DEV_BUTTONS)
            })
            
        if can_manage_roles and text == "المدراء":
            onair_ids_list_str = "\n".join(onair_ids)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"🔱¦ أليك قائمة المدراء بالأيديات 📮؛\n\n<b>{onair_ids_list_str}</b>\n\n➖",
                'reply_to_message_id': message_id, 'parse_mode': "html", 'reply_markup': json.dumps(DEV_BUTTONS)
            })
            
        if can_manage_roles and text == "الادمنيه":
            admin_roles_list_str = "\n".join(current_admin_roles)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"🔱¦ أليك قائمة الادمنيه بالأيديات 📮؛\n\n<b>{admin_roles_list_str}</b>\n\n➖",
                'reply_to_message_id': message_id, 'parse_mode': "html", 'reply_markup': json.dumps(DEV_BUTTONS)
            })
        
        if can_manage_roles and text in ["المميزون", "المميزين"]:
            memberil_ids_list_str = "\n".join(memberil_ids)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"🔱¦ أليك قائمة الأعظاء المميزين بالأيديات 📮؛\n\n<b>{memberil_ids_list_str}</b>\n\n➖",
                'reply_to_message_id': message_id, 'parse_mode': "html", 'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Clear custom roles
    if from_id == SUDO_ID and text == "مسح المطورين":
        if chat_type == "supergroup":
            count_deleted = len(memo_devs)
            delete_file(memo_devs_file)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"📛¦ تم حذف {{ {count_deleted} }} من المطورين بنجاح\n√",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    if can_manage_roles and text == "مسح المنشئين":
        if chat_type == "supergroup":
            count_deleted = len(cretor_ids)
            delete_file(cretor_file)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"📛¦ تم حذف {{ {count_deleted} }} من المنشئين بنجاح\n√",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })

    if can_manage_roles and text == "مسح المدراء":
        if chat_type == "supergroup":
            count_deleted = len(onair_ids)
            delete_file(onair_file)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"📛¦ تم حذف {{ {count_deleted} }} من المدراء بنجاح\n√",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
            # Original PHP had this block twice for "مسح المدراء", second one for admins, merging.
            count_deleted_admins = len(current_admin_roles)
            delete_file(admin_roles_file)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"📛¦ تم حذف {{ {count_deleted_admins} }} من الادمنيه بنجاح\n√",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })

    if can_manage_roles and text in ["حذف المميزين", "مسح المميزين"]:
        if chat_type == "supergroup":
            count_deleted = len(memberil_ids)
            delete_file(memberil_file)
            bot_request('sendMessage', {
                'chat_id': chat_id, 'text': f"📛¦ تم حذف {{ {count_deleted} }} من الاعضاء المميزين بنجاح\n√",
                'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
            })
    
    # Left Chat Member (bot leaves)
    if left_chat_member and left_chat_member.get('id') == BOT_ID:
        # If the bot itself left, remove the chat from groups.txt
        new_groups = [g for g in groups if g != str(chat_id)]
        save_file_content("data/groups.txt", "\n".join(new_groups) + "\n" if new_groups else "")
        # The PHP code sends a message to sudo here, for bot being kicked
        chat_title = message.get('chat', {}).get('title', 'N/A')
        bot_request('sendMessage', {
            'chat_id': SUDO_ID,
            'text': (
                "\n📛| قام شخص بطرد البوت من المجموعه الاتيه : \n"
                f"🏷| ألايدي : {chat_id}\n"
                f"🗯| الـمجموعه : {chat_title}\n\n"
                "📮| تـم مسح كل بيانات المجموعه بنـجاح"
            ),
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # "الكروبات" Command (duplicate of "المجموعات", merging)
    if text == "الكروبات":
        members_pv = load_file_content("data/memomemb.txt").split('\n')
        members_pv = [m for m in members_pv if m]
        
        groups_list = load_file_content("data/groups.txt").split('\n')
        groups_list = [g for g in groups_list if g]
        
        left_groups_list = load_file_content("data/left.txt").split('\n')
        left_groups_list = [g for g in left_groups_list if g]

        active_groups_count = len(groups_list)
        
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"📮¦ عدد المجموعات المفعلة » *{active_groups_count}*  ➼",
            'parse_mode': 'MARKDOWN',
            'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # "جهاتي" command (seems to rely on a `NumberofAddicts` variable not defined, will return 0)
    if text == "جهاتي":
        # Placeholder for `NumberofAddicts`. In a real bot, this would require querying a database
        # or another mechanism to count contacts added by the user.
        number_of_addicts = 0 
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': f"عدد جهاتك المضافة {number_of_addicts}",
            'reply_to_message_id': message_id,
            'parse_mode': "html",
            'reply_markup': json.dumps(DEV_BUTTONS)
        })
    
    # Games: "ترتيب", "الاسرع", "معاني"
    # Word scramble game ("ترتيب")
    word_scramble_phrases = [
        'اســرع واحد يرتب » { ل ، س ، ا ، ق ، ت ،ب ، ا } «', # استقبال
        'اســرع واحد يرتب » { ه ، ا ، ر ، س ، ي } «',       # سياره
        'اســرع واحد يرتب » { ر ، و ، ح ، س } «',           # سحور
        'اســرع واحد يرتب » { و ، ن ، ي ، ا ، ف } «',       # ايفون
        'اســرع واحد يرتب » { ا ، ش ، ن ، ح } «',           # شاحن
        'اســرع واحد يرتب » { ب ، و ، ر ، و ، ت } «',       # روبوت
        'اســرع واحد يرتب » { ب ، م ، ل ، ا ، س } «',       # ملابس
        'اســرع واحد يرتب » { ض ، ح ، ر ، م ، و ، ت } «',   # حضرموت
        'اســرع واحد يرتب » { ط ، ب ، ي ، ر ، ق } «',       # بطريق
        'اســرع واحد يرتب » { ف ، ي ، س ، ه ، ن } «',       # سفينه
        'اســرع واحد يرتب » { ج ، ا ، ج ، د ، ه } «',       # دجاجه
        'اســرع واحد يرتب » { س ، م ، ر ، د ، ه } «',       # مدرسه
        'اســرع واحد يرتب » { ا ، ا ، ل ، ن ، و } «',       # الوان
        'اســرع واحد يرتب » { ر ، ه ، غ ، ف } «',           # غرفه
        'اســرع واحد يرتب » { ج ، ه ، ل ، ا ، ث } «',       # ثلاجه
        'اســرع واحد يرتب » { خ ، م ، ب ، ط } «',           # مطبخ
        'اســرع واحد يرتب » { ش ، و ، ع ، ل } «',           # علوش (name)
        'اســرع واحد يرتب » { ل ، ا ، م ، ك } «',           # كلام
        'اســرع واحد يرتب » { ح ، ن ، و ، ي ، ا } «',       # حيوان
        'اســرع واحد يرتب » { س ، ا ، د } «',               # اسد
        'اســرع واحد يرتب » { خ ، ط ، و ، ط ، ا ، ب } «',   # اخطبوط
        'اســرع واحد يرتب » { ف ، ش ، ر ، ه ، ا } «',       # فراشه
    ]
    if text in ["ترتيب", "الترتيب", "ترتيب"]:
        import random
        selected_phrase = random.choice(word_scramble_phrases)
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': selected_phrase,
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Points for word scramble solutions
    scramble_solutions = {
        'سحور', 'سياره', 'فراشه', 'اخطبوط', 'اسد', 'حيوان', 'علوش', 'كلام', 'استقبال',
        'شاحن', 'ايفون', 'روبوت', 'مطبخ', 'ملابس', 'دجاجه', 'مدرسه', 'الوان', 'غرفه',
        'ثلاجه', 'بطريق', 'سفينه', 'حضرموت'
    }
    if text and text.lower() in scramble_solutions:
        current_points = int(load_file_content(user_points_file, "0"))
        new_points = current_points + 1
        save_file_content(user_points_file, str(new_points))
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "🎉¦ مبروك لقد ربحت نقطه\n"
                f"🔖¦ اصبح لديك {{ {new_points} }} نقطه 🍃️\n"
            ),
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Fast Emoji game ("الاسرع")
    fast_emoji_prompts = [
        'اسرع شخص يدز » { ️`😈` } «', 'اسرع شخص يدز » { ️`🏦` } «', 'اسرع شخص يدز » { ️`🏥` } «',
        'اسرع شخص يدز » { ️`🐢` } «', 'اسرع شخص يدز » { ️`🐀` } «', 'اسرع شخص يدز » { ️`🐁` } «',
        'اسرع شخص يدز » { ️`🐱` } «', 'اسرع شخص يدز » { ️`🐩` } «', 'اسرع شخص يدز » { ️`😨` } «',
        'اسرع شخص يدز » { ️`😴` } «', 'اسرع شخص يدز » { ️`🔧` } «', 'اسرع شخص يدز » { ️`🏇` } «',
        'اسرع شخص يدز » { ️`🗼` } «', 'اسرع شخص يدز » { ️`🔨` } «', 'اسرع شخص يدز » { ️`🎈` } «',
        'اسرع شخص يدز » { ️`🔛` } «', 'اسرع شخص يدز » { ️`⏳` } «', 'اسرع شخص يدز » { ️`🚰` } «',
        'اسرع شخص يدز » { ️`⛎` } «', 'اسرع شخص يدز » { ️`💮` } «', 'اسرع شخص يدز » { ️`➿` } «',
        'اسرع شخص يدز » { ️`🗿` } «', 'اسرع شخص يدز » { ️`💙` } «', 'اسرع شخص يدز » { ️`🍖` } «',
        'اسرع شخص يدز » { ️`🍕` } «', 'اسرع شخص يدز » { ️`🍟` } «', 'اسرع شخص يدز » { ️`🍄` } «',
        'اسرع شخص يدز » { ️`🌜` } «', 'اسرع شخص يدز » { ️`🌛` } «', 'اسرع شخص يدز » { ️`🌎` } «',
        'اسرع شخص يدز » { ️`💧` } «', 'اسرع شخص يدز » { ️`⚡` } «',
    ]
    if text in ["الاسرع", "الٲسرع", "اسرع", "أسرع"]:
        import random
        selected_prompt = random.choice(fast_emoji_prompts)
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': selected_prompt,
            'parse_mode': 'MARKDOWN', 'reply_to_message_id': message_id,
            'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Points for fast emoji solutions
    fast_emoji_solutions = {
        '😈', '🏦', '🏥', '🐢', '🐀', '🐁', '🐱', '🐩', '😨', '😴', '🔧', '🏇',
        '🗼', '🔨', '🎈', '🔛', '⏳', '🚰', '⛎', '💮', '➿', '🗿', '💙', '🍖',
        '🍕', '🍟', '🍄', '🌜', '🌛', '🌎', '💧', '⚡'
    }
    if text and text in fast_emoji_solutions:
        current_points = int(load_file_content(user_points_file, "0"))
        new_points = current_points + 1
        save_file_content(user_points_file, str(new_points))
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "🎉¦ مبروك لقد ربحت نقطه\n"
                f"🔖¦ اصبح لديك {{ {new_points} }} نقطه 🍃️\n"
            ),
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Emoji Meaning game ("معاني")
    emoji_meaning_prompts = [
        'اسرع واحد يدز { 😜 }', 'اسرع واحد يدز معنى السمايل يفوز » { 🚀 }',
        'اسرع واحد يدز معنى السمايل يفوز » { ⚽ }', 'اسرع واحد يدز معنى السمايل يفوز » { 🐜 }',
        'اسرع واحد يدز معنى السمايل يفوز » { 📙 }', 'اسرع واحد يدز معنى السمايل يفوز » { ⌚ }',
        'اسرع واحد يدز معنى السمايل يفوز » { 🐧 }', 'اسرع واحد يدز معنى السمايل يفوز » { 🐍 }',
        'اسرع واحد يدز معنى السمايل يفوز » { 🐈 }', 'اسرع واحد يدز معنى السمايل يفوز » { 🐒 }',
        'اسرع واحد يدز معنى السمايل يفوز » { 💜 }', 'اسرع واحد يدز معنى السمايل يفوز » { 🐄 }',
        'اسرع واحد يدز معنى السمايل يفوز » { 🍎 }', 'اسرع واحد يدز معنى السمايل يفوز » { 🐔 }',
        'اسرع واحد يدز معنى السمايل يفوز » { 🐇 }', 'اسرع واحد يدز معنى السمايل يفوز » { 🐟 }',
        'اسرع واحد يدز معنى السمايل يفوز » { 🐙 }', 'اسرع واحد يدز معنى السمايل يفوز » { 🐝 }',
        'اسرع واحد يدز معنى السمايل يفوز » { 🐅 }', 'اسرع واحد يدز معنى السمايل يفوز » { 🐫 }',
        'اسرع واحد يدز معنى السمايل يفوز » { 🐘 }',
    ]
    if text in ["معاني", "المعاني", "معأني"]:
        import random
        selected_prompt = random.choice(emoji_meaning_prompts)
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': selected_prompt,
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Points for emoji meaning solutions
    emoji_meaning_solutions = {
        'قمر', 'دجاجه', 'قرد', 'قط', 'ثعبان', 'قطه', 'برج', 'ساعه', 'كتاب', 'نمله', 'نملة',
        'كره', 'كرة', 'صاروخ', 'اخطبوط', 'فيل', 'جمل', 'نمر', 'نحله', 'قلب', 'بقره', 'بقرة',
        'تفاحه', 'بطريق', 'ارنب', 'سمكه', 'سمكة'
    }
    if text and text.lower() in emoji_meaning_solutions:
        current_points = int(load_file_content(user_points_file, "0"))
        new_points = current_points + 1
        save_file_content(user_points_file, str(new_points))
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "🎉¦ مبروك لقد ربحت نقطه\n"
                f"🔖¦ اصبح لديك {{ {new_points} }} نقطه 🍃️\n"
            ),
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Games list
    if text == "الالعاب":
        bot_request('sendMessage', {
            'chat_id': chat_id,
            'text': (
                "👤¦ اهلا بك عزيزي \n"
                "🚸¦ اليك قائمه الالعاب\n"
                "📬¦ الاسرع » لعبه تطابق السمايلات\n"
                "📛¦ معاني » لعبه معاني السمايلات\n"
                "🎭¦ ترتيب » لعبه ترتيب الكلمات"
            ),
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # Generic text responses
    response_texts = {
        "السلام عليكم": "وعليكم السلام اغاتي🌝👋 ",
        "السلامو عليكم": "وعليكم السلام اغاتي🌝👋 ",
        "سلام عليكم": "وعليكم السلام اغاتي🌝👋 ",
        "سلام الله عليكم": "وعليكم السلام اغاتي🌝👋 ",
        "السلام  عليكم ورحمة الله": "وعليكم السلام اغاتي🌝👋 ",
        "السلام عليكم ورحمه الله": "وعليكم السلام اغاتي🌝👋 ",
        "السلام عليكم ورحمة الله وبركاته": "وعليكم السلام اغاتي🌝👋 ",
        "السلام عليكم ورحمة الله تعالى وبركاته": "وعليكم السلام اغاتي🌝👋 ",
        "سلام عليكم كيفكم": "وعليكم السلام اغاتي🌝👋 ",
        "رابط حذف": "🌿¦ رابط حذف حـساب التيليگرام ↯\n📛¦ لتتندم فڪر قبل ڪلشي  \n👨🏽‍⚖️¦ بالتـوفيـق عزيزي ...\n🚸 ¦ـ  https://telegram.org/deactivate",
        "رابط الحذف": "🌿¦ رابط حذف حـساب التيليگرام ↯\n📛¦ لتتندم فڪر قبل ڪلشي  \n👨🏽‍⚖️¦ بالتـوفيـق عزيزي ...\n🚸 ¦ـ  https://telegram.org/deactivate",
        "اريد احذف الحساب": "🌿¦ رابط حذف حـساب التيليگرام ↯\n📛¦ لتتندم فڪر قبل ڪلشي  \n👨🏽‍⚖️¦ بالتـوفيـق عزيزي ...\n🚸 ¦ـ  https://telegram.org/deactivate",
        "ححذف": "🌿¦ رابط حذف حـساب التيليگرام ↯\n📛¦ لتتندم فڪر قبل ڪلشي  \n👨🏽‍⚖️¦ بالتـوفيـق عزيزي ...\n🚸 ¦ـ  https://telegram.org/deactivate",
        "ايديي": f" {from_id} ",
        "معرفي": f" @{user_username} ",
        "اسمي": f" {user_name} ",
        "بوت": "أسمي  السفاح المصري 🌸",
        "😔": "ليش الحلو ضايج ❤️🍃",
        "😳": "ها بس لا شفت خالتك الشكره 😳😹🕷",
        "😭": "لتبجي حياتي 😭😭",
        "😡": "ابرد  🚒",
        "😍": "يَمـه̷̐ إآلُحــ❤ــب يَمـه̷̐ ❤️😍",
        "😉": "😻🙈",
        "😋": "طبب لسانك جوه عيب 😌",
        "☹️": "لضوج حبيبي 😢❤️🍃",
        "هلو": "هلووات 😊🌹",
        "شكرا": "{ •• الـّ~ـعـفو •• } ",
        "مشكور": "{ •• الـّ~ـعـفو •• } ",
        "مح": "محات حياتي🙈❤",
        "تف": "عيب ابني/بتي اتفل/ي اكبر منها شوية 😌😹",
        "تخليني": "اخليك بزاويه 380 درجه وانته تعرف الباقي 🐸",
        "اكرهك": "ديله شلون اطيق خلقتك اني😾🖖🏿🕷",
        "باي": f"بايات حياتي 😍 {user_name}",
        "زاحف": "زاحف عله خالتك الشكره 🌝",
        "واو": "قميل 🌝🌿",
        "شكو ماكو": "غيرك/ج بل كلب ماكو يبعد كلبي😍❤️️",
        "شكو": "كلشي وكلاشي🐸تگـول عبالك احنـة بالشورجـة🌝",
        "معزوفه": "طرطاا طرطاا طرطاا 😂👌",
        "زاحفه": "لو زاحفتلك جان ماكلت زاحفه 🌝🌸",
        "حفلش": "افلش راسك 🤓",
        "ضوجه": "شي اكيد الكبل ماكو 😂 لو بعدك/ج مازاحف/ة 🙊😋",
        "غنزدبليي": "اللهم عذب المدرسين 😢 منهم الاحياء والاموات 😭🔥 اللهم عذب ام الانكليزي 😭💔 وكهربها بلتيار الرئيسي 😇 اللهم عذب ام الرياضيات وحولها الى غساله بطانيات 🙊 اللهم عذب ام الاسلاميه واجعلها بائعة الشاميه 😭🍃 اللهم عذب ام العربي وحولها الى بائعه البلبي اللهم عذب ام الجغرافيه واجعلها كلدجاجه الحافية اللهم عذب ام التاريخ وزحلقها بقشره من البطيخ وارسلها الى المريخ اللهم عذب ام الاحياء واجعلها كل مومياء اللهم عذب المعاون اقتله بلمدرسه بهاون 😂😂😂",
    }
    if text in response_texts:
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': response_texts[text],
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

    # " السفاح المصري" random response
    if text == "السفاح المصري":
        import random
        random_responses = [
            'سويت هواي شغلات سخيفه بحياتي بس عمري مصحت على واحد وكلتله انجب 😑',
            'نعم حبي 😎', 'اشتعلو اهل فير شتريد 😠',
            'لك فداك فير حبيبي انت اموووح 💋',
            'بوooooo 👻 ها ها فزيت شفتك شفتك لا تحلف 😂',
            'هياتني اجيت 🌚❤️',
            'راجع المكتب حبيبي عبالك فير سهل تحجي ويا 😒',
            'باقي ويتمدد 😎',
            'لك دبدل ملابسي اطلع برااااا 😵😡 ناس متستحي',
            'دا اشرب جاي تعال غير وكت 😌',
            'هوه غير يسكت عاد ها شتريد 😷',
            'انت مو اجيت البارحه تغلط عليه ✋🏿😒'
        ]
        bot_request('sendMessage', {
            'chat_id': chat_id, 'text': random.choice(random_responses),
            'reply_to_message_id': message_id, 'reply_markup': json.dumps(DEV_BUTTONS)
        })

def main():
    offset = 0
    while True:
        try:
            updates = bot_request('getUpdates', {'offset': offset, 'timeout': 30})
            if updates and updates.get('ok') and updates.get('result'):
                for update in updates['result']:
                    offset = update['update_id'] + 1
                    handle_message(update)
            time.sleep(1) # Polling interval
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(5) # Wait before retrying on error

if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/filter'):
        os.makedirs('data/filter')
    
    # Initialize files if they don't exist
    for f in ["data/groups.txt", "data/memo.txt", "data/memomemb.txt", "data/memousr.txt", 
              "data/namebot.txt", "data/sudo.txt", "mode.txt", "dev_start.txt", "msgs.json", "data/left.txt"]:
        if not os.path.exists(f):
            if f.endswith(".json"):
                save_file_content(f, "{}")
            else:
                save_file_content(f, "")

    print("Bot started...")
    main()
#