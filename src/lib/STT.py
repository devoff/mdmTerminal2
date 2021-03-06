
import hashlib
import json
import subprocess
import time
from io import BytesIO

import requests
from speech_recognition import AudioData

from utils import REQUEST_ERRORS, UnknownValueError
from .proxy import proxies
from .yandex_utils import requests_post, xml_yandex

__all__ = ['Yandex', 'YandexCloud', 'PocketSphinxREST']


class BaseSTT:
    BUFF_SIZE = 1024

    def __init__(self, url, audio_data: AudioData,
                 headers=None, convert_rate=None, convert_width=None, proxy_key=None, **kwargs):
        self._text = None
        self._rq = None
        self._url = url
        self._convert_rate = convert_rate
        self._convert_width = convert_width
        self._audio = self._get_audio(audio_data)
        self._headers = {'Transfer-Encoding': 'chunked'}
        if isinstance(headers, dict):
            self._headers.update(headers)
        self._params = kwargs

        self._send(proxy_key)
        self._reply_check()
        self._parse_response()

    def _get_audio(self, audio_data: AudioData):
        return audio_data.get_wav_data(self._convert_rate, self._convert_width)

    def _chunks(self):
        with BytesIO(self._audio) as fp:
            while True:
                chunk = fp.read(self.BUFF_SIZE)
                yield chunk
                if not chunk:
                    break

    def _send(self, proxy_key):
        try:
            self._rq = requests.post(
                self._url,
                data=self._chunks(),
                params=self._params,
                headers=self._headers,
                stream=True,
                timeout=60,
                proxies=proxies(proxy_key)
            )
        except REQUEST_ERRORS as e:
            raise RuntimeError(str(e))

    def _reply_check(self):
        if not self._rq.ok:
            print(self._rq.status_code, self._rq.reason, self._rq.text)
            raise RuntimeError('{}: {}'.format(self._rq.status_code, self._rq.reason))

    def _parse_response(self):
        pass

    def text(self):
        if not self._text:
            raise UnknownValueError('No variants')
        return self._text


class Yandex(BaseSTT):
    # https://tech.yandex.ru/speechkit/cloud/doc/guide/common/speechkit-common-asr-http-request-docpage/
    URL = 'https://asr.yandex.net/asr_xml'

    def __init__(self, audio_data: AudioData, key, lang='ru-RU'):
        if not key:
            raise RuntimeError('API-Key unset')
        rate = 16000
        width = 2
        headers = {'Content-Type': 'audio/x-pcm;bit={};rate={}'.format(width*8, rate)}
        kwargs = {
            'uuid': hashlib.sha1(str(time.time()).encode()).hexdigest()[:32],
            'key': key,
            'topic': 'queries',
            'lang': lang,
            'disableAntimat': 'true'
        }
        super().__init__(self.URL, audio_data, headers, rate, width, 'stt_yandex', **kwargs)

    def _get_audio(self, audio_data: AudioData):
        return audio_data.get_raw_data(self._convert_rate, self._convert_width)

    def _parse_response(self):
        self._text = xml_yandex(self._rq.text)


class YandexCloud(BaseSTT):
    # https://cloud.yandex.ru/docs/speechkit/stt/request
    URL = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'

    def __init__(self, audio_data: AudioData, key, lang='ru-RU'):
        if not isinstance(key, (tuple, list)) or len(key) < 2:
            raise RuntimeError('Wrong Yandex APIv2 key')
        rate = 16000
        width = 2
        headers = {'Authorization': 'Bearer {}'.format(key[1])}
        kwargs = {
            'topic': 'general',
            'lang': lang,
            'profanityFilter': 'false',
            'folderId': key[0]
        }
        super().__init__(self.URL, audio_data, headers, rate, width, 'stt_yandex', **kwargs)

    def _chunks(self):
        cmd = ['opusenc', '--quiet', '--discard-comments', '-', '-']
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as popen:
            popen.stdin.write(self._audio)
            del self._audio
            while True:
                chunk = popen.stdout.read(self.BUFF_SIZE)
                yield chunk
                if not chunk:
                    break

    def _send(self, proxy_key):
        self._text = requests_post(
            self._url,
            'result',
            data=self._chunks(),
            params=self._params,
            headers=self._headers,
            stream=True,
            timeout=60,
            proxies=proxies(proxy_key)
        )

    def _reply_check(self):
        pass


class PocketSphinxREST(BaseSTT):
    # https://github.com/Aculeasis/pocketsphinx-rest
    def __init__(self, audio_data: AudioData, url='http://127.0.0.1:8085'):
        url = '{}/stt'.format(url)
        super().__init__(url, audio_data, {'Content-Type': 'audio/wav'}, 16000, 2, 'stt_pocketsphinx-rest')

    def _parse_response(self):
        try:
            result = json.loads(''.join(self._rq.text.split('\n')))
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            raise RuntimeError('Json decode error: {}'.format(e))

        if 'code' not in result or 'text' not in result or result['code']:
            raise RuntimeError('Response error: {}: {}'.format(result.get('code', 'None'), result.get('text', 'None')))
        self._text = result['text']
