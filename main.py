import os
import logging
from datetime import datetime
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your OpenWeatherMap API key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Replace with your Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text('Hi! I am your weather and time bot. Use /weather <city> to get weather info and /time <city> to get local time.')


def get_weather(city: str) -> str:
    """Fetch weather information for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't fetch the weather information. Please check the city name."


def weather(update: Update, context: CallbackContext) -> None:
    """Send weather information for the requested city."""
    if context.args:
        city = ' '.join(context.args)
        weather_info = get_weather(city)
        update.message.reply_text(weather_info)
    else:
        update.message.reply_text("Please provide a city name. Usage: /weather <city>")


def get_time(city: str) -> str:
    """Fetch local time for a given city."""
    url = f"http://worldtimeapi.org/api/timezone/{city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        datetime_str = data['datetime']
        local_time = datetime.fromisoformat(datetime_str[:-1])
        return f"The local time in {city} is {local_time.strftime('%Y-%m-%d %H:%M:%S')}."
    else:
        return "Sorry, I couldn't fetch the time information. Please check the city name or format."


def time(update: Update, context: CallbackContext) -> None:
    """Send local time for the requested city."""
    if context.args:
        city = ' '.join(context.args)
        time_info = get_time(city)
        update.message.reply_text(time_info)
    else:
        update.message.reply_text("Please provide a city name. Usage: /time <city>")


def main() -> None:
    """Start the bot."""
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather))
    dispatcher.add_handler(CommandHandler("time", time))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()