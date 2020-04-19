import speech_recognition as sr


def speech_to_english_and_recognize():

    import google.cloud.speech

    r = sr.Recognizer()
    r.energy_threshold = 1000
    defining_operation_words = list()
    # Append the pairs of words to the defining_operation_words list
    defining_operation_words.append('right')
    defining_operation_words.append('left')
    defining_operation_words.append('up')
    defining_operation_words.append('down')
    with sr.Microphone() as source:
        try:
            print("start talking")
            # Starts listening on user's microphone
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            print("End listening")

            # Recognizing what the user said in English
            res = r.recognize_google(audio, language='en-US', show_all=True)
            if(not res) :
                return "undefined"
            alt_list = res['alternative']
            print(alt_list)
            for d in alt_list:
                val = d['transcript']
                split_sentence = val.split()
                for word in split_sentence:
                    if word in defining_operation_words:
                        return word
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return "undefined"  # List of words that defining the applications

    return "undefined"

if __name__ == '__main__':
    for i in range(1,20):
        print(speech_to_english_and_recognize())
