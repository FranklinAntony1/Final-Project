# List of repo names
$repos = @("flask", "fastapi", "django", "tornado", "sanic", "scikit-learn", "statsmodels")

foreach ($repo in $repos) {
    Write-Host "Collecting raw metrics for $repo..."
    
    radon raw $repo > "$repo`_raw.txt"

    Write-Host "Done with $repo"
    Write-Host "----------------------------"
}
