#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Speech to Scratch
  April 2020
  Gal Savranevski from base code of Hiroaki Kawashima and SpeechToEnglish project of rdb lab
  Description:
    Create  server which accpets scratch requests
    and Connects to voice recognition server as client
"""

import urllib
import asyncio
from aiohttp import web
import speech_recognition as sr

ERROR = "תקלה בזיהוי"
UNDEFINED = "לא מוגדר"
FLIP_FWD = 'פליפ קידמי'
FLIP_BWD = 'פליפ אחורי'
FLIP_LEFT = 'פליפ שמאלי'
FLIP_RIGHT = 'פליפ ימיני'
RIGHT_1 = 'ימין'
RIGHT_2 = 'ימינה'
LEFT_1 = 'שמאל'
LEFT_2 = 'שמאלה'
UP = 'למעלה'
DOWN = 'למטה'
STRAIGHT = 'ישר'
BACK_1 = 'אחורה'
BACK_2 = 'אחור'
TAKE_OFF_1 = 'המראה'
TAKE_OFF_2 = 'להמריא'
LAND_1 = 'נחיתה'
LAND_2 = 'נחת'
LAND_3 = 'לנחות'
TURN1 = 'סיבוב'
TURN_2 = 'להסתובב'
TURN_3 = 'הסתובב'
TURN_4 = 'תסתובב'


def speech_to_hebrew_and_recognize(timeToWait):
    import google.cloud.speech

    r = sr.Recognizer()
    r.energy_threshold = 200
    defining_operation_words = list()
    # Append the pairs of words to the defining_operation_words list
    defining_operation_words.append(FLIP_FWD)
    defining_operation_words.append(FLIP_BWD)
    defining_operation_words.append(FLIP_LEFT)
    defining_operation_words.append(FLIP_RIGHT)
    defining_operation_words.append(RIGHT_1)
    defining_operation_words.append(RIGHT_2)
    defining_operation_words.append(LEFT_1)
    defining_operation_words.append(LEFT_2)
    defining_operation_words.append(UP)
    defining_operation_words.append(DOWN)
    defining_operation_words.append(STRAIGHT)
    defining_operation_words.append(BACK_1)
    defining_operation_words.append(BACK_2)
    defining_operation_words.append(TAKE_OFF_1)
    defining_operation_words.append(TAKE_OFF_2)
    defining_operation_words.append(LAND_1)
    defining_operation_words.append(LAND_2)
    defining_operation_words.append(LAND_3)
    defining_operation_words.append(TURN1)
    defining_operation_words.append(TURN_2)
    defining_operation_words.append(TURN_3)
    defining_operation_words.append(TURN_4)

    # decode words to numbers
    i = 0
    word_to_num_dict = dict()
    word_to_num_dict[ERROR] = i
    i = i + 1
    word_to_num_dict[UNDEFINED] = i
    i = i + 1
    for word in defining_operation_words:
        word_to_num_dict[word] = i
        i = i + 1

    with sr.Microphone() as source:
        try:
            print("start talking")
            # Starts listening on user's microphone
            # print(r.energy_threshold)
            # r.adjust_for_ambient_noise(source)
            # print(r.energy_threshold)
            audio = r.listen(source, timeout=timeToWait, phrase_time_limit=3)
            # r.adjust_for_ambient_noise(source)
            print("End listening")

            # Recognizing what the user said in English
            res = r.recognize_google(audio, language='he', show_all=True)
            if (not res):
                print(f"error in recognize_google {ERROR} , code ={word_to_num_dict[ERROR]}")
                return word_to_num_dict[ERROR]
            alt_list = res['alternative']
            print(alt_list)
            for operation_word in defining_operation_words:
                for d in alt_list:
                    val = str(d['transcript'])
                    if operation_word in val:
                        num = word_to_num_dict[operation_word]
                        print(f"operational word recognized {operation_word} , code ={num}")
                        return num
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print(f"operational word not recognized {UNDEFINED} , code ={word_to_num_dict[UNDEFINED]}")
            return word_to_num_dict[UNDEFINED]  # List of words that defining the applications

    print(f"operational word not recognized {UNDEFINED} , code ={word_to_num_dict[UNDEFINED]}")
    return word_to_num_dict[UNDEFINED]


class S2SpeechRecognition:
    """ scratch 2 speech recognition server """

    def __init__(self):
        self.helper_host = "127.0.0.1"
        self.helper_port = 50211  # port of this helper

        self.max_waittime = 10  # max wait sec for recognition
        self.min_waittime = 1
        self.check_cycle = 0.5  # seconds for one awaytio.sleep cycle

        self.waiting_commands = set()  # waiting block in scratch
        self.pollresponse_template = "template"
        self.pollresponse_flush = "response"

        self.poll_flush_request = False
        self.recog_request = False
        self.heard_sentence = "undefined"

    def clear_recog(self):
        self.heard_sentence = "undefined"

    def start_recog(self, waittime):
        res = speech_to_hebrew_and_recognize(waittime)
        self.heard_sentence = res
        self.recog_request = False
        print(res)

    async def recogwait(self, request):
        """ wait until either something is recognized 
            or waittime elapses
        """
        try:
            val = int(request.match_info['waittime'])
        except ValueError:
            print("Ignored. Not a number: ", request.match_info['waittime'])
            return web.Response(text="failed")
        command_id = request.match_info['command_id']
        self.waiting_commands.add(command_id)
        if val > self.max_waittime:
            self.waittime = self.max_waittime
        elif val < self.min_waittime:
            self.waittime = self.min_waittime
        else:
            waittime = val
        print("recogwait: ", waittime)

        # request recognition and wait for waittime
        self.recog_request = True
        self.clear_recog()
        self.create_pollresponse_flush()
        elapsedtime = 0
        self.start_recog(waittime)  # Start recognition
        while self.recog_request and elapsedtime < waittime:
            await asyncio.sleep(self.check_cycle)
            elapsedtime += self.check_cycle
        self.recog_request = False
        self.waiting_commands.remove(command_id)
        print("send ok ")
        return web.Response(text='ok')

    def create_pollresponse_flush(self):
        """ create a poll response for flushing variables in the scratch """
        text = "heardsentence\n"
        self.pollresponse_flush = text
        self.poll_flush_request = True

    async def poll(self, request):
        """ response to polling from scratch """
        text = ""
        if self.poll_flush_request:
            text += self.pollresponse_flush
            self.poll_flush_request = False
        else:
            text += "heardsentence " + str(self.heard_sentence) + "\n"
        text += "_busy "
        text += " ".join(self.waiting_commands)
        # print(text)  # for debug
        return web.Response(text=text)

    async def crossdomain(self, request):
        """ response to crossdomain policy request """
        text = '<cross-domain-policy>'
        text += '<allow-access-from domain="*" to-ports="' + str(self.helper_port) + '"/>'
        text += '</cross-domain-policy>'
        return web.Response(text=text)

    def main(self):
        """ launch server"""
        loop = asyncio.get_event_loop()

        self.create_pollresponse_flush()

        # create server for scratch
        app = web.Application(loop=loop)
        app.router.add_get("/recogwait/{command_id}/{waittime}", self.recogwait)
        app.router.add_get("/poll", self.poll)
        app.router.add_get("/crossdomain.xml", self.crossdomain)
        scratch_server = loop.create_server(app.make_handler(), self.helper_host, self.helper_port)

        try:
            loop.run_until_complete(asyncio.wait({scratch_server}))
            loop.run_forever()  # until loop.stop()
        finally:
            loop.close()


if __name__ == '__main__':
    s2SpeechRecognition = S2SpeechRecognition()
    s2SpeechRecognition.main()
