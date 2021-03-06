# mdmTerminal 2
[![Build status](https://ci.appveyor.com/api/projects/status/v98bcj9mr2s1g13a/branch/master?svg=true)](https://ci.appveyor.com/project/Aculeasis/mdmterminal2)

Голосовой терминал для [MajorDoMo](https://github.com/sergejey/majordomo), форк [mdmPiTerminal](https://github.com/devoff/mdmPiTerminal).

Полностью совместим с [MDM VoiceAssistant](https://github.com/lanket/mdmPiTerminalModule).

**Возможности**
- Запуск распознавания по любым ключевым словам
- Передача команды в MajorDoMo
- Взаимодействие через [MajorDroid API](http://majordomo.smartliving.ru/forum/viewtopic.php?f=5&t=518) (sayReply, ask etc.)
- Воспроизведение музыки через MajorDroid API
- [Работа через прокси](https://github.com/Aculeasis/mdmTerminal2/wiki/proxy)
- [Дополнительные возможности](#Дополнительные-возможности)

# Установка
**Используя докер**: [Dockerfile и готовые образы под x86_64, aarch64, armv7l](https://github.com/Aculeasis/mdmt2-docker)

## Обычная установка
### Подготовка
- Проверка работы записи\воспроизведения

  Запустите `arecord -d 5 __.wav && aplay __.wav && rm __.wav` и говорите что-нибудь 5 секунд.

Вы должны услышать хреновую запись своего голоса. Если что-то пошло не так аудиосистема требует настройки.

Скопируйте один из файлов из `mdmTerminal2/asound` в `/etc/asound.conf`. Для OPi zero +2 H5 должен подойти `asound_h3.conf
`
#### Armbian на OrangePi
- Аналоговые кодеки:

  Запустите `armbian-config` -> System -> Hardware. Включите *analog-codec* и перезагрузите апельсинку.
- Встроенный микрофон (проверял на Zero +2 H5 с платой):

  `alsamixer` -> F4 выбираем Mic1 и жмем space, выходим

Узнайте на каком устройстве находятся микрофон и динамик через команды:
```bash
    aplay -l
    arecord -l
```
и отредактировать если нужно `"hw:X,0"` в `/etc/asound.conf`

Если запись или воспроизведение все еще не работают, можно поискать решение [на форуме](https://majordomo.smartliving.ru/forum/viewtopic.php?f=5&t=5460)

### Установка
Клонируйте репозиторий и запустите скрипт установки:
```bash
    cd ~/
    git clone https://github.com/Aculeasis/mdmTerminal2
    cd mdmTerminal2
    ./scripts/install.sh
```

Теперь можно запустить терминал в консоли и проверить его работоспособность:
```bash
    env/bin/python -u src/main.py
```
Если все работает можно добавить сервис в systemd - терминал будет запускаться автоматически:
```bash
    ./scripts/systemd_install.sh
```
И посмотреть статус сервиса:
```bash
    sudo systemctl status mdmterminal2.service
```
# Настройка
### [Описание всех настроек](https://github.com/Aculeasis/mdmTerminal2/wiki/settings.ini)
**Важно!** Значительная часть настроек не доступна через MDM VoiceAssistant, их можно изменить отредактировав `mdmTerminal2/src/settings.ini`.

[Настройка системных фраз](https://github.com/Aculeasis/mdmTerminal2/wiki/phrases.json)

## Подключение к MajorDoMo
**Создание терминала**:
- После заходим - в Настройки > Терминалы > Добавить новую запись > Добавляем название и IP адрес терминала.
- Включаем *MajorDroid API*.
- Тип плеера: *MajorDroid*.
- Порт доступа к плееру: *7999*.
- Сохраняем.

Также можно выбрать плеер *MPD* и порт *6600*, тогда MajorDoMo будет управлять mpd напрямую.

**MDM VoiceAssistant**:
- Заходим в Панель управления MajorDomo > Система > Маркет дополнений > Оборудование > MDM VoiceAssistant и устанавливаем модуль.
- Переходим в Устройства > MDM VoiceAssistant.
- Выбираем ранее созданный терминал.
- Выбираем Сервис синтеза речи

  Если есть API ключ от Яндекса, лучше выбрать Yandex TTS, ~~если нет то Google~~ Yandex может работать с пустым ключом (пока).
- Чувствительность реагирования на ключевое слово

  Чем больше тем лучше слышит, но будет много ложных срабатываний.
- Сервис распознавания речи

  Можно выбрать wit.ai или Microsoft, но для них нужно получить API. Google работает без ключа.
- Сохраняем.
## Запись ключевых слов
- Переходим в Устройства >  MDM VoiceAssistant > Выбираем наш терминал > Запись ключевого слова.
- В самом верху выбираем какую модель-активатор мы хотим создать. Если модель уже существует, она будет перезаписана. Можно создать до 6 фраз-активаторов.
- Нажимаем **Запись**, последовательно записываем 3 образца голоса.
- (Опционально) Прослушиваем записи.
- Нажимаем **Компиляция**. Терминал отправит образцы на сервер snowboy и получит готовую модель.

  Если все прошло хорошо, терминал выполнит реинициализацию моделей и начнет активироваться по новой фразе.

Модели хранятся в `mdmTerminal2/src/resources/models/` и имеют расширение `.pmdl`. Они идентичны моделям в **mdmPiTerminal**. Если вы хотите убрать фразу из активации вам нужно удалить соответствующую модель.

# Сборка snowboy (_snowboydetect.so)
`src/lib/_snowboydetect.so` собирается при установке, но если что-то пошло не так проще всего пересобрать его скриптом:
```bash
    ./scripts/snowboy_build.sh
```
**Важно!** Скрипт можно запускать после `./scripts/install.sh`, т.к. он устанавливает все необходимые зависимости.

### Сборка на старых системах
Для сборки нужен swig 3.10 и выше, если у вас старый swig и вы получаете ошибку `ImportError: No module named '_snowboydetect'` т.к. модуль не собирается нужно обновить swig:
```bash
sudo apt update
sudo apt-get install -y build-essential libpcre3-dev autoconf automake libtool bison git libboost-dev python-dev ruby ruby-dev tcl-dev mono-devel lua5.1 liblua5.1-0-dev octave liboctave-dev php5-cli php5-dev openjdk-7-jdk guile-2.0-dev

git clone https://github.com/swig/swig.git
cd swig
./autogen.sh
./configure
make
sudo make install
cd ..
rm -rf swig/
```
И снова запустить скрипт сборки модуля.

# Дополнительные возможности
Терминал поддерживает модули, большинство их них активны только в режиме разработчика (можно переключить в нормальный). Модули перехватывают фразы по ключевым словам и что-то делают (или нет)

**Блокировка**: Включается\отключается фразой _блокировка_. Заблокированный терминал не реагирует на иные фразы, удобно для предотвращения случайных срабатываний.
### Режим разработчика
Включается фразой _режим разработчика_, выключается _выход_. В этом режиме терминал работает автономно.

Доступно изменение некоторых настроек, считалка, поиск в Википедии и т.д.

Вызов справки по модулям: _помощь_, _справка_, _help_ или _хелп_. Можно вызвать справку по конкретному модулю _справка <имя модуля>_

Настраивать модули можно через модуль `Менеджер`

# Решение проблем
- Если не работает USB микрофон, попробуйте выдернуть и вставить обратно, иногда это помогает.
- Заикание rhvoice* в конце фраз лечится использованием одного из конфигов для `asound.conf`. Или отключением кэша (wav не заикается)
- Если голос терминала искажается при активации, нужно настраивать `asound.conf` или попробовать другие конфиги.
- Если терминал плохо распознает голос т.к. записывает сам себя, `blocking_listener = 1` может помочь.

# Ссылки
- [mdmPiTerminal](https://github.com/devoff/mdmPiTerminal)
- [В докере](https://github.com/Aculeasis/mdmt2-docker)
- [MDM VoiceAssistant](https://github.com/lanket/mdmPiTerminalModule)
- [MajorDoMo](https://github.com/sergejey/majordomo)
- [Snowboy](https://github.com/Kitt-AI/snowboy)
- [rhvoice-rest](https://github.com/Aculeasis/rhvoice-rest)
- [pocketsphinx-rest](https://github.com/Aculeasis/pocketsphinx-rest)
