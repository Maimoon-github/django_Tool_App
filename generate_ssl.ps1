# Set SSL directory path
$sslPath = Join-Path $PSScriptRoot "ssl"

# Create SSL directory if it doesn't exist
if (-not (Test-Path $sslPath)) {
    New-Item -ItemType Directory -Force -Path $sslPath | Out-Null
    Write-Host "Created SSL directory at: $sslPath" -ForegroundColor Green
}

try {
    # Generate self-signed certificate
    $cert = New-SelfSignedCertificate `
        -Subject "localhost" `
        -DnsName "localhost" `
        -KeyAlgorithm RSA `
        -KeyLength 2048 `
        -NotBefore (Get-Date) `
        -NotAfter (Get-Date).AddYears(1) `
        -CertStoreLocation "Cert:\CurrentUser\My" `
        -FriendlyName "Tscript_App Dev Certificate" `
        -HashAlgorithm SHA256 `
        -KeyUsage DigitalSignature, KeyEncipherment, DataEncipherment `
        -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.1")

    # Set certificate password
    $password = ConvertTo-SecureString -String "development_password" -Force -AsPlainText

    # Export paths
    $pfxPath = Join-Path $sslPath "server.pfx"
    $cerPath = Join-Path $sslPath "server.crt"

    # Export PFX certificate
    Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $password | Out-Null
    Write-Host "Generated PFX certificate at: $pfxPath" -ForegroundColor Green

    # Export public key certificate
    Export-Certificate -Cert $cert -FilePath $cerPath -Type CERT | Out-Null
    Write-Host "Generated public certificate at: $cerPath" -ForegroundColor Green

    Write-Host "`nSSL certificates generated successfully!" -ForegroundColor Green
    Write-Host "Use these files in your Gunicorn configuration." -ForegroundColor Yellow
}
catch {
    Write-Host "Error generating SSL certificates: $_" -ForegroundColor Red
    exit 1
}

# Clean up the certificate from store
Get-ChildItem Cert:\CurrentUser\My\ | Where-Object { $_.Subject -eq "CN=localhost" } | Remove-Item
