# Usage: .\dev.ps1 [up|down|restart|logs|rebuild|ps|clean]
param(
    [ValidateSet("up", "down", "restart", "logs", "rebuild", "ps", "clean")]
    [string]$cmd = "up",
    [string]$service = ""   # optional, e.g. backend or frontend
)

Set-Location $PSScriptRoot   # always run from the project root

switch ($cmd) {
    "up"      { docker compose up -d --build; docker compose ps }
    "down"    { docker compose down }
    "restart" { docker compose restart $service }
    "logs"    { docker compose logs -f --tail 100 $service }
    "rebuild" { docker compose build --no-cache $service; docker compose up -d $service }
    "ps"      { docker compose ps }
    "clean"   { docker compose down -v }   # also deletes volumes (local DB data!)
}