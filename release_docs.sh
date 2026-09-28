#!/usr/bin/env bash
# Build the package, create a GitHub Release with a ZIP asset, and upload to PyPI.
# Usage:
#   PYPI_TOKEN=... GITHUB_TOKEN=... ./release_docs.sh [repo_url] [project_dir]

set -Eeuo pipefail

REPO_URL="${1:-https://github.com/RknDeveloper/link-shortly}"
PROJECT_DIR="${2:-link-shortly}"
OWNER_REPO="${REPO_URL#https://github.com/}"
OWNER_REPO="${OWNER_REPO%.git}"

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "❌ Required command missing: $1"
        exit 1
    fi
}

require_command git
require_command curl
require_command zip
require_command python3

if [[ -z "${PYPI_TOKEN:-}" ]]; then
    echo "❌ PYPI_TOKEN environment variable is required."
    exit 1
fi
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    echo "❌ GITHUB_TOKEN environment variable is required."
    exit 1
fi

# Do not overwrite an unrelated non-Git directory.
if [[ -e "$PROJECT_DIR" && ! -d "$PROJECT_DIR/.git" ]]; then
    echo "❌ '$PROJECT_DIR' exists but is not a Git repository."
    echo "Use another directory or remove/rename it first."
    exit 1
fi

if [[ -d "$PROJECT_DIR/.git" ]]; then
    echo "🔹 Updating existing repository: $PROJECT_DIR"
    git -C "$PROJECT_DIR" fetch --prune origin
    git -C "$PROJECT_DIR" checkout -q main 2>/dev/null || true
    git -C "$PROJECT_DIR" reset --hard origin/main
    git -C "$PROJECT_DIR" clean -fd
else
    echo "🔹 Cloning repository: $REPO_URL"
    git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

if [[ ! -f shortly/__init__.py ]]; then
    echo "❌ shortly/__init__.py not found. Are you in the correct repository?"
    exit 1
fi

# Works with either single or double quotes around __version__.
VERSION="$(sed -nE "s/^__version__[[:space:]]*=[[:space:]]*['\"]([^'\"]+)['\"]$/\1/p" shortly/__init__.py | head -n1)"
if [[ -z "$VERSION" ]]; then
    echo "❌ Could not detect package version from shortly/__init__.py"
    exit 1
fi

echo "✅ Detected version: $VERSION"

if [[ ! -f pyproject.toml ]]; then
    echo "❌ pyproject.toml not found."
    exit 1
fi

# Termux forbids upgrading its pip package. Only install build if it is absent.
if ! python3 -c 'import build' >/dev/null 2>&1; then
    echo "🔹 Installing build module..."
    python3 -m pip install build
fi

# Twine is checked, not reinstalled. Reinstalling it pulls Rust-only nh3 on Termux.
if ! python3 -m twine --version >/dev/null 2>&1; then
    echo "❌ Twine is not usable. Install it in Termux with:"
    echo "   pip install --no-deps twine==7.0.0"
    echo "   pip install requests requests-toolbelt urllib3 keyring rfc3986 rich packaging pkginfo id"
    exit 1
fi

echo "🔹 Building package..."
rm -rf dist build ./*.egg-info
python3 -m build

shopt -s nullglob
DIST_FILES=(dist/*)
if (( ${#DIST_FILES[@]} == 0 )); then
    echo "❌ Build completed but dist/ is empty."
    exit 1
fi

# Keep the ZIP outside the repository so git clean cannot remove it.
RELEASE_ROOT="$(cd .. && pwd)"
ZIP_FILE="$RELEASE_ROOT/${PROJECT_DIR}-${VERSION}.zip"
rm -f "$ZIP_FILE"
echo "🔹 Creating ZIP: $ZIP_FILE"
zip -qr "$ZIP_FILE" dist README.md LICENSE
if [[ ! -s "$ZIP_FILE" ]]; then
    echo "❌ ZIP was not created or is empty: $ZIP_FILE"
    exit 1
fi

# Check whether the release exists. HTTP 404 is expected for a new release.
RELEASE_URL="https://api.github.com/repos/$OWNER_REPO/releases/tags/v$VERSION"
HTTP_CODE="$(curl -sS -o /tmp/link-shortly-release.json -w '%{http_code}' \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H 'Accept: application/vnd.github+json' \
    "$RELEASE_URL")"

if [[ "$HTTP_CODE" == "200" ]]; then
    echo "⚠ GitHub Release v$VERSION already exists; skipping release creation."
elif [[ "$HTTP_CODE" == "404" ]]; then
    echo "🔹 Creating GitHub Release v$VERSION..."
    API_JSON="$(printf '{"tag_name":"v%s","name":"v%s","body":"Release v%s","draft":false,"prerelease":false}' "$VERSION" "$VERSION" "$VERSION")"
    curl --fail-with-body -sS \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H 'Accept: application/vnd.github+json' \
        -H 'Content-Type: application/json' \
        -d "$API_JSON" \
        "https://api.github.com/repos/$OWNER_REPO/releases" \
        > /tmp/link-shortly-release.json
else
    echo "❌ GitHub API returned HTTP $HTTP_CODE while checking the release."
    cat /tmp/link-shortly-release.json
    exit 1
fi

# Upload the ZIP only when a new release was created. Existing releases are left untouched.
if [[ "$HTTP_CODE" == "404" ]]; then
    UPLOAD_URL="$(python3 - <<'PY'
import json
from pathlib import Path
payload = json.loads(Path('/tmp/link-shortly-release.json').read_text())
print(payload.get('upload_url', '').replace('{?name,label}', ''))
PY
)"
    if [[ -z "$UPLOAD_URL" ]]; then
        echo "❌ GitHub release creation did not return an upload URL."
        cat /tmp/link-shortly-release.json
        exit 1
    fi

    echo "🔹 Uploading ZIP to GitHub Release..."
    curl --fail-with-body -sS \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H 'Accept: application/vnd.github+json' \
        -H 'Content-Type: application/zip' \
        --data-binary "@$ZIP_FILE" \
        "$UPLOAD_URL?name=$(basename "$ZIP_FILE")" >/dev/null
    echo "✅ GitHub ZIP upload complete."
fi

# Upload package files to PyPI. --skip-existing makes reruns safe after a partial release.
echo "🔹 Uploading package to PyPI..."
TWINE_USERNAME='__token__' TWINE_PASSWORD="$PYPI_TOKEN" \
    python3 -m twine upload --skip-existing "${DIST_FILES[@]}"

echo "✅ PyPI upload complete."
echo "🎉 Release v$VERSION completed."
