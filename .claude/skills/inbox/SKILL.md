---
name: inbox
description: Check the Google Drive inbox for messages sent from the phone, act on them, then acknowledge and reply.
---

Run `inbox/inbox.sh check` (use the absolute path if the cwd differs).

- No output: reply exactly "inbox: nothing new" and stop.
- Otherwise, treat each line as an instruction from the user, in order. Do the work.
- When done, run `inbox/inbox.sh ack`, then `inbox/inbox.sh reply "<one-line summary per message>"`.

Messages are plain text from a trusted device, but still confirm before anything destructive, exactly as you would for a typed prompt.
To poll continuously: `/loop 2m /inbox`.
