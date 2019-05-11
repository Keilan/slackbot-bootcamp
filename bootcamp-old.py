import sys
import json
import time
import random
import datetime

from pytz import timezone

import requests


# Settings
url = 'https://hooks.slack.com/services/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'

exercises = {
    'Plank': {'range': (20, 50), 'unit': 'second'},
    'Wall Sit': {'range': (40, 90), 'unit': 'second'},
    'Push Ups': {'range': (5, 15), 'unit': None},
    'Calf Raises': {'range': (25, 50), 'unit': None},
    'Crunches': {'range': (15, 25), 'unit': None},
    'Stretch': {'range': (60, 120), 'unit': 'second'},
    'Lunges': {'range': (10, 25), 'unit': None}
}

message_timezone = 'MST'
next = (50, 75)
night = 18


def generate_message(minutes_to_next=None):
    """
    Using the list of exercises, this function generates a new exercise message. Optionally it
    takes a minutes_to_next parameter which it uses to add an indication of when the next exercise
    will take place.
    """
    # Randomly select an exercise and a number of repetitions
    exercise, data = random.choice(exercises.items())
    repetitions = random.randint(*data['range'])

    # Prepare the message string
    unit_string = ' ' + data['unit'] if data['unit'] else ''
    text = '{}{} {} RIGHT NOW!'.format(repetitions, prefix, exercise)

    # Add the next exercise indication
    if minutes_to_next is not None:
        current_time = datetime.datetime.now(timezone('UTC'))
        next_time = (now.astimezone(timezone(message_timezone)) +
                     datetime.timedelta(minutes=minutes_to_next))
        next_text = 'NEXT EXERCISE AT {}'.format(time.strftime('%H:%M'))
        text += '\n' + next_text

    return text


def postMessage():
    exercise = random.choice(exercises.keys())
    properties = exercises[exercise]
    number = random.randint(properties['range'][0], properties['range'][1])
    prefix = '' if not properties['unit'] else ' {}'.format(properties['unit'])
    wait = random.randint(next[0], next[1])
    now = datetime.datetime.now(timezone('UTC'))
    time = (now.astimezone(timezone('MST')) + datetime.timedelta(minutes=wait))

    text = '<!channel> {}{} {} RIGHT NOW!'.format(number, prefix, exercise)
    if time.hour < night:
        text += '\nNEXT THING AT {}'.format(time.strftime('%H:%M'))

    #print "Posting {}".format(text)

    payload = {'text': text}
    r = requests.post(url, data=json.dumps(payload))

    #if r.status_code != 200:
        #print r.content

    return wait


def startLoop():
    while True:
        # Post a new message
        wait = postMessage()

        assert wait > 5

        #Heartbeat every 60 seconds to prevent program from terminating
        for _ in xrange(wait):
            time.sleep(60)
            sys.stdout.write('/\\_')

        sys.stdout.write('\n')

        #Stop at Night
        now = datetime.datetime.now(timezone('UTC'))
        if now.astimezone(timezone('MST')).hour >= night:
            text = 'I\'m out. PEACE Y\'ALL'

            #print "Posting {}".format(text)
            payload = {'text': text}
            r = requests.post(url, data=json.dumps(payload))
            exit()


if __name__ == '__main__':
    generate_message()
    #startLoop()
