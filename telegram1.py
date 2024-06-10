from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import logging
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '7208251579:AAEH48lAhlbf96ecoN4tHZ-GlJ7hhe02PvM'
QUESTION, ANSWER = range(2)

users_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    users_data[user.id] = {'score': 0}
    await update.message.reply_text('Welcome to the Math Game! Type /play to start playing.')

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    question, answer = generate_math_problem()
    users_data[user.id]['current_answer'] = answer
    await update.message.reply_text(f'What is {question}?')
    return ANSWER

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_data = users_data.get(user.id, {})
    if not user_data:
        await update.message.reply_text('Please start the game first by typing /play.')
        return ConversationHandler.END
    
    try:
        user_answer = int(update.message.text)
    except ValueError:
        await update.message.reply_text('Please enter a valid number.')
        return ANSWER

    if user_answer == user_data['current_answer']:
        user_data['score'] += 1
        await update.message.reply_text(f'Correct! Your current score is {user_data["score"]}. Type /play for another question.')
    else:
        await update.message.reply_text(f'Wrong answer. The correct answer was {user_data["current_answer"]}. Your final score is {user_data["score"]}. Type /play to try again.')
        user_data['score'] = 0
    
    return ConversationHandler.END

def generate_math_problem():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operation = random.choice(['+', '-', '*'])
    if operation == '+':
        question = f'{a} + {b}'
        answer = a + b
    elif operation == '-':
        question = f'{a} - {b}'
        answer = a - b
    else:
        question = f'{a} * {b}'
        answer = a * b
    return question, answer

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Game cancelled. Type /play to start a new game.')
    return ConversationHandler.END

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('play', play)],
        states={
            ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
