[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Invoke-PythonStep {
    param(
        [Parameter(Mandatory)]
        [string]$Label,
        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    Write-Host "==> $Label"
    & $script:pythonExe @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

Invoke-PythonStep -Label "Compile maintained Python" -Arguments @(
    "-m", "compileall", "-q", "human-writing/scripts", "tests", "tools"
)
Invoke-PythonStep -Label "Ruff (E9 + F)" -Arguments @(
    "-m", "ruff", "check", "--select", "E9,F", "--target-version", "py39",
    "human-writing/scripts", "tests", "tools"
)
Invoke-PythonStep -Label "Pytest" -Arguments @("-m", "pytest", "tests", "-q")
Invoke-PythonStep -Label "Validate SKILL.md" -Arguments @(
    "tools\validate_skill.py", "human-writing\SKILL.md"
)
Invoke-PythonStep -Label "Check Markdown links" -Arguments @(
    "tools\check_links.py"
)

Write-Host "WINDOWS DEV CHECK GREEN"
