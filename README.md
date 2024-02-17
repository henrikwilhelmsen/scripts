# Scripts

Various utility scripts for my personal use

## bootstrap.ps1

PowerShell script to bootstrap a new system with Python and other development tools.

### Usage Examples

Run script with no parameters, skipping the optional installs:

```shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/scripts/main/bootstrap.ps1" -OutFile "./bootstrap.ps1"; &"./bootstrap.ps1"; & Remove-Item "./bootstrap.ps1"
```

Run script directly and install a specific version of Python (3.11) and install Git:

```shell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/scripts/main/bootstrap.ps1" -OutFile "./bootstrap.ps1"; &"./bootstrap.ps1" -Python -PythonVersion 311 -Git; & Remove-Item "./bootstrap.ps1"
```
