# raspi-clus-backend
___
## Table of contents 
 * [General Info](#general-info)
 * [Installation](#installation)
 * [Running](#running)
 * [Raspberry Pi setup](#raspberry-pi-setup)
 * [Image Preparation](#image-preparation)
## General info
>Please note that this project is only backend part of the RaspiClus application, for frontend part go to [RaspiClus](https://github.com/DonHesus/raspi-clus-client)

> This project is part of the master thesis.

Welcome to RaspiClus project.

Main goal of this project is to allow for an easy way to create, maintain and monitor Raspberry Pi clusters with diskless booting. 
With that being said, imagine a situation when you're maintaining a fog layer containing X number of Fog nodes containing Y number of Raspberry Pi systems.

Supported(or in Roadmap) use cases and features:
1. Remote system refresh in case something happens to the original OS.
2. Remote system swap, for example, standard Raspberry Pi OS, might not support some of required packages, in this case just simple switch to Ubuntu or another one that's needed.
3. Let's say that you want to merge to clusters into one but without physical interaction.
4. Each system gathers information about itself and sends it to the server allowing for monitoring.

___

## Installation
`make install`
___

## Running
``make run``
___

## Raspberry Pi setup
>More complex instructions TBD

In order to prepare your Raspberry Pi, you need to first boot it using Raspberry Pi OS.

Next step is to run raspi-config tool and change boot mode in advanced settings to net boot.

After reboot make sure that result of `vcgencmd bootloader_config` returns sections with `BOOT_ORDER=0xf21` value. 
If value is correct, you can shut down Raspberry Pi and disconnect SD card.

Turn on ip tables
cgroup enebaled
___

## Image Preparation
>More complex instructions TBD

Easiest and least demanding method is to choose a pre_installed OS, boot it, configure it for your use.

After that, turn off raspberry Pi and connect SD card to your server, you should be able to identify two partitions.

One is designed for booting the system and the second one is actual system. Both of them need to be copied into prepared
by server directory, accordingly.
___
