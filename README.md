# Scripts

Various utility scripts for my personal use

## bootstrap.sh

```shell
curl -sL https://raw.githubusercontent.com/henrikwilhelmsen/scripts/main/bootstrap.sh | bash
```

## bootstrap.ps1

PowerShell script to bootstrap a new system with Git, uv and other development tools.

### Usage Examples

Run script with no parameters, skipping the optional installs:

```shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/scripts/main/bootstrap.ps1" -OutFile "./bootstrap_tmp.ps1"; &"./bootstrap_tmp.ps1"; & Remove-Item "./bootstrap_tmp.ps1"
```

Run script directly and install Git and uv:

```shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/scripts/main/bootstrap.ps1" -OutFile "./bootstrap_tmp.ps1"; &"./bootstrap_tmp.ps1" -Python -Git; & Remove-Item "./bootstrap_tmp.ps1"
```

## configure_win_shell.py

Configure Windows Terminal and PowerShell with my preferences.

Download and run the script with uv:

```shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/scripts/main/configure_win_shell.py" -OutFile "./configure_win_shell_tmp.py"; &uv run "./configure_win_shell_tmp.py"; & Remove-Item "./configure_win_shell_tmp.py"
```
