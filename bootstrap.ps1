<#
.SYNOPSIS
    Utility script to bootstrap a Windows pc with developer tools with Winget and Scoop.
    Updates tools if they are already installed.
.PARAMETER Git
    Installs Git and Fork if specified.
.PARAMETER Python
    Installs uv if specified.

.NOTES
    - This script requires Winget package manager.
#>

param (
    [switch]$Git,
    [switch]$Python
)
function CommandInstalled {
    [CmdletBinding()]
    param (
        [string]$CommandName
    )

    $command = Get-Command $CommandName -ErrorAction SilentlyContinue
    if ($command) {
        return $true
    }
    else {
        return $false
    }
}

function Install-PowerShell {
    if ((CommandInstalled pwsh)) {
        Write-Host "PowerShell already installed, updating."
        winget update Microsoft.PowerShell --silent
        return
    }

    Write-Host "Installing PowerShell..."

    try {
        winget install Microsoft.PowerShell --silent
        Write-Host "Powershell installed!"
    }
    catch {
        Write-Warning "Failed to install PowerShell. Please install it manually."
        return
    }
}
function Install-WindowsTerminal {
    if ((CommandInstalled wt)) {
        Write-Host "Windows Terminal already installed, updating."
        winget update Microsoft.WindowsTerminal --silent
        return
    }

    Write-Host "Installing Windows Terminal..."

    try {
        winget install Microsoft.WindowsTerminal --silent
        Write-Host "Windows Terminal installed!"
    }
    catch {
        Write-Warning "Failed to install Windows Terminal. Please install it manually."
        return
    }
}
function Install-TerminalIcons {
    Write-Host "Installing Terminal Icons..."

    try {
        Install-Module -Name Terminal-Icons -Repository PSGallery -Force
        Write-Host "Terminal Icons installed!"
    }
    catch {
        Write-Warning "Failed to install Terminal Icons. Please install it manually."
        return
    }
}
function Install-Uv {
    if ((CommandInstalled uv)) {
        Write-Host "uv already installed, updating."
        winget update astral-sh.uv --silent
        return
    }

    Write-Host "Installing Windows Terminal..."

    try {
        winget install --id=astral-sh.uv  -e --silent
        Write-Host "uv installed!"
    }
    catch {
        Write-Warning "Failed to install uv. Please install it manually."
        return
    }
}

function Update-Scoop {
    if (!(CommandInstalled git)) {
        Write-Host "Git not installed, skipping scoop update."
        return
    }
    try {
        Write-Host "Updating Scoop..."
        scoop update
    }
    catch {
        Write-Warning "Failed to update scoop."
        return
    }
    Write-Host "Scoop updated!"
}
function Install-Scoop {
    if ((CommandInstalled scoop)) {
        Write-Host "Scoop already installed, updating..."
        Update-Scoop
        return
    }
    try {
        Write-Host "Installing Scoop..."
        Invoke-RestMethod get.scoop.sh | Invoke-Expression
    }
    catch {
        Write-Warning "Failed to install Scoop. Please install it manually from https://scoop.sh/."
        return
    }
    Write-Host "Scoop installed!"
}

function Install-ScoopBucket {
    param (
        [string]$bucketName
    )
    # check if Scoop is available, return if not.
    if (!(CommandInstalled scoop)) {
        Write-Warning "scoop not available, skipping $bucketName bucket setup."
        return
    }

    # add the bucket to Scoop if it doesn't exist
    if (!(scoop bucket list | Select-String -Quiet $bucketName)) {
        try {
            scoop bucket add $bucketName
        }
        catch {
            Write-Warning "Failed to add $bucketName bucket to Scoop."
            return
        }
        Write-Host "$bucketName bucket added!"
        return
    }
    # if the bucket already exists, return
    Write-Host "$bucketName bucket already added, skipping."
}
function Install-ScoopPackage {
    <#
    .SYNOPSIS
        Installs a package with Scoop.
    .PARAMETER packageName
        The name of the package to install.
    .PARAMETER installArg
        The argument to pass to Scoop when installing the package. Default is the package name.

        For use when the package name differs from the install argument.
    #>
    param (
        [string]$packageName,
        [string]$installArg = $packageName
    )
    # check if Scoop is available, return if not.
    if (!(CommandInstalled scoop)) {
        Write-Warning "scoop not available, skipping $packageName installation."
        return
    }

    # update the package if it's already installed, then return
    if ((scoop list | Select-String -Quiet $packageName)) {
        Write-Host "$packageName already installed, updating."
        scoop update $packageName
        return
    }

    # install the package
    try {
        scoop install $packageName
    }
    catch {
        Write-Warning "Failed to install $packageName with scoop."
        return
    }
    Write-Host "$packageName installed!"
}


function BootStrap {
    Install-PowerShell
    Install-WindowsTerminal
    Install-TerminalIcons
    Install-Scoop
    Install-ScoopBucket "nerd-fonts"
    Install-ScoopBucket "extras"
    Install-ScoopPackage "Mononoki-NF"
    Install-ScoopPackage "FiraCode-NF"
    Install-ScoopPackage "CascadiaCode-NF"
    Install-ScoopPackage "MesloLGM-NF"
    Install-ScoopPackage "JetBrainsMono-NF"
    Install-ScoopPackage "oh-my-posh" "https://github.com/JanDeDobbeleer/oh-my-posh/releases/latest/download/oh-my-posh.json"

    if ($Git) {
        Install-ScoopPackage "git"
        Install-ScoopPackage "Fork"
    }

    if ($Python) {
        Install-Uv
    }
}

BootStrap
