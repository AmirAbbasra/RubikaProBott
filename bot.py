
import random
import re
from rubka import Robot

TOKEN = "توکن_ربات_اینجا"

bot = Robot(token=TOKEN)
pending_quiz = {}

challenges = [
    "🎯 یه حقیقت جالب درباره خودت بگو!",
    "😂 خنده‌دارترین خاطره‌ات رو تعریف کن!",
    "💙 سه تا ایموجی برای حالت بفرست!",
    "✨ اگه یه آرزو داشتی چی بود؟",
    "😎 بهترین خاطره‌ات با دوستات چیه؟"
]

quizzes = [
    ("پایتخت ایران کجاست؟", ["تهران", "شیراز", "تبریز"], 1),
    ("۵ ضربدر ۶ چند می‌شود؟", ["۲۵", "۳۰", "۳۵"], 2),
    ("سیاره سرخ کدام است؟", ["زمین", "مریخ", "زهره"], 2),
    ("بزرگ‌ترین سیاره منظومه شمسی؟",
     ["مشتری", "زمین", "عطارد"], 1)
]

answers = {
    "سلام": "سلام رفیق! 👋 خوبی؟",
    "خوبی": "مرسی، خوبم! تو چطوری؟ 😎",
    "سلام خوبی": "سلام! مرسی، تو خوبی؟ ❤️",
    "چه خبر": "سلامتی! تو چه خبر؟ 😁",
    "چخبر": "سلامتی رفیق! 😎",
    "خوبی چخبر": "خوبم، تو چه خبر؟ 💙",
    "صبح بخیر": "صبح تو هم بخیر ☀️",
    "شب بخیر": "شب تو هم بخیر 🌙",
    "مرسی": "خواهش می‌کنم ❤️",
    "ممنون": "قربونت! 😁",
    "خداحافظ": "فعلاً رفیق، مراقب خودت باش 👋",
}

def clean(text):
    text = text.strip().lower()
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = re.sub(r"[!！?؟.,،]+", "", text)
    return re.sub(r"\s+", " ", text)

@bot.on_message()
def handler(bot, message):
    text = message.text
    if not text:
        return

    msg = clean(text)
    chat_id = message.chat_id
    sender = str(message.sender_id)
    key = (str(chat_id), sender)

    # بررسی پاسخ کوییز
    if key in pending_quiz and msg in ("1", "2", "3"):
        correct = pending_quiz.pop(key)
        if int(msg) == correct:
            message.reply("✅ آفرین! جواب درست بود! 🎉")
        else:
            message.reply(
                f"❌ جواب اشتباه بود!\n"
                f"پاسخ درست: گزینه {correct}"
            )
        return

    if msg in ("/start", "شروع", "سلام ربات"):
        message.reply(
            "🤖 سلام! به ربات همه‌کاره خوش اومدی!\n\n"
            "دستورها:\n"
            "سلام | خوبی | چه خبر\n"
            "چالش | کوییز | کمک\n"
            "کجایی"
        )
        return

    if msg in ("کمک", "/help", "راهنما"):
        message.reply(
            "📚 راهنمای ربات\n"
            "👋 گفت‌وگوی فارسی\n"
            "🎯 چالش\n"
            "🧠 کوییز\n"
            "📍 کجایی؟"
        )
        return

    if "کجایی" in msg:
        message.reply("سر قبر آقات 😂💀")
        return

    if msg in ("چالش", "چالش بده", "یه چالش"):
        message.reply(random.choice(challenges))
        return

    if msg in ("کوییز", "سوال", "سؤال", "مسابقه"):
        question, options, correct = random.choice(quizzes)
        pending_quiz[key] = correct

        choices = "\n".join(
            f"{i + 1}. {option}"
            for i, option in enumerate(options)
        )

        message.reply(
            f"🧠 کوییز!\n{question}\n\n"
            f"{choices}\n\n"
            "شماره گزینه درست رو بفرست."
        )
        return

    if msg in answers:
        message.reply(answers[msg])
        return

    if "😂" in text or "🤣" in text:
        message.reply("چیه رفیق؟ 😂 ما رو هم بخندون!")
        return

    if "دوستت دارم" in msg:
        message.reply("چه مهربون! ❤️")
        return

    if msg in ("خسته نباشی", "دمت گرم", "دمتگرم"):
        message.reply("قربونت رفیق! 💙")
        return

    message.reply("هنوز اینو یاد نگرفتم 😅 «کمک» رو بفرست.")

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    bot.run()
