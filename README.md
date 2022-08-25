# Omen Bot

[![GitHub release](https://img.shields.io/github/release/phloot/omen-bot.svg?style=flat-square)](https://github.com/Phloot/omen-bot/releases/latest)
[![CodeQL](https://github.com/Phloot/omen-bot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Phloot/omen-bot/actions/workflows/codeql-analysis.yml)
[![ci](https://github.com/Phloot/omen-bot/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/Phloot/omen-bot/actions/workflows/docker-ci.yml)
[![Discord](https://discordapp.com/api/guilds/840265739884560384/widget.png)](https://discord.gg/Y3VkTCdV4b)

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

## Build Workflow

1. Whenever a new tag is pushed following the format `v*.*.*`, the [Docker CI workflow](https://github.com/Phloot/omen-bot/blob/main/.github/workflows/docker-ci.yml) is triggered
2. The Docker build is run on a self hosted GitHub runner
3. Assuming the build is successful, the image is pushed to [Dockerhub](https://hub.docker.com/repository/docker/phlootdocker/omen) using the same tag as GitHub

## License

MIT
