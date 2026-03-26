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
$CONTAINER_NAME = $env:CONTAINER_NAME
$DB_USER = $env:DB_USER
$DB_NAME = $env:DB_NAME

Write-Host "1. Fazendo dump do Supabase..."
pg_dump --dbname $SUPABASE_HOST --format plain -f $LOCAL_DUMP_FILE

Write-Host "2. Copiando dump para o container..."
docker cp $LOCAL_DUMP_FILE "${CONTAINER_NAME}:/tmp/"

Write-Host "3. Restaurando no banco local..."
docker exec -it $CONTAINER_NAME psql `
  -U $DB_USER `
  -d $DB_NAME `
  -f "/tmp/$LOCAL_DUMP_FILE"

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Banco restaurado com sucesso!"
    Write-Host "    Arquivo: $LOCAL_DUMP_FILE"
} else {
    Write-Host "[ERRO] Falha ao restaurar"
}