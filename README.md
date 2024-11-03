# Scripts

Various utility scripts for my personal use

## bootstrap.ps1

PowerShell script to bootstrap a new system with Git, uv and other development tools.

### Usage Examples

Run script with no parameters, skipping the optional installs:

```shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/scripts/main/bootstrap.ps1" -OutFile "./bootstrap.ps1"; &"./bootstrap.ps1"; & Remove-Item "./bootstrap.ps1"
```

Run script directly and install Git and uv:

```shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/scripts/main/bootstrap.ps1" -OutFile "./bootstrap.ps1"; &"./bootstrap.ps1" -Python -Git; & Remove-Item "./bootstrap.ps1"
```
