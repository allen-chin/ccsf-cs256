Param (
    [string]$LocalPath = (Get-Item -Path ".\").FullName + '\images\',
    [string]$Config = (Join-Path $PSScriptRoot "config.xml"),
    [switch]$EnterCredentials
)

if ($LocalPath.Substring($LocalPath.Length - 1) -ne '\') {
    $LocalPath += '\'
}

$null = New-Item -Path $LocalPath -ItemType "directory" -Force

if ($EnterCredentials) {
    $credential = Get-Credential
}
elseif (Test-Path -Path $Config) {
    # Use saved credentials file
    $credential = Import-CliXml -Path $Config
}
else {
    # Use credentials and store in file for future use
    $credential = Get-Credential
    $credential | Export-CliXml -Path $Config
}

try
{
    # Loads WinSCP assembly
    Add-Type -Path (Join-Path $PSScriptRoot "WinSCPnet.dll")

    # Set up session options
    $sessionOptions = New-Object WinSCP.SessionOptions -Property @{
        Protocol = [WinSCP.Protocol]::Sftp
        HostName = "hills.ccsf.edu"
        UserName = $credential.UserName
        SecurePassword = $credential.Password
        SshHostKeyFingerprint = "ssh-rsa 2048 S9gQfX4YbPVLvVSSfxEt4wT3VdI+nNfXHV3Yc8NZ5XA="
    }

    $session = New-Object WinSCP.Session
    # $session.SessionLogPath = Join-Path $PSScriptRoot "winscp.log"

    try
    {
        # Connect
        $session.Open($sessionOptions)

        $results = $session.ExecuteCommand("~abrick/tally | grep -E '^/users/.*png$'")
        $results.Check()

        foreach ($filePath in $results.Output -Split '\r?\n') {
            [Void]$session.GetFiles($filePath, $LocalPath)
        }
    }
    finally
    {
        $session.Dispose()
    }
}
catch
{
    Write-Output "Error: $($_.Exception.Message)"
    exit 1
}
