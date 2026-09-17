#!/usr/bin/env bash
# Tiny cross-device inbox for Claude Code, transported by Google Drive for desktop.
# Each message is one small text file dropped into  <claude-inbox>/inbox/ .
#
#   inbox.sh check          print unread messages (exit 0 even when none)
#   inbox.sh ack            move every message currently in inbox/ to done/
#   inbox.sh reply "text"   append a reply to outbox.md
#   inbox.sh status         show paths and unread count
#
# Configure with env vars or ~/.claude-inbox/config:
#   CLAUDE_INBOX_DIR   the Drive-synced claude-inbox folder
#                      (default: first match under ~/Library/CloudStorage/GoogleDrive-*/)
set -euo pipefail

STATE_DIR="${CLAUDE_INBOX_STATE:-$HOME/.claude-inbox}"
mkdir -p "$STATE_DIR"
[ -f "$STATE_DIR/config" ] && . "$STATE_DIR/config"

if [ -z "${CLAUDE_INBOX_DIR:-}" ]; then
  CLAUDE_INBOX_DIR="$(find "$HOME/Library/CloudStorage" -maxdepth 4 -type d -name claude-inbox 2>/dev/null | head -n1 || true)"
fi
if [ -z "$CLAUDE_INBOX_DIR" ] || [ ! -d "$CLAUDE_INBOX_DIR" ]; then
  echo "inbox: folder not found. Set CLAUDE_INBOX_DIR in $STATE_DIR/config" >&2
  exit 1
fi

IN="$CLAUDE_INBOX_DIR/inbox"
DONE="$CLAUDE_INBOX_DIR/done"
OUTBOX="$CLAUDE_INBOX_DIR/outbox.md"
mkdir -p "$IN" "$DONE"
touch "$OUTBOX"

# Message files, oldest first (names are timestamps, so lexical order is chronological).
list_unread() {
  find "$IN" -maxdepth 1 -type f \( -name '*.txt' -o -name '*.md' \) ! -name '.*' 2>/dev/null | sort
}

case "${1:-check}" in
  check)
    files="$(list_unread)"
    [ -n "$files" ] || exit 0
    echo "=== Unread messages from phone (run 'inbox.sh ack' after handling) ==="
    while IFS= read -r f; do
      printf -- '--- %s ---\n' "$(basename "$f")"
      cat "$f"; echo
    done <<< "$files"
    ;;
  ack)
    n=0
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      mv "$f" "$DONE/"; n=$((n + 1))
    done <<< "$(list_unread)"
    echo "inbox: acknowledged $n message(s)"
    ;;
  reply)
    shift
    [ $# -gt 0 ] || { echo "usage: inbox.sh reply \"text\"" >&2; exit 2; }
    printf '%s | mac | %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >> "$OUTBOX"
    echo "inbox: reply queued in outbox.md"
    ;;
  status)
    echo "inbox dir : $CLAUDE_INBOX_DIR"
    echo "unread    : $(list_unread | grep -c '' || true)"
    echo "done      : $(find "$DONE" -maxdepth 1 -type f | grep -c '' || true)"
    ;;
  *)
    sed -n '2,9p' "$0"; exit 2 ;;
esac
