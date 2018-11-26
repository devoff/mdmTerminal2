class _ConfigPrettyModels:
    @classmethod
    def format(cls, count):
        ot = 'о'
        if count == 1:
            et = 'ь'
            ot = 'а'
        elif count in [2, 3, 4]:
            et = 'и'
        else:
            et = 'ей'
        pretty = ['ноль', 'одна', 'две', 'три', 'четыре', 'пять', 'шесть']
        count = pretty[count] if count < 7 else count
        return 'Загружен{} {} модел{}'.format(ot, count, et)


CONFIG = {
    # ConfigHandler
    'err_ya_key': 'Ошибка получения ключа для Yandex: {}',
    'err_cfg_check': 'Ошибка в конфиге, {} не может быть {}. Установлено: {}',
    'err_save': 'Ошибка сохранения {}: {}',
    'miss_file': 'Файл не найден: {}',
    'err_load': 'Ошибка загрузки {}: {}',
    'save_for': 'Конфигурация сохранена за {}',
    'save': 'Конфигурация сохранена!',
    'miss_models': 'Директория с моделями не найдена {}',
    'models_count_call': _ConfigPrettyModels,
    'miss_settings': 'Файл настроек не найден по пути {}. Для первого запуска это нормально',
    'load_for': 'Загружено {} опций за {}',
    'lng_load_for': 'Локализация {} загружена за {}',
    'cfg_up': 'Конфиг обновлен: {}',
    'cfg_no_change': 'Конфигурация не изменилась',
    'load': 'Конфигурация загр+ужена!',
    'err_lng': 'Ошибка инициализации языка \'{}\': {}',
    'miss_tts_cache': 'Директория c tts кэшем не найдена {}',
    'tts_cache_size': 'Размер tts кэша {}: {}',
    'tts_cache_act_list': ['Ок.', 'Удаляем...'],
    'delete_file': 'Удаляю {}',
    'deleted_files': 'Удалено {} файлов. Новый размер TTS кэша {}',
    'create_dir': 'Директория {} не найдена. Создаю...',
    'miss_file_fixme': 'Файл {} не найден. Это надо исправить!',
    'say_ip': 'Терминал еще не настроен, мой IP адрес: {}',
    # ConfigUpdater
    # Учитывая что он сам читает настройки толку тут не много, все равно будет DEFAULT_LANG
    'wrong_json': 'Кривой json \'{}\': {}',
    'wrong_key': 'Ключи настроек могут быть только строками, не {}. Игнорирую ключ \'{}\'',
    'wrong_val': 'Недопустимое значение \'{}:{}\'. Игнорирую',
    'ignore_section': 'Игнорируем неизвестную секцию от сервера \'{}:{}\'',
    'wrong_type_val': 'Не верный тип настройки \'{}:{}\' {}. Сохраняем старое значение: \'{}\'. {}',
}

LOADER = {
    'hello': 'Приветствую. Голосовой терминал Мажордомо настраивается, три - - - - - - два - - - - - -один - - - - - -',
    'bye': 'Голосовой терминал мажордомо завершает свою работу.',
}

LOGGER = {'err_permission': 'Логгирование в {} невозможно - отсутствуют права на запись. Исправьте это'}

