
<span style="color: magenta; font-size: 20px;">·.•°•.·.✧ ✦ 🧚 ✦</span> 
# Navi-Assistant

Navi is a command-line personal assistant, powered by OpenAI,  designed to leverage terminal commands. For example, Navi can be configured to have the ability to execute `uname -a` to understand the current operating system.  

A number of commands have been added by default, including:  
- `date`
- `cat`
- `diff`
- `df`
- `ip address`
- `journalctl`
- `ls`
- `lsblk`
- `lscpu`
- `lsusb`
- `ps aux`
- `rg` (ripgrep)
- `sensors`
- `systemctl status`
- `tree`
- `uptime`
- `users`
- `uname`
- `w3m`

> NOTE: The current default list of commands is based upon a Linux system; in the future there should be defaults for Windows.  

The commands available to Navi is fully customisable. Commands are defined in a JSON file (`~/.local/config/navi/commands.json`).  
Commands are added to assistants as tools during their creation. This makes it possible to extend your assistants capabilities.

## Installation
> TODO: There should be a bash script to curl and execute which installs Navi

## Usage

