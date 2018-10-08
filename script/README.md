# Script
Contains a Powershell script to fetch peer review files from hills.ccsf.edu to a local Windows computer.

# Requirements
Script was tested using Windows 10 and Powershell 5.0, but it should be compatible with any version. If the script errors, please let me know.

# Usage
Run Get-PeerReview.bat if you don't use Powershell.

If you have already changed the execution policy to allow scripts to run, you can just run Get-PeerReview.ps1.

The first time you use the script, it will prompt for your credentials and store it for later use.

Arguments:

LocalPath - Path to store files in. Defaults to **images** folder in the current directory.

Config - Path for the XML file that stores your credentials. Defaults to $PSScriptRoot/config.xml.

EnterCredentials - Switch to manually enter credentials without storing them.