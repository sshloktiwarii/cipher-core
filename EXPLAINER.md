# cipher-core: The Plain-English Guide

## What does this do?

When software breaks or code fails on your computer, a developer normally has to perform five manual steps:
1. **Notice the error:** Look at terminal error messages or logs.
2. **Remember the fix:** Search past notes or runbooks to see how this was solved before.
3. **Write a code change:** Draft an edit to fix the bug.
4. **Test the fix:** Run the new code to see if the error is resolved.
5. **Save the change:** Create a git commit to save the working code.

`cipher-core` automates these exact five steps in sequence:
* **Step 1: Catches the error** directly from `cipher-log`.
* **Step 2: Searches your documentation** inside `cipher-mem` to find past incident resolutions.
* **Step 3: Drafts a fix** using your local AI model via `cipher-route`.
* **Step 4: Tests the fix inside `cipher-exec`**, ensuring it passes without errors or timeouts.
* **Step 5: Creates a git commit** through `cipher-mcp` once the test succeeds.

The entire 5-step loop executes in less than 20 milliseconds on local hardware.

---

## What happens if I don't use this?

Without `cipher-core`, the platform services run as isolated tools. You would have to manually read logs from one port, copy search queries into another, and run manual terminal commands to verify fixes. `cipher-core` connects all the pieces into an automated loop.

---

## Frequently Asked Questions

#### Can this make unverified changes to my codebase?
No. Step 4 requires the candidate code to pass execution in `cipher-exec` with exit code `0` before Step 5 is allowed to commit anything. If the test fails, the change is rejected.

#### How do I run it?
In the full Cipher system, `cipher appliance` runs `cipher-core` automatically. To run a single test loop manually:
```bash
./cipher-core --once
```
To run it continuously in the background:
```bash
./cipher-core --poll-interval 2s
```
