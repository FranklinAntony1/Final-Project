# List of repo names
$repos = @("flask", "fastapi", "django", "tornado", "sanic", "scikit-learn", "statsmodels")

foreach ($repo in $repos) {
    Write-Host "Analyzing cyclomatic complexity for $repo..."

    radon cc $repo -s > "$repo`_cc.txt"
    radon cc $repo -a > "$repo`_cc_avg.txt"
    radon cc $repo -s --show-closures > "$repo`_cc_funcs.txt"

    Write-Host "Done with $repo"
    Write-Host "----------------------------"
}