MODULES = {
    'error': 'Ошибка',

    # lock
    'lock_name': 'Блокировка',
    'lock_dsc': 'Включение/выключение блокировки терминала',
    'lock_phrase_lock': 'блокировка',

    'lock_say_unlock': 'Блокировка снята',
    'lock_say_lock': 'Блокировка включена',
    # debug
    'debug_name': 'Отладка',
    'debug_dsc': 'Режим настройки и отладки',
    'debug_phrase_enter': 'режим разработчика',
    'debug_phrase_exit': 'выход',

    'debug_say_exit': 'Внимание! Выход из режима разработчика',
    'debug_say_enter': 'Внимание! Включён режим разработчика. Для возврата в обычный режим скажите \'выход\'',
    # manager
    'mm_name': 'Менеджер',
    'mm_desc': 'Управление модулями',
    'mm_act_all': 'активировать везде',
    'mm_act': 'активировать',
    'mm_uact': 'деактивировать',
    'mm_del': 'удалить',
    'mm_rec': 'восстановить',

    'mm_no_mod': 'Модуль {} не найден',
    'mm_sys_mod': 'Модуль {} системный, его нельзя настраивать',
    'mm_must_rec': 'Модуль {} удален. Вначале его нужно восстановить',
    'mm_already': 'Модуль {} уже в режиме {}',
    'mm_now': 'Теперь модуль {} доступен в режиме {}',
    'mm_already2': 'Модуль {} и так {}',
    'mm_mod': 'Модуль {} {}',
    'err_mm': 'Это невозможно, откуда тут {}',
    # this_say
    'say_name': 'Скажи',
    'say_desc': 'Произнесение фразы',
    # this_nothing
    'nothing_all': 'Ничего',
    # counter
    'count_name': 'считалка',
    'count_desc':  'Считалка до числа. Или от числа до числа. Считалка произносит не больше 20 чисел за раз',
    'count_phrase_list': ['сосчитай', 'считай', 'посчитай'],

    'count_to': 'до',
    'count_from': 'от',
    'count_to_long': 'Это слишком много для меня - считать {} чисел.',
    'count_complete': 'Я всё сосчитала',
    # who_am_i
    'who_name': 'Кто я',
    'who_desc': 'Получение информации о настройках голосового генератора (только для Яндекса и RHVoice)',
    'who_ph_1': 'кто ты',
    'who_ph_2': 'какая ты',

    'who_now_no_support': 'Не поддерживается для {}',
    'who_my_emo': ' Я очень {}.',
    'who_my_name': 'Меня зовут {}.{}',
    # now_i
    'now_name': 'Теперь я',
    'now_desc': 'Изменение характера или голоса голосового генератора (только для Яндекса и RHVoice)',
    'now_phrases_list': ['теперь ты', 'стань'],
    # __now_i_set_speaker
    'now_already': 'Я уже {}.',
    'now_i_now': 'Теперь меня зовут {}, а еще я {}.',
    'now_no_character': 'без характера',
    # __now_i_set_emo
    'now_i_very': 'Теперь я очень {} {}.',
    # wiki
    'wiki_name': 'Вики',
    'wiki_desc': 'Поиск в Википедии',
    'wiki_phrases_list': ['расскажи', 'что ты знаешь', 'кто такой', 'что такое', 'зачем нужен', 'для чего'],

    'wiki_rm_pretext_list': ['о ', 'про ', 'в '],
    'wiki_find_of': 'Ищу в вики о \'{}\'',
    'wiki_ask': 'Уточните свой вопрос: {}',
    'wiki_not_know': 'Я ничего не знаю о {}.',
    # help_
    'help_name': 'Помощь',
    'help_desc': 'Справку по модулям (вот эту)',
    'help_phrases_list': ['помощь', 'справка', 'help', 'хелп'],

    'help_any_phrase': 'любую фразу',
    'help_mod_deleted': '. Модуль удален',
    'help_mod_full': 'Модуль {} доступен в режиме {}. Для активации скажите {}. Модуль предоставляет {} {}',
    'help_mod_header': 'Всего доступно {} модулей. Вот они:',
    'help_mod_line': 'Скажите {}. Это активирует {}. Модуль предоставляет {}',
    'help_mod_del_header': 'Всего {} модулей удалены, это: {}',
    'help_bye': 'Работа модуля помощь завершена.',
    # terminate_
    'term_name': 'Выход',
    'term_desc': 'Завершение работы голосового терминала',
    'term_phs_list_3': ['Завершение работы', 'умри', 'сдохни'],
    'term_bye': 'Come Along With Me.',
    # reboot_
    'rbt_name': 'Перезагрузка',
    'rbt_dsc': 'Перезапуск голосового терминала',
    'rbt_ph_4': ['Перезагрузка', 'Ребут', 'Рестарт', 'reboot'],
    'rbt_bye': 'Терминал перезагрузится через 5... 4... 3... 2... 1...',
    # majordomo
    'mjd_name': 'Мажордом',
    'mjd_desc': 'Отправку команд на сервер Мажордомо',

    'mjd_no_say': 'Вы ничего не сказали?',
    'mjd_no_ip_log': 'IP сервера majordomo не задан.',
    'mjd_no_ip_say': 'IP сервера MajorDoMo не задан, исправьте это! Мой IP адрес: {}',
    # 'Скажи ' -> 'скажи '
    'mjd_rep_say': 'Скажи ',
    'mjd_rep_say_len': 6,
    'mjd_rep_say_s': 'с',

    'err_mjd': 'Ошибка коммуникации с сервером majordomo: {}',
    'mjd_ok': 'Запрос был успешен: {}',
    # terminator
    'terminator_name': 'Терминатор',
    'terminator_desc': 'Информацию что соответствие фразе не найдено',
    'terminator_say': 'Соответствие фразе не найдено: {}',
}

MODULES_MANAGER = {
    'say_nm': 'Обычный',
    'say_dm': 'Отладка',
    'say_any': 'Любой',
    'say_enable': 'восстановлен',
    'say_disable': 'удален',
    'modules_load': 'Загружены модули: {}',
    'conflict_found': 'Обнаружены конфликты в режиме {}: {}',
    'not_say': 'Вы ничего не сказали?',
    'catch': 'Захвачено {}',
}

MPD_CONTROL = {'err_mpd': 'Ошибка подключения к MPD-серверу'}

PLAYER = {
    'file_not_found': 'Файл {} не найден',
    'unknown_type': 'Неизвестный тип файла: {}',
    'play': 'Играю {} ...',
    'stream': 'Стримлю {} ...',
}

