#encoding=utf-8
import os
import urllib
import urllib2
import json
import sys
rootpath = os.path.split(os.path.realpath(__file__))[0] + "/.."
rootpath1 = rootpath + "/speech_recognition"
rootpath2 = rootpath + "/tts"
sys.path.insert(0, rootpath1)
sys.path.insert(0, rootpath2)
import speech_recognition as sr
import tts_manager

class SpeechMain():
    def __init__(self):
        self.output_text = None

    def speech2text(self,source_flag_or_filename_or_fileobject = 0):
        """

        :param source_flag_or_filename_or_fileobject: 语音源的标识，0（默认）代表系统麦克风输入。如果语音源为从文件读取，应为文件路径字符串或file-like object，如``io.BytesIO``。
        :return:
        """
        r = sr.Recognizer()
        if source_flag_or_filename_or_fileobject == 0:
            s = sr.Microphone()
        else:
            s = sr.AudioFile(source_flag_or_filename_or_fileobject)


        try:
            print('根据环境噪音调整能量阈值中，请稍候...')
            with s as source: r.adjust_for_ambient_noise(source)
            print("设置最小能量阈值为{}".format(r.energy_threshold))
            print("请说话：")
            with s as source: text_list = r.listen_and_slice_and_recognize(source)
        except KeyboardInterrupt:
            pass

        return ' '.join(text_list)



    def request_wordbot(self,input_text):
        url = 'http://47.93.118.55:8080/wordbot'
        userid = 'Li xiufei'
        appid = '51b500fa-2662-4a24-9180-2650ae8ad41b'
        data = {
            'appid': appid,
            'userid': userid,
            'text': input_text,
        }
        post_data = urllib.urlencode(data)
        request = urllib2.Request(url,post_data)
        response = urllib2.urlopen(request)
        res = json.loads(response.read())
        if res['retcode']==0:
            return res['body']
        else:
            return res['describe']

    def text2speech(self,text):
        ttsm = tts_manager.TTSManger()
        ttsm.text = text
        ttsm.begin_tts()


if __name__=="__main__":
    sm = SpeechMain()
    input_text = sm.speech2text()
    print input_text
    output_text = sm.request_wordbot(input_text)
    print output_text
    sm.text2speech(output_text)
