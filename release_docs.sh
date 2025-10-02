#!/bin/bash
# ==============================================
# Tools Unified Release Script (Public Repo)
# Auto-version detect, GitHub release + ZIP, PyPI upload
# Updated for pyproject.toml support
# Usage: PYPI_TOKEN=token GITHUB_TOKEN=token ./release_docs.sh <repo_url> <project_dir>
# ==============================================

set -e

# ---------------- CHECK TOKENS ----------------
if [ -z "$PYPI_TOKEN" ]; then
    echo "❌ Error: PYPI_TOKEN environment variable is required!"
    exit 1
fi
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable is required!"
    exit 1
fi

# ---------------- INPUT PARAMETERS ----------------
REPO_URL=${1:-"https://github.com/RknDeveloper/link-shortly"}
PROJECT_DIR=${2:-"link-shortly"}
VERSION_FILE="shortly/__init__.py"  # Updated path for new structure

if [ -z "$REPO_URL" ] || [ -z "$PROJECT_DIR" ]; then
    echo "Usage: PYPI_TOKEN=token GITHUB_TOKEN=token ./release_docs.sh <repo_url> <project_dir>"
    exit 1
fi

# ---------------- CLONE OR PULL ----------------
if [ -d "$PROJECT_DIR" ]; then
    echo "🔹 Pulling latest changes in $PROJECT_DIR..."
    cd "$PROJECT_DIR"
    git fetch origin
    git reset --hard origin/main
    git clean -fd
else
    echo "🔹 Cloning repository..."
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# ---------------- DETECT VERSION ----------------
if [ -f "$VERSION_FILE" ]; then
    VERSION=$(grep -E "^__version__ *= *['\"]([0-9]+\.[0-9]+\.[0-9]+)['\"]" "$VERSION_FILE" | cut -d'"' -f2)
else
    echo "❌ Error: Version file $VERSION_FILE not found!"
    exit 1
fi

if [ -z "$VERSION" ]; then
    echo "❌ Error: Could not detect version!"
    exit 1
fi

echo "✅ Detected version: $VERSION"

# ---------------- CLEAN DIST ----------------
echo "🔹 Cleaning previous builds..."
rm -rf dist *.egg-info build

# ---------------- BUILD PACKAGE (pyproject.toml) ----------------
echo "🔹 Building package with pyproject.toml..."
python3 -m pip install --upgrade build
python3 -m build

# ---------------- PREPARE ZIP FOR GITHUB ----------------
echo "🔹 Preparing ZIP for GitHub release..."
cd ..
ZIP_FILE="${PROJECT_DIR}-${VERSION}.zip"
zip -r "$ZIP_FILE" "$PROJECT_DIR/dist" "$PROJECT_DIR/README.md" "$PROJECT_DIR/LICENSE" 2>/dev/null || true

# ---------------- CHECK & CREATE GITHUB RELEASE ----------------
REPO_NAME=$(basename "$REPO_URL" .git)
OWNER_REPO=$(echo "$REPO_URL" | sed 's#https://github.com/##')

# Check if release already exists
EXISTING_TAG=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/$OWNER_REPO/releases/tags/v$VERSION" | grep '"id":' || true)

if [ -n "$EXISTING_TAG" ]; then
    echo "⚠ Release v$VERSION already exists. Skipping creation."
else
    echo "🔹 Creating GitHub release..."
    API_JSON=$(printf '{"tag_name":"v%s","name":"v%s","body":"Release v%s","draft":false,"prerelease":false}' "$VERSION" "$VERSION" "$VERSION")
    RELEASE_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
         -H "Accept: application/vnd.github+json" \
         -d "$API_JSON" \
         "https://api.github.com/repos/$OWNER_REPO/releases")

    UPLOAD_URL=$(echo "$RELEASE_RESPONSE" | grep -Po '"upload_url": "\K[^"]+' | sed 's/{?name,label}//')
    if [ -z "$UPLOAD_URL" ]; then
        echo "❌ GitHub release creation failed!"
        echo "$RELEASE_RESPONSE"
        exit 1
    fi

    # Upload ZIP to GitHub release
    echo "🔹 Uploading ZIP to GitHub release..."
    curl -s -H "Authorization: token $GITHUB_TOKEN" \
         -H "Content-Type: application/zip" \
         --data-binary @"$ZIP_FILE" \
         "$UPLOAD_URL?name=$(basename "$ZIP_FILE")"

    echo "✅ GitHub release created with ZIP attached!"
fi

# ---------------- UPLOAD TO PYPI ----------------
echo "🔹 Uploading package to PyPI..."
cd "$PROJECT_DIR"
python3 -m pip install --upgrade twine
python3 -m twine upload dist/* -u __token__ -p "$PYPI_TOKEN"

echo "✅ PyPI upload done!"
echo "🎉 Release process complete!"