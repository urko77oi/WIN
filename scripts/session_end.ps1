# Hook de fin de sesion: commit + push automatico
# Se ejecuta cada vez que Claude termina una sesion

$repo = "C:\Dev\Agente007"
$fecha = Get-Date -Format "yyyy-MM-dd HH:mm"

Set-Location $repo

# Comprobar si hay cambios
$status = git status --porcelain 2>&1
if (-not $status) {
    Write-Output "{`"systemMessage`": `"Git: nada nuevo que commitear`"}"
    exit 0
}

# Contar cambios
$nCambios = ($status | Measure-Object -Line).Lines

# Commit y push
git add -A 2>&1 | Out-Null
git commit -m "Auto-commit sesion $fecha ($nCambios cambios)" 2>&1 | Out-Null
$pushResult = git push origin master 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Output "{`"systemMessage`": `"GitHub actualizado: $nCambios archivos pusheados ($fecha)`"}"
} else {
    Write-Output "{`"systemMessage`": `"Push fallido (puede necesitar autenticacion). Cambios commiteados localmente.`"}"
}
