<#
.SYNOPSIS
  MySkills installer for Windows PowerShell.

.DESCRIPTION
  Clones the MySkills repository into the canonical skills folder and wires it
  into every agent that reads from a standard skills directory. Safe to re-run:
  it updates the clone and never deletes an existing agent skill folder.

  Directory links use NTFS junctions, so no administrator rights and no
  Developer Mode are required.

.EXAMPLE
  irm https://raw.githubusercontent.com/FYI88/MYSKILLS/main/install.ps1 | iex

.EXAMPLE
  .\install.ps1 -Force
#>
[CmdletBinding()]
param(
  [string]$Repo = $(if ($env:MYSKILLS_REPO) { $env:MYSKILLS_REPO } else { 'https://github.com/FYI88/MYSKILLS.git' }),
  [string]$Branch = $(if ($env:MYSKILLS_BRANCH) { $env:MYSKILLS_BRANCH } else { 'main' }),
  [string]$Dir = $(if ($env:MYSKILLS_DIR) { $env:MYSKILLS_DIR } else { Join-Path $HOME '.agents\skills' }),
  [switch]$NoLink,
  [switch]$NoHermes,
  [switch]$Force,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Write-Step { param([string]$Message) Write-Host "`n==> $Message" -ForegroundColor Cyan }
function Write-Log  { param([string]$Message) Write-Host "  $Message" }
function Write-Warn { param([string]$Message) Write-Host "  ! $Message" -ForegroundColor Yellow }
function Write-Err  { param([string]$Message) Write-Host "  x $Message" -ForegroundColor Red }

function Invoke-Action {
  param([scriptblock]$Action, [string]$Description)
  if ($DryRun) {
    Write-Log "[dry-run] $Description"
  } else {
    & $Action
  }
}

function Invoke-Git {
  param([string[]]$Arguments)
  $previous = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    & git @Arguments 2>&1 | ForEach-Object { Write-Log $_ }
    if ($LASTEXITCODE -ne 0) { throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE" }
  } finally {
    $ErrorActionPreference = $previous
  }
}

$linkTargets = @(
  (Join-Path $HOME '.claude\skills'),
  (Join-Path $HOME '.pi\agent\skills'),
  (Join-Path $HOME '.config\opencode\skills')
)
$hermesTarget = Join-Path $HOME '.hermes\skills'

Write-Step 'Checking prerequisites'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Err 'git is required. Install Git for Windows, then re-run this script.'
  exit 1
}
Write-Log "git: $((& git --version 2>$null) -join ' ')"
Write-Log "canonical: $Dir"

Write-Step 'Installing the canonical skill collection'
$parent = Split-Path -Parent $Dir
if (-not (Test-Path -LiteralPath $parent)) {
  Invoke-Action -Description "create $parent" -Action { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
}

$gitDir = Join-Path $Dir '.git'
if (Test-Path -LiteralPath $gitDir) {
  $remote = ((& git -C $Dir remote get-url origin 2>$null) -join '').Trim()
  if ($remote -and ($remote -match 'MYSKILLS' -or $remote -match 'myskills')) {
    Write-Log 'existing clone found - updating'
    Invoke-Action -Description "git -C $Dir pull --ff-only origin $Branch" -Action {
      Invoke-Git @('-C', $Dir, 'pull', '--ff-only', 'origin', $Branch)
    }
  } else {
    Write-Err "$Dir is a git repo for a different remote ($remote)."
    Write-Err 'Re-run with -Dir PATH to use a different location, or move the folder aside.'
    exit 1
  }
} elseif ((Test-Path -LiteralPath $Dir) -and (Get-ChildItem -LiteralPath $Dir -Force | Measure-Object).Count -gt 0) {
  Write-Err "$Dir exists and is not empty, and is not a git clone of MYSKILLS."
  Write-Err 'Re-run with -Dir PATH to use a different location, or move the folder aside.'
  exit 1
} else {
  Write-Log "cloning $Repo"
  Invoke-Action -Description "git clone --branch $Branch $Repo $Dir" -Action {
    Invoke-Git @('clone', '--branch', $Branch, $Repo, $Dir)
  }
}

$skillCount = (Get-ChildItem -LiteralPath $Dir -Recurse -Filter 'SKILL.md' -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notlike '*\.git\*' } | Measure-Object).Count
Write-Log "$skillCount skills available"

