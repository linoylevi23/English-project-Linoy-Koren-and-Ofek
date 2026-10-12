#!/bin/bash
# ==============================================================================
# Google Drive Connection Helper for Team Members
# ==============================================================================

TARGET_DIR="$1"

if [ -z "$TARGET_DIR" ]; then
    echo "🔍 Attempting to auto-detect Google Drive folder..."
    FOUND=$(find "$HOME/Library/CloudStorage" -maxdepth 4 -name "English Recognition Project" 2>/dev/null | head -n 1)
    if [ -n "$FOUND" ]; then
        TARGET_DIR="$FOUND"
        echo "✅ Found shared project folder at:"
        echo "   $TARGET_DIR"
    else
        echo "❌ Could not auto-detect Google Drive folder."
        echo ""
        echo "Usage:"
        echo "   ./connect_drive.sh \"/path/to/GoogleDrive/English Recognition Project\""
        echo ""
        echo "Example (macOS):"
        echo "   ./connect_drive.sh \"\$HOME/Library/CloudStorage/GoogleDrive-user@gmail.com/.../English Recognition Project\""
        exit 1
    fi
fi

# Remove existing symlinks if present
rm -f Audio Transcripts

# Create symbolic links
ln -s "$TARGET_DIR/Audio" Audio
if [ -d "$TARGET_DIR/Transcripts UPDATED" ]; then
    ln -s "$TARGET_DIR/Transcripts UPDATED" Transcripts
    TRANSCRIPTS_SRC="$TARGET_DIR/Transcripts UPDATED"
else
    ln -s "$TARGET_DIR/Transcripts" Transcripts
    TRANSCRIPTS_SRC="$TARGET_DIR/Transcripts"
fi

echo ""
echo "🎉 Connection successful!"
echo "   Audio       -> $TARGET_DIR/Audio"
echo "   Transcripts -> $TRANSCRIPTS_SRC"
echo ""
echo "You can now run:"
echo "   ./run_app.sh    # To start the tagging web app"
echo "   jupyter notebook # Or open the notebook in VS Code"
