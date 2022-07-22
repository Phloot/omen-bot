# Omen Bot
## A Guild Wars 2 themed Discord bot for the Celestial Omen guild on Crystal Desert

## Features

- Simple Guild Wars 2 API wrapper support
- Welcoming of new joinees

Markdown is a lightweight markup language based on the formatting conventions
that people naturally use in email.

## Set up

The bot is designed to run inside of a Docker container, with the scripts dependencies installed during container build. Build is tested and confirmed working under Docker version 20.10.17 build 100c701

Clone repository

```sh
git clone git@github.com:Phloot/omen-bot.git
```

Build Docker image

```sh
docker build omen-bot -t .
```

Spawn Docker container

```sh
docker run omen-bot --discord_token TOKEN_HERE
```

## License

MIT
