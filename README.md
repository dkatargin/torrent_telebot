# Torrent-Telebot

## Telegramm-бот для управления торрент-сервером на базе transmission

На данный момент умеет:

- запрашивать список торрентов;
- добавлять торренты;
- загружать торренты в определенные каталоги;
- работать через socks-прокси

## Пример интеграции с systemd

```systemd
[Unit]
Description=TorrentTelegramBot
After=network.target

[Service]
Type=simple
User=user
Group=usergroup
WorkingDirectory=/torrent_telebot
ExecStart=/usr/bin/python3 /torrent_telebot/app.py
StandardOutput=syslog
StandardError=syslog
RestartSec=20
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Включение proxy

```
[Proxy]
host = <proxyadddr>
port = 1080
username = <proxy user>
password = <proxy password>
```