if ($NoLink) {
  Write-Step 'Done (agent linking skipped)'
  exit 0
}

function Test-Junction {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) { return $false }
  $item = Get-Item -LiteralPath $Path -Force
  return ($item.LinkType -eq 'Junction' -or $item.Attributes -band [IO.FileAttributes]::ReparsePoint)
}

function Get-LinkTarget {
  param([string]$Path)
  try { return (Get-Item -LiteralPath $Path -Force).Target } catch { return $null }
}

function Merge-SkillsInto {
  param([string]$TargetDir)
  $linked = 0
  $kept = 0
  Get-ChildItem -LiteralPath $Dir -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')
  } | ForEach-Object {
    $dest = Join-Path $TargetDir $_.Name
    if (Test-Path -LiteralPath $dest) {
      if ((Test-Junction -Path $dest) -and ((Get-LinkTarget -Path $dest) -eq $_.FullName)) {
        return
      }
      if ($Force -and (Test-Junction -Path $dest)) {
        Invoke-Action -Description "remove $dest" -Action { Remove-Item -LiteralPath $dest -Force -Recurse }
      } else {
        $kept++
        return
      }
    }
    Invoke-Action -Description "link $($_.Name) -> $($_.FullName)" -Action {
      New-Item -ItemType Junction -Path $dest -Target $_.FullName | Out-Null
    }
    $linked++
  }
  Write-Log "linked $linked new skill(s), kept $kept existing entr(ies) untouched"
}

Write-Step 'Linking agent skill folders'
foreach ($target in $linkTargets) {
  if (Test-Path -LiteralPath $target) {
    if (Test-Junction -Path $target) {
      $current = Get-LinkTarget -Path $target
      if ($current -eq $Dir) {
        Write-Log "already linked: $target"
        continue
      }
      if ($Force) {
        Write-Log "repointing: $target -> $Dir"
        Invoke-Action -Description "remove $target" -Action { Remove-Item -LiteralPath $target -Force -Recurse }
        Invoke-Action -Description "junction $target -> $Dir" -Action {
          New-Item -ItemType Junction -Path $target -Target $Dir | Out-Null
        }
      } else {
        Write-Warn "$target points to $current (use -Force to repoint)"
      }
      continue
    }
    Write-Log "existing folder found, merging skills into it: $target"
    Merge-SkillsInto -TargetDir $target
    continue
  }
  $targetParent = Split-Path -Parent $target
  if (-not (Test-Path -LiteralPath $targetParent)) {
    Invoke-Action -Description "create $targetParent" -Action { New-Item -ItemType Directory -Path $targetParent -Force | Out-Null }
  }
  Write-Log "linking: $target -> $Dir"
  Invoke-Action -Description "junction $target -> $Dir" -Action {
    New-Item -ItemType Junction -Path $target -Target $Dir | Out-Null
  }
}

if (-not $NoHermes) {
  Write-Step 'Copying skills for Hermes (independent copy, as Hermes snapshots on start)'
  if ($DryRun) {
    Write-Log "[dry-run] copy skills -> $hermesTarget"
  } else {
    if (-not (Test-Path -LiteralPath $hermesTarget)) {
      New-Item -ItemType Directory -Path $hermesTarget -Force | Out-Null
    }
    $copied = 0
    Get-ChildItem -LiteralPath $Dir -Directory | Where-Object {
      Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')
    } | ForEach-Object {
      $dest = Join-Path $hermesTarget $_.Name
      if ((Test-Path -LiteralPath $dest) -and (-not $Force)) { return }
      if (Test-Path -LiteralPath $dest) { Remove-Item -LiteralPath $dest -Force -Recurse }
      Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force
      $copied++
    }
    Write-Log "copied $copied skill(s) to $hermesTarget"
  }
}

Write-Step 'Done'
Write-Log 'Re-run this script anytime to pull the latest skills.'
Write-Log "Browse the catalog: $(Join-Path $Dir 'CATALOG.md')"
