import requests
import os
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Get token and chat ID from Railway environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

# Get top meme coins from pump.fun
def get_pumpfun_data():
    url = "https://client-api-2-phi.vercel.app/token/list"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Filter and send alerts
def check_graduating_memecoins():
    coins = get_pumpfun_data()
    for coin in coins[:10]:  # Limit to top 10 coins
        try:
            name = coin.get('name')
            symbol = coin.get('symbol')
            market_cap = float(coin.get('marketCapUsd', 0))
            liquidity = float(coin.get('liquidityUsd', 0))
            holders = coin.get('holders', 0)
            address = coin.get('address')

            if market_cap > 50000 and liquidity > 5000 and holders > 100:
                message = f"""🚀 *Graduating Meme Coin Alert!*
*Name:* {name} (${symbol})
*Market Cap:* ${int(market_cap):,}
*Liquidity:* ${int(liquidity):,}
*Holders:* {holders}
[View on pump.fun](https://pump.fun/{address})
"""
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        except Exception as e:
            print(f"Error parsing coin: {e}")

# Respond to /start
def start(update, context):
    update.message.reply_text("Solana Meme Coin Bot is Live ✅")

# Run the bot
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    print("Bot is running...")

    while True:
        check_graduating_memecoins()
        time.sleep(60)  # Wait 60 seconds between checks

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()