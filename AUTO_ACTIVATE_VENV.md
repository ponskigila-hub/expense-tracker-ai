# Project-local venv + auto-activation (Windows / Git Bash)

Your `uvicorn` crash happened because the terminal had the **NLP course's shared
venv** (`nlp`) active instead of a venv belonging to this project — that
environment has a different, mismatched set of numpy/pandas/scikit-learn
versions, which is what threw `ValueError: numpy.dtype size changed`.

This sets up a venv that lives **inside `backend/`**, used only by this
project, and (optionally) makes it activate automatically.

## 1. Create the venv

```bash
cd "/c/College Full/Projects/ExpenseTrackerAI/backend"
bash setup_venv.sh
```

This creates `backend/venv/` and installs the exact versions pinned in
`backend/requirements.txt` (the ones this app was actually built against —
not whatever happens to be in the `nlp` environment).

## 2. Auto-activate it

Pick whichever matches how you actually open this project day to day —
you can set up both.

### If you use VS Code

Already done — `.vscode/settings.json` is included in this project and
points VS Code at `backend/venv`. Open the project folder in VS Code, open
a new integrated terminal, and it activates automatically. No extra setup.

(Note: `.vscode/` is git-ignored in this repo, which is normal/expected —
it's machine-specific config, not something to commit.)

### If you work directly in Git Bash (like your `uvicorn` session did)

1. Open (or create) `~/.bashrc` in your home directory.
2. Add this line at the bottom:

   ```bash
   source "/c/College Full/Projects/ExpenseTrackerAI/auto_activate_venv.sh"
   ```

3. Restart Git Bash, or run `source ~/.bashrc`.

From then on, every time you `cd` into this project (or any subfolder of
it), Git Bash switches into `backend/venv` automatically — even if `nlp`
was already active. `cd` back out and it deactivates.

## 3. Verify

```bash
cd "/c/College Full/Projects/ExpenseTrackerAI/backend"
where python
```

The path should now be inside `...ExpenseTrackerAI\backend\venv\...`, not
the NLP course folder. Then:

```bash
uvicorn app.main:app --reload
```

should start cleanly.
