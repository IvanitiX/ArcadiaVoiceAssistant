import subprocess, os
from time import sleep
from arcadia import instances, settings


class MainLoop():
    def main(self):
        transcript = instances.SPEECH_RECOGNIZER.recognize_stream()
        keyword_separator = ''
        for keyword in settings.BOT_NAME_VARIANTS:
            if  keyword in transcript and keyword_separator == '':
                keyword_separator = keyword
        if keyword_separator != '':
            transcript = transcript.split(keyword_separator,1)[-1]
            response = instances.CHATBOT.make_petition(transcript)
            for item in response:
                if '[>]' in item:
                    url = item.split('[>] ',1)[-1]
                    subprocess.Popen(instances.MEDIA_PLAYER.play(url),
                                    stdout=open('/dev/null', 'w'),
                                    preexec_fn=os.setpgrp)
                else:
                    instances.TEXT_TO_SPEECH_GENERATOR.generate_voice(item)
                    sleep(2)
                    instances.RESPONSE_PLAYER.play(f"{settings.TESTING_FILES}/nano.wav")