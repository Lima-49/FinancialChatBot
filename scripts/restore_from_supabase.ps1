# Carregar variáveis do arquivo .env
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"')
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
} else {
    Write-Host "[ERRO] Arquivo .env nao encontrado!"
    exit 1
}

# Configurações
$SUPABASE_HOST = $env:SUPABASE_HOST
$SUPABASE_USER = $env:SUPABASE_USER
$SUPABASE_DB = $env:SUPABASE_DB
$LOCAL_DUMP_FILE = $env:LOCAL_DUMP_FILE
$DB_USER = $env:DB_USER
$DB_NAME = $env:DB_NAME

Write-Host "1. Fazendo dump do Supabase..."
pg_dump --dbname $SUPABASE_HOST --format plain --schema=public --no-owner --no-privileges -f $LOCAL_DUMP_FILE

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao gerar dump do Supabase"
    exit 1
}

Write-Host "1.1 Ajustando dump para compatibilidade local..."
$SANITIZED_DUMP_FILE = "$LOCAL_DUMP_FILE.sanitized.sql"
Get-Content $LOCAL_DUMP_FILE | Where-Object {
    $_ -notmatch "^SET transaction_timeout" -and $_ -notmatch "^CREATE SCHEMA public;"
} | Set-Content $SANITIZED_DUMP_FILE

Write-Host "2. Garantindo que o container do banco esteja ativo..."
docker compose up -d db | Out-Null

$DB_CONTAINER_ID = (docker compose ps -q db).Trim()
if (-not $DB_CONTAINER_ID) {
    Write-Host "[ERRO] Nao foi possivel localizar o container do servico 'db'."
    exit 1
}

$DUMP_FILE_NAME = Split-Path -Leaf $SANITIZED_DUMP_FILE

Write-Host "2. Copiando dump para o container..."
docker cp $SANITIZED_DUMP_FILE "${DB_CONTAINER_ID}:/tmp/$DUMP_FILE_NAME"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao copiar dump para o container do banco"
    exit 1
}

Write-Host "3. Recriando banco local para restore limpo..."
docker compose exec -T db psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao remover banco local existente"
    exit 1
}

docker compose exec -T db psql -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME;"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao criar banco local"
    exit 1
}

Write-Host "4. Restaurando no banco local..."
docker compose exec -T db psql `
  -U $DB_USER `
  -d $DB_NAME `
  -v ON_ERROR_STOP=1 `
  -f "/tmp/$DUMP_FILE_NAME"

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Banco restaurado com sucesso!"
    Write-Host "    Arquivo: $LOCAL_DUMP_FILE"
} else {
    Write-Host "[ERRO] Falha ao restaurar"
}