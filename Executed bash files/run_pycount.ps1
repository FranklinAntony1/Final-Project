# List of repo names
$repos = @("flask", "fastapi", "django", "tornado", "sanic", "scikit-learn", "statsmodels")

foreach ($repo in $repos) {
    Write-Host "Counting Python files in $repo..."

    $count = (Get-ChildItem -Recurse $repo -Include *.py -File).Count
    "$count" | Out-File "$repo`_pycount.txt"

    Write-Host "$repo contains $count Python files."
    Write-Host "----------------------------"
}
