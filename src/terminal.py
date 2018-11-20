#!/usr/bin/env python3

import os
import queue
import threading
import time

import lib.snowboy_training as training_service
import logger
import player
import stts
import utils
from languages import TERMINAL as LNG
from lib import snowboydecoder


class MDTerminal(threading.Thread):
    MAX_LATE = 60

    def __init__(self, cfg, play_: player.Player, stt: stts.SpeechToText, log, handler):
        super().__init__(name='MDTerminal')
        self.log = log
        self._cfg = cfg
        self._play = play_
        self._stt = stt
        self._handler = handler
        self.work = False
        self._paused = False
        self._is_paused = False
        self._snowboy = None
        self._callbacks = []
        self.reload()
        self._queue = queue.Queue()

    def reload(self):
        self.paused(True)
        try:
            self._reload()
        finally:
            self.paused(False)

    def _reload(self):
        if len(self._cfg.path['models_list']) and self._stt.max_mic_index != -2:
            self._snowboy = snowboydecoder.HotwordDetector(
                decoder_model=self._cfg.path['models_list'], sensitivity=[self._cfg.gts('sensitivity')]
            )
            self._callbacks = [self._detected for _ in self._cfg.path['models_list']]
        else:
            self._snowboy = None

    def join(self, timeout=None):
        self.work = False
        self.log('stopping...', logger.DEBUG)
        super().join()
        self.log('stop.', logger.INFO)

    def start(self):
        self.work = True
        super().start()
        self.log('start', logger.INFO)

    def paused(self, paused: bool):
        if self._paused == paused or self._snowboy is None:
            return
        self._paused = paused
        while self._is_paused != paused and self.work:
            time.sleep(0.1)

    def _interrupt_callback(self):
        return not self.work or self._paused or self._queue.qsize()

    def run(self):
        while self.work:
            self._is_paused = self._paused
            if self._paused:
                time.sleep(0.1)
                continue
            self._listen()
            self._external_check()

    def _listen(self):
        if self._snowboy is None:
            time.sleep(0.5)
        else:
            self._snowboy.start(detected_callback=self._callbacks,
                                interrupt_check=self._interrupt_callback,
                                sleep_time=0.03)
            self._snowboy.terminate()

    def _external_check(self):
        while self._queue.qsize() and self.work:
            try:
                (cmd, data, lvl, late) = self._queue.get_nowait()
            except queue.Empty:
                self.log(LNG['err_queue_empty'], logger.ERROR)
                continue
            late = time.time() - late
            msg = LNG['get_call'].format(cmd, data, lvl, int(late))
            if late > self.MAX_LATE:
                self.log(LNG['ignore_call'].format(msg), logger.WARN)
                continue
            else:
                self.log(msg, logger.DEBUG)
            if cmd == 'ask' and data:
                self.detected(data)
            elif cmd == 'voice' and not data:
                self.detected(voice=True)
            elif cmd == 'rec':
                self._rec_rec(*data)
            elif cmd == 'play':
                self._rec_play(*data)
            elif cmd == 'compile':
                self._rec_compile(*data)
            else:
                self.log(LNG['err_call'].format(cmd, data, lvl), logger.ERROR)

    def _rec_rec(self, model, sample):
        # Записываем образец sample для модели model
        if sample not in LNG['rec_nums']:
            self.log('{}: {}'.format(LNG['err_rec_param'], sample), logger.ERROR)
            self._play.say(LNG['err_rec_param'])
            return

        hello = LNG['rec_hello'].format(LNG['rec_nums'][sample])
        save_to = os.path.join(self._cfg.path['tmp'], model + sample + '.wav')
        self.log(hello, logger.INFO)

        err = self._stt.voice_record(hello=hello, save_to=save_to, convert_rate=16000, convert_width=2)
        if err is None:
            bye = LNG['rec_bye'].format(LNG['rec_nums'][sample])
            self._play.say(bye)
            self.log(bye, logger.INFO)
        else:
            err = LNG['err_rec_save'].format(LNG['rec_nums'][sample], err)
            self.log(err, logger.ERROR)
            self._play.say(err)

    def _rec_play(self, model, sample):
        file_name = ''.join([model, sample, '.wav'])
        file = os.path.join(self._cfg.path['tmp'], file_name)
        if os.path.isfile(file):
            self._play.say(file, is_file=True)
        else:
            self._play.say(LNG['err_play_say'].format(file_name))
            self.log(LNG['err_play_log'].format(file), logger.WARN)

    def _rec_compile(self, model, _):
        models = [os.path.join(self._cfg.path['tmp'], ''.join([model, x, '.wav'])) for x in ['1', '2', '3']]
        miss = False
        for x in models:
            if not os.path.isfile(x):
                miss = True
                self.log(LNG['compile_no_file'].format(x), logger.ERROR)
                self._play.say(LNG['compile_no_file'].format(os.path.basename(x)))
        if miss:
            return
        pmdl_name = ''.join(['model', model, self._cfg.path['model_ext']])
        pmdl_path = os.path.join(self._cfg.path['models'], pmdl_name)
        self.log(LNG['compiling'].format(pmdl_path), logger.INFO)
        work_time = time.time()
        try:
            snowboy = training_service.Training(*models)
        except RuntimeError as e:
            self.log(LNG['err_compile_log'].format(pmdl_path, e), logger.ERROR)
            self._play.say(LNG['err_compile_say'].format(model))
            return
        work_time = utils.pretty_time(time.time() - work_time)
        snowboy.save(pmdl_path)
        phrase, match_count = self._stt.phrase_from_files(models)
        msg = ', "{}",'.format(phrase) if phrase else ''
        if match_count != len(models):
            self.log(LNG['no_consensus'].format(pmdl_name, match_count, len(models)), logger.WARN)
        self.log(LNG['compile_ok_log'].format(msg, work_time, pmdl_path), logger.INFO)
        self._play.say(LNG['compile_ok_say'].format(msg, model, work_time))
        self._cfg.models_load()
        if self._cfg.json_to_cfg({'models': {pmdl_name: phrase}}):
            self._cfg.config_save()
        self._reload()
        # Удаляем временные файлы
        for x in models:
            os.remove(x)

    def external_cmd(self, cmd: str, data='', lvl: int = 0):
        if cmd == 'tts':
            if not lvl:
                self._play.say(data, lvl=0)
                return
        self._queue.put_nowait((cmd, data, lvl, time.time()))

    def _detected(self, model: int=0):
        phrase = ''
        if not model:
            self.log(LNG['err_call2'], logger.CRIT)
        else:
            model -= 1
            if model < len(self._cfg.path['models_list']):
                model_name = os.path.split(self._cfg.path['models_list'][model])[1]
                phrase = self._cfg['models'].get(model_name)
                msg = '' if not phrase else ': "{}"'.format(phrase)
            else:
                model_name = str(model)
                msg = ''
            self.log(LNG['activate_by'].format(model_name, msg), logger.INFO)
        no_hello = self._cfg.gts('no_hello', 0)
        hello = ''
        if phrase and self._stt.sys_say.chance and not no_hello:
            hello = LNG['model_listened'].format(phrase)
        self.detected(hello=hello, voice=no_hello)

    def detected(self, hello: str = '', voice=False):
        if self._snowboy is not None:
            self._snowboy.terminate()

        caller = False
        reply = self._stt.listen(hello, voice=voice)
        if reply or voice:
            while caller is not None:
                reply, caller = self._handler(reply, caller)
                if caller:
                    reply = self._stt.listen(reply or '', voice=not reply)
        if reply:
            self._play.say(reply, lvl=1)
        self._listen()
