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
