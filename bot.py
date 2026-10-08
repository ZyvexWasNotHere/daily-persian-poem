import os
import random
import asyncio
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# شعرهای فعلی
poems = [
    ("حافظ", "دوش دیدم که ملائک در میخانه زدند\nگل آدم بسرشتند و به پیمانه زدند"),
    ("سعدی", "بنی آدم اعضای یکدیگرند\nکه در آفرینش ز یک گوهرند"),
    ("فردوسی", "توانا بود هر که دانا بود\nز دانش دل پیر برنا بود"),
    ("مولانا", "این قافله عمر عجب می‌گذرد\nدریاب دمی که با طرب می‌گذرد"),
]


# =========================
# منوی اصلی
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 شعر امروز", callback_data="today")],
        [InlineKeyboardButton("👑 پنل مالک", callback_data="owner_panel")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📜 به ربات Daily Poem خوش آمدید!\n\n"
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup
    )


# =========================
# بررسی مالک
# =========================

def is_owner(user_id):
    return str(user_id) == str(CHAT_ID)


# =========================
# نمایش شعر
# =========================

async def show_poem(update: Update):
    query = update.callback_query
    await query.answer()

    poet, poem = random.choice(poems)

    await query.message.reply_text(
        f"📜 شعر روز\n\n"
        f"✍️ {poet}\n\n"
        f"{poem}"
    )


# =========================
# پنل مالک
# =========================

async def owner_panel(update: Update):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if not is_owner(user_id):
        await query.message.reply_text(
            "⛔ شما مالک ربات نیستید."
        )
        return

    keyboard = [
        [InlineKeyboardButton("➕ اضافه کردن شعر", callback_data="add_poem")],
        [InlineKeyboardButton("📚 مدیریت شعرها", callback_data="manage_poems")],
        [InlineKeyboardButton("📊 آمار ربات", callback_data="stats")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "👑 پنل مالک\n\n"
        "به پنل مدیریت Daily Poem خوش آمدید.",
        reply_markup=reply_markup
    )


# =========================
# مدیریت دکمه‌ها
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "today":
        await show_poem(update)

    elif query.data == "owner_panel":
        await owner_panel(update)

    elif query.data == "add_poem":
        if not is_owner(query.from_user.id):
            await query.answer("⛔ دسترسی ندارید.", show_alert=True)
            return

        await query.answer()

        await query.message.reply_text(
            "➕ بخش اضافه کردن شعر\n\n"
            "این قسمت را در مرحله بعد کامل می‌کنیم."
        )

    elif query.data == "manage_poems":
        if not is_owner(query.from_user.id):
            await query.answer("⛔ دسترسی ندارید.", show_alert=True)
            return

        await query.answer()

        await query.message.reply_text(
            "📚 مدیریت شعرها\n\n"
            "این قسمت را در مرحله بعد اضافه می‌کنیم."
        )

    elif query.data == "stats":
        if not is_owner(query.from_user.id):
            await query.answer("⛔ دسترسی ندارید.", show_alert=True)
            return

        await query.answer()

        await query.message.reply_text(
            f"📊 آمار ربات\n\n"
            f"تعداد شعرهای فعلی: {len(poems)}"
        )

    elif query.data == "back":
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("📖 شعر امروز", callback_data="today")],
            [InlineKeyboardButton("👑 پنل مالک", callback_data="owner_panel")],
        ]

        await query.message.reply_text(
            "📜 منوی اصلی:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================
# ارسال شعر روزانه
# =========================

def send_daily_poem():
    poet, poem = random.choice(poems)

    message = f"""📜 شعر روز

✍️ {poet}

{poem}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    response.raise_for_status()

    print("شعر روزانه با موفقیت ارسال شد.")


# =========================
# اجرای ربات
# =========================

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("ربات تعاملی شروع شد.")

    application.run_polling()


if __name__ == "__main__":
    main()
