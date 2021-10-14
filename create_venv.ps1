$options = @("-m","venv")
$requirementsFile = ".\app_req.txt"
$virtualFolder = ".\v_app"

$cmdArgs = @($options,"$virtualFolder")
"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe" @cmdArgs

$ScriptToRun= ".\v_app\Scripts\activate.ps1"
&$ScriptToRun

$options = @("-m","pip", "install", "--upgrade", "pip")
$cmdArgs = @($options)
python @cmdArgs

$options = @("install","-r")
$cmdArgs = @($options,"$requirementsFile")

if (Test-Path -Path $virtualFolder -PathType "Container") {
    if (Test-Path -Path $requirementsFile ) {
        pip @cmdArgs
    }
}

python --version
