param(
    [string]$Realm = "realm_52300063",
    [string]$ClientId = "flask-app",
    [string]$Username = "sv01",
    [string]$Password = "sv01@123",
    [string]$KeycloakBaseUrl = "http://localhost:8081",
    [string]$BackendSecureUrl = "http://localhost:8085/secure"
)

$ErrorActionPreference = "Stop"

$tokenEndpoint = "$KeycloakBaseUrl/realms/$Realm/protocol/openid-connect/token"
Write-Host "Token endpoint: $tokenEndpoint"

$body = @{
    grant_type = "password"
    client_id  = $ClientId
    username   = $Username
    password   = $Password
}

try {
    $tokenResponse = Invoke-RestMethod -Method POST -Uri $tokenEndpoint -ContentType "application/x-www-form-urlencoded" -Body $body
} catch {
    Write-Error "Cannot get token from Keycloak. Ensure realm/client/user are imported and Keycloak is up. $($_.Exception.Message)"
    exit 1
}

if (-not $tokenResponse.access_token) {
    Write-Error "No access_token returned from Keycloak."
    exit 1
}

$accessToken = $tokenResponse.access_token
Write-Host "Access token acquired for user '$Username'."

$headers = @{ Authorization = "Bearer $accessToken" }

try {
    $secureResponse = Invoke-RestMethod -Method GET -Uri $BackendSecureUrl -Headers $headers
    Write-Host "Secure endpoint response:"
    $secureResponse | ConvertTo-Json -Depth 8
} catch {
    if ($_.ErrorDetails -and $_.ErrorDetails.Message) {
        Write-Host "Backend response body: $($_.ErrorDetails.Message)"
    }
    Write-Error "Cannot call /secure endpoint. $($_.Exception.Message)"
    exit 1
}
