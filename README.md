# claude-inbox 📬

Send messages from a phone to a Claude Code session on a Mac, using a shared Google Drive folder as the transport. No server, no extra accounts.

```
iPhone (Claude app, personal account) ──creates──▶ Drive: claude-inbox/inbox/<timestamp>.txt
                                                         │ Google Drive for desktop syncs
Mac (Claude Code, work account)      ◀──reads────── ~/Library/CloudStorage/GoogleDrive-…/claude-inbox/inbox/
                                      ──moves─────▶ claude-inbox/done/        (after handling)
                                      ──appends───▶ claude-inbox/outbox.md    (replies, readable on the phone)
```

## Files

| Drive path            | Written by | Content |
|-----------------------|-----------|---------|
| `inbox/<ts>.txt`      | phone     | one message per file, name like `2026-09-17T10-00Z.txt` |
| `done/`               | Mac       | handled messages, moved here by `ack` |
| `outbox.md`           | Mac       | one reply per line: `2026-09-17T10:00Z \| mac \| text` |

One file per message avoids concurrent edits to a single file. Drive sync handles a new small file better than an edited one, and the Claude Drive connector can create files but cannot append to them.

## Drive layout (already created)

Folder `claude-inbox` on the personal Drive: https://drive.google.com/drive/folders/1CK22pZqD_L7p4AgB4qrRkA96Qewz6W3d
Subfolders `inbox/` and `done/`, plus `outbox.md`. Share the whole folder with the work Google account (Editor), then the work Mac can sync it.

## Mac setup (one time)

1. Install Google Drive for desktop and sign in to the account that owns or has been shared the `claude-inbox` folder. Make the folder available offline.
2. Clone this repo. If the folder is not auto-detected, write its path to `~/.claude-inbox/config`:
   ```
   CLAUDE_INBOX_DIR="$HOME/Library/CloudStorage/GoogleDrive-you@work.com/Shared drives/…/claude-inbox"
   ```
3. Check: `inbox/inbox.sh status`.
4. Optional: copy `inbox/settings.example.json` into `.claude/settings.local.json`. Then every prompt you type (and every session start) automatically surfaces unread messages as context.

## Using it

- On the phone, tell Claude: "drop a message in my claude-inbox: <message>". A Drive-connected Claude creates `inbox/<timestamp>.txt`. The Drive app itself also works: upload or create a `.txt` in that folder.
- On the Mac, run `/inbox` in Claude Code, or `/loop 2m /inbox` to poll every two minutes.
- Replies land in `outbox.md`; open it in the Drive app or ask Claude on the phone to read it.

## Security notes

Anything dropped into `inbox/` is executed as if you typed it. Share the folder with exactly one other account, and keep it out of any shared drive with broad access.
