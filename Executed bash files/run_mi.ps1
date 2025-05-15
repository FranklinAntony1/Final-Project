# List of repo names
$repos = @("flask", "fastapi", "django", "tornado", "sanic", "scikit-learn", "statsmodels")

foreach ($repo in $repos) {
    Write-Host "Analyzing  for $repo..."

    radon mi $repo -s > "$repo`_mi.txt"

    Write-Host "Done with $repo"
    Write-Host "----------------------------"
}
