import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# --- Font Data ---
FONTS = {
    "𝕭𝖔𝖑𝖉": ("𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",
              "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟",
              "𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫"),
    "𝓢𝓬𝓻𝓲𝓹𝓽": ("𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
                "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃",
                "0123456789"),
    "𝙼𝚘𝚗𝚘": ("𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
              "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣",
              "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"),
    "𝔉𝔯𝔞𝔨𝔱𝔲𝔯": ("𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",
                  "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷",
                  "0123456789"),
}

def convert_text(text: str, font_key: str):
    """Convert text to the chosen Unicode font."""
    if font_key not in FONTS:
        return text
    
    upper_map, lower_map, digit_map = FONTS[font_key]
    result = []
    
    for char in text:
        if 'A' <= char <= 'Z':
            result.append(upper_map[ord(char) - ord('A')])
        elif 'a' <= char <= 'z':
            result.append(lower_map[ord(char) - ord('a')])
        elif '0' <= char <= '9':
            result.append(digit_map[ord(char) - ord('0')])
        else:
            result.append(char)
            
    return "".join(result)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome!*\n\n"
        "Send me any text and choose a font to transform it instantly!\n"
        "Use the buttons below to select a style.",
        reply_markup=font_selection_keyboard(),
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*How to use:*\n"
        "1. Send me any message with plain text.\n"
        "2. Select a font style from the buttons I reply with.\n\n"
        "Or, just type /start to see the keyboard again.",
        parse_mode="Markdown"
    )

async def fonts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Choose a font style!",
        reply_markup=font_selection_keyboard()
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Font Style Bot*\n\n"
        "This bot is designed to make your messages look unique using Unicode fonts.\n"
        "It's simple, fast, and fully respects Telegram's policies.\n\n"
        "Built with ❤️ for the Telegram community."
    )

def font_selection_keyboard():
    keyboard = []
    for font_name in FONTS.keys():
        keyboard.append([InlineKeyboardButton(font_name, callback_data=font_name)])
    return InlineKeyboardMarkup(keyboard)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    selected_font = query.data
    context.user_data['selected_font'] = selected_font
    await query.edit_message_text(
        f"✅ Font selected: *{selected_font}*\n\nNow, send me a message to transform!",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if 'selected_font' not in context.user_data:
        await update.message.reply_text(
            "Please select a font style first!",
            reply_markup=font_selection_keyboard()
        )
        return
        
    selected_font = context.user_data['selected_font']
    converted = convert_text(text, selected_font)
    
    await update.message.reply_text(
        f"*{selected_font} Style:*\n\n{converted}",
        parse_mode="Markdown",
        reply_markup=font_selection_keyboard()
    )

def main():
    # Set up logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Get token from environment
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        logging.error("No TELEGRAM_TOKEN set in environment variables!")
        return

    # Create the Application (FIXED: Using Application instead of ApplicationBuilder)
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('fonts', fonts_command))
    application.add_handler(CommandHandler('about', about_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logging.info("🚀 Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
