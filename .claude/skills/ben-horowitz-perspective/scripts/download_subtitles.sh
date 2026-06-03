#!/usr/bin/env bash
# ============================================================================
# download_subtitles.sh
#
# Download YouTube subtitles for a given video URL, with intelligent fallback
# through subtitle-language and quality tiers.
#
# Priority order (best first):
#   1. Manually authored English subtitles
#   2. Manually authored Chinese subtitles (zh-Hans, zh-CN, zh)
#   3. Any other manually authored subtitles
#   4. Auto-generated English subtitles
#   5. Auto-generated Chinese subtitles
#   6. Any other auto-generated subtitles
#
# Output: SRT files placed in the specified output directory (default ./subs).
# Filenames preserve the video title.
#
# Requirements: yt-dlp must be installed and on PATH.
#   Install: pip install yt-dlp     or     brew install yt-dlp
#
# Usage:
#   bash download_subtitles.sh <YouTube_URL> [output_dir]
#
# Example:
#   bash download_subtitles.sh "https://youtu.be/abc123" ./sources/transcripts
# ============================================================================

set -euo pipefail

# ---------- Argument parsing ----------

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <YouTube_URL> [output_dir]" >&2
  echo "Example: $0 'https://youtu.be/abc123' ./sources/transcripts" >&2
  exit 1
fi

URL="$1"
OUTPUT_DIR="${2:-./subs}"

# ---------- Dependency check ----------

if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "ERROR: yt-dlp is not installed." >&2
  echo "  Install with:  pip install yt-dlp" >&2
  echo "        or:      brew install yt-dlp" >&2
  exit 2
fi

mkdir -p "$OUTPUT_DIR"

echo "==> Target URL:       $URL"
echo "==> Output directory: $OUTPUT_DIR"
echo ""

# ---------- Helper: attempt a single download tier ----------
# $1 = description, $2 = yt-dlp language list, $3 = --write-subs or --write-auto-subs
try_download() {
  local label="$1"
  local langs="$2"
  local mode_flag="$3"

  echo "==> Trying: $label  (langs=$langs)"
  if yt-dlp \
        "$mode_flag" \
        --sub-langs "$langs" \
        --sub-format "srt/vtt/best" \
        --convert-subs srt \
        --skip-download \
        --no-warnings \
        --output "$OUTPUT_DIR/%(title)s.%(ext)s" \
        "$URL" 2>/tmp/ytdlp.err
  then
    # Check that a file was actually written; yt-dlp can return 0 even when
    # no subtitles were available for the requested language.
    if find "$OUTPUT_DIR" -name "*.srt" -newer /tmp/ytdlp.err -print -quit | grep -q .; then
      echo "    SUCCESS: $label"
      return 0
    fi
  fi
  echo "    not available, falling through..."
  return 1
}

# ---------- Tiered attempts ----------

# Tier 1: manually written subtitles, preferred languages first
try_download "manual subtitles (English)"  "en"        "--write-subs" && exit 0
try_download "manual subtitles (Chinese)"  "zh-Hans,zh-CN,zh" "--write-subs" && exit 0
try_download "manual subtitles (any)"      "all"       "--write-subs" && exit 0

# Tier 2: auto-generated subtitles, preferred languages first
try_download "auto-generated (English)"    "en"        "--write-auto-subs" && exit 0
try_download "auto-generated (Chinese)"    "zh-Hans,zh-CN,zh" "--write-auto-subs" && exit 0
try_download "auto-generated (any)"        "all"       "--write-auto-subs" && exit 0

# ---------- All tiers exhausted ----------

echo "" >&2
echo "ERROR: no subtitles of any kind could be downloaded for this URL." >&2
echo "       Last yt-dlp stderr:" >&2
sed 's/^/         /' /tmp/ytdlp.err >&2
exit 3