SERVER = {
    'err_start_say': 'Ошибка запуска сервера{}.',
    'err_already_use': ' - адрес уже используется',
    'err_start': 'Ошибка запуска сервера на {}:{}: {}',
    'no_data': 'Нет данных',
    'get_data': 'Получены данные: {}',
    'unknown_cmd': 'Неизвестная команда: {}',
    'no_implement': 'Not implemented yet - {}:{}',
    'err_rec_param': 'Ошибка разбора параметров для \'rec\': {}',
    'unknown_rec_cmd': 'Неизвестная команда для rec: {}',
}

STTS = {
    # _TTSWrapper
    'action_cache': '{}найдено в кэше',
    'action_gen': '{}сгенерированно {}',
    'for_time': '{} за {}{}: {}',
    # lang для tts провайдеров
    'tts_lng_def': 'ru-RU',
    'tts_lng_dict': {'google': 'ru', 'yandex': 'ru-RU'},

    'unknown_prov': 'Неизвестный провайдер: {}',
    'err_synthesis': 'Ошибка синтеза речи от {}, ключ \'{}\'. ({})',
    # SpeechToText
    'no_mics': 'Микрофоны не найдены',
    'mics_to': 'Доступны {}, от 0 до {}.',
    'wrong_mic_index': 'Не верный индекс микрофона {}. {}',
    'record_for': 'Голос записан за {}',
    'recognized': 'Распознано: {}{}',
    'recognized_from': 'Для распознавания используем {}',
    'err_voice_record': 'Во время записи произошел сбой, это нужно исправить',
    # language для google и bing
    'stt_lng': 'ru-RU',

    'err_unknown_prov': 'Ошибка распознавания - неизвестный провайдер {}',
    'err_stt_say': 'Произошла ошибка распознавания',
    'err_stt_log': 'Произошла ошибка {}',
    'recognized_for': 'Распознано за {}',
    'consensus': 'Распознано: {}. Консенсус: {}',
    # Phrases
    'p_hello': ['Привет', 'Слушаю', 'На связи', 'Привет-Привет'],
    'p_deaf': ['Я ничего не услышала', 'Вы ничего не сказали', 'Ничего не слышно', 'Не поняла'],
    'p_ask': ['Ничего не слышно, повторите ваш запрос'],
}

TERMINAL = {
    'err_queue_empty': 'Пустая очередь? Impossible!',
    'get_call': 'Получено {}:{}, lvl={} опоздание {} секунд.',
    'ignore_call': '{} Игнорирую.',
    'err_call': 'Не верный вызов, WTF? {}:{}, lvl={}',
    # _rec_rec
    'rec_nums': {'1': 'первого', '2': 'второго', '3': 'третьего'},
    'err_rec_param': 'Ошибка записи - недопустимый параметр',
    'rec_hello': 'Запись {} образца на 5 секунд начнется после звукового сигнала',
    'rec_bye': 'Запись {} образца завершена. Вы можете прослушать свою запись.',
    'err_rec_save': 'Ошибка сохранения образца {}: {}',
    # _rec_play
    'err_play_say': 'Ошибка воспроизведения - файл {} не найден',
    'err_play_log': 'Файл {} не найден',
    # _rec_compile
    'compile_no_file': 'Ошибка компиляции - файл {} не найден.',
    'compiling': 'Компилирую {}',
    'err_compile_log': 'Ошибка компиляции модели {}: {}',
    'err_compile_say': 'Ошибка компиляции модели номер {}',
    'no_consensus': 'Полный консенсус по модели {} не достигнут [{}/{}]. Советую пересоздать модель.',
    'err_no_consensus': 'Полный консенсус по модели {} не достигнут. Компиляция отменена.',
    'compile_ok_log': 'Модель{} скомпилирована успешно за {}: {}',
    'compile_ok_say': 'Модель{} номер {} скомпилирована успешно за {}',
    # _detected
    'err_call2': 'Очень странный вызов от сноубоя. Это нужно исправить',
    'wrong_activation': 'Ошибка активации: \'{}\'',
    'activate_by': 'Голосовая активация по {}{}',
    'model_listened': '{} слушает',
}

YANDEX_EMOTION = {
    'good'    : 'добрая',
    'neutral' : 'нейтральная',
    'evil'    : 'злая',
}

YANDEX_SPEAKER = {
    'jane'  : 'Джейн',
    'oksana': 'Оксана',
    'alyss' : 'Алиса',
    'omazh' : 'Омар',  # я это не выговорю
    'zahar' : 'Захар',
    'ermil' : 'Саня'  # и это
}

RHVOICE_SPEAKER = {
    'anna'     : 'Аня',
    'aleksandr': 'Александр',
    'elena'    : 'Елена',
    'irina'    : 'Ирина'
}
