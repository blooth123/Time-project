

# siimple Bot to send timed Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import picamera
import time
import telegram
import sys, serial,time
import RPi.GPIO as GPIO
from telegram.ext import Updater, CommandHandler, Job
import logging
from sense_hat import SenseHat

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)
camera = picamera.PiCamera()

pirPin = 4
GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def takePhoto():
    camera.resolution = (2592,1944)
    camera.framerate = 15
    camera.start_preview()
    camera.capture('image.jpg')
    camera.stop_preview()
    camera.close()

#def telegram():
   # chat_id = 1118932942
   # bot = telegram.Bot('1324949291:AAG2ezp_UlGNX6qGELySUlM88Z5WIxfqQ_o')
   # bot.sendPhoto(chat_id=chat_id,photo=open('./image.jpg', 'rb'))
   # bot.sendMessage(chat_id=chat_id,text='Motion Detected!')
   # time.sleep(3)

def white(update, context):
    sense = SenseHat()

    x = [255, 0, 0]
    o = [255, 255, 255]
    w = [0, 84, 255]
    question_mark = [
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, x, x, o, o, o,
    o, o, x, x, x, x, o, o,
    o, o, w, w, w, w, o, o,
    o, o, o, w, w, o, o, o,
    o, o, o, o, o, o, o, o,
    o, o, o, o, o, o, o, o
    ]
    sense.set_pixels(question_mark)

def Red(update, context):
    sense = SenseHat()
    time.sleep(2)
    sense.clear(255, 0, 0)

def dark(update, context):
    sense = SenseHat()
    sense.clear(0, 0, 0)

def start(update,context):
    chat_id = 1118932942
    bot = telegram.Bot('1324949291:AAG2ezp_UlGNX6qGELySUlM88Z5WIxfqQ_o')
    bot = telegram.Bot('1140833243:AAG93wcLftgl8Iv8a1Gr16zyZycCapzS_Q0')

    update.message.reply_text('Security System On')
    while True:
        if GPIO.input(pirPin) == GPIO.LOW:
            try:
                white()
                takePhoto()
                Red()
                #telegram()
                bot.sendPhoto(chat_id=chat_id,photo=open('./image.jpg', 'rb'))
                bot.sendMessage(chat_id=chat_id,text='Motion Detected!')
            except:
                camera.stop_preview()
        time.sleep(5)

def off(update, context):
    dark()
    #chat_id = 1118932942
    #bot = telegram.Bot('1324949291:AAG2ezp_UlGNX6qGELySUlM88Z5WIxfqQ_o')

    update.message.reply_text('Security System OFF')
    return start()


def alarm(bot, job):
    """Function to send the alarm message"""
	#camera.start_preview(fullscreen=False, window(100,20,640,480))
	#time.sleep(2)
    takePhoto()
    time.sleep(1)
	#camera.stop_preview()
    bot.sendPhoto(job.context, photo=open('./image.jpg', 'rb'))
    bot.sendMessage(job.context, text='Worked!')


def set(bot, update, args, job_queue, chat_data):
    """Adds a job to the queue"""
    chat_id =1118932942
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = Job(alarm, due, repeat=False, context=chat_id)
        chat_data['job'] = job
        job_queue.put(job)

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(bot, update, chat_data):
    """Removes the job if the user changed their mind"""

    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("1324949291:AAG2ezp_UlGNX6qGELySUlM88Z5WIxfqQ_o",use_context=True)
    updater = Updater("1140833243:AAG93wcLftgl8Iv8a1Gr16zyZycCapzS_Q0", use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('off', off))
    #dp.add_handler(CommandHandler("help", on))
    #dp.add_handler(CommandHandler("set", set,
    #                              pass_args=True,
    #                              pass_job_queue=True,
    #                              pass_chat_data=True))
    #dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
