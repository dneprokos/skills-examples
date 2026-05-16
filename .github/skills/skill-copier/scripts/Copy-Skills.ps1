<#
.SYNOPSIS
    Copies skills from one tool folder to another within the repository.

.PARAMETER Source
    The source tool key: .claude | .cursor | .github

.PARAMETER Destination
    The destination tool key: .claude | .cursor | .github

.PARAMETER Overwrite
    When set, overwrites skills that already exist in the destination.
    Default behaviour is to skip existing skills.

.PARAMETER DryRun
    When set, shows what would be copied/skipped without making any changes.

.EXAMPLE
    .\Copy-Skills.ps1 -Source .github -Destination .claude
    .\Copy-Skills.ps1 -Source .github -Destination .cursor -Overwrite
    .\Copy-Skills.ps1 -Source .github -Destination .claude -DryRun
#>

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('.claude', '.cursor', '.github')]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [ValidateSet('.claude', '.cursor', '.github')]
    [string]$Destination,

    [switch]$Overwrite,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ── Path resolution ────────────────────────────────────────────────────────────

$folderMap = @{
    '.claude' = '.claude/skills'
    '.cursor' = '.cursor/skills'
    '.github' = '.github/skills'
}

$sourcePath = $folderMap[$Source]
$destPath   = $folderMap[$Destination]

if ($Source -eq $Destination) {
    Write-Error "Source and destination must be different folders."
    exit 1
}

if (-not (Test-Path $sourcePath)) {
    Write-Error "Source folder '$sourcePath' does not exist."
    exit 1
}

$sourceSkills = Get-ChildItem $sourcePath -Directory -ErrorAction SilentlyContinue
if (-not $sourceSkills) {
    Write-Warning "Source folder '$sourcePath' contains no skill sub-folders."
    exit 0
}

# ── Ensure destination exists ──────────────────────────────────────────────────

if (-not (Test-Path $destPath)) {
    if ($DryRun) {
        Write-Host "[DRY RUN] Would create destination folder: $destPath"
    } else {
        New-Item -ItemType Directory -Force -Path $destPath | Out-Null
        Write-Host "Created destination folder: $destPath"
    }
}

# ── Copy loop ──────────────────────────────────────────────────────────────────

$copied  = [System.Collections.Generic.List[string]]::new()
$skipped = [System.Collections.Generic.List[string]]::new()
$failed  = [System.Collections.Generic.List[string]]::new()

foreach ($skill in $sourceSkills) {
    $destSkill = Join-Path $destPath $skill.Name

    if (Test-Path $destSkill) {
        if ($Overwrite) {
            if ($DryRun) {
                Write-Host "[DRY RUN] Would overwrite: $($skill.Name)"
                $copied.Add($skill.Name)
            } else {
                try {
                    Remove-Item -Recurse -Force $destSkill
                    Copy-Item -Recurse $skill.FullName $destSkill
                    $copied.Add($skill.Name)
                } catch {
                    Write-Warning "Failed to overwrite '$($skill.Name)': $_"
                    $failed.Add($skill.Name)
                }
            }
        } else {
            $skipped.Add($skill.Name)
        }
    } else {
        if ($DryRun) {
            Write-Host "[DRY RUN] Would copy: $($skill.Name)"
            $copied.Add($skill.Name)
        } else {
            try {
                Copy-Item -Recurse $skill.FullName $destSkill
                $copied.Add($skill.Name)
            } catch {
                Write-Warning "Failed to copy '$($skill.Name)': $_"
                $failed.Add($skill.Name)
            }
        }
    }
}

# ── Summary ────────────────────────────────────────────────────────────────────

$prefix = if ($DryRun) { "[DRY RUN] " } else { "" }
Write-Host ""
Write-Host "${prefix}Copy complete: $sourcePath → $destPath"
Write-Host "  Copied  : $($copied.Count)"
Write-Host "  Skipped : $($skipped.Count) (already exist)"
Write-Host "  Failed  : $($failed.Count)"

if ($copied.Count -gt 0) {
    Write-Host ""
    Write-Host "Copied skills:"
    $copied | ForEach-Object { Write-Host "  + $_" }
}

if ($skipped.Count -gt 0) {
    Write-Host ""
    Write-Host "Skipped (already in destination):"
    $skipped | ForEach-Object { Write-Host "  ~ $_" }
}

if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "Failed:"
    $failed | ForEach-Object { Write-Host "  ! $_" }
    exit 1
}
