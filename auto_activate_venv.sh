# ExpenseTrackerAI — auto-activate its own venv in Git Bash
#
# This makes Git Bash automatically switch into backend/venv whenever you
# `cd` anywhere inside this project, and switch back out (deactivate) when
# you leave — so you never accidentally run uvicorn with the "nlp" course
# environment again.
#
# ONE-TIME SETUP:
#   1. Run backend/setup_venv.sh first if you haven't (creates backend/venv).
#   2. Open (or create) ~/.bashrc and add this line at the bottom:
#
#        source "/c/College Full/Projects/ExpenseTrackerAI/auto_activate_venv.sh"
#
#   3. Restart Git Bash, or run:  source ~/.bashrc
#
# From then on, `cd` into any folder under this project and the venv
# activates automatically. cd out, and it deactivates automatically.

_expensetracker_root="/c/College Full/Projects/ExpenseTrackerAI"
_expensetracker_venv="$_expensetracker_root/backend/venv"

_expensetracker_auto_venv() {
  case "$PWD" in
    "$_expensetracker_root"*)
      # Switch into this project's venv even if some other venv (e.g. "nlp")
      # is currently active.
      if [ "$VIRTUAL_ENV" != "$_expensetracker_venv" ] && [ -f "$_expensetracker_venv/Scripts/activate" ]; then
        [ -n "$VIRTUAL_ENV" ] && deactivate 2>/dev/null
        source "$_expensetracker_venv/Scripts/activate"
      fi
      ;;
    *)
      if [ -n "$VIRTUAL_ENV" ] && [ "$VIRTUAL_ENV" = "$_expensetracker_venv" ]; then
        deactivate
      fi
      ;;
  esac
}

# Only hook in once even if this file gets sourced more than once.
case "$PROMPT_COMMAND" in
  *_expensetracker_auto_venv*) ;;
  *) PROMPT_COMMAND="_expensetracker_auto_venv${PROMPT_COMMAND:+; $PROMPT_COMMAND}" ;;
esac
