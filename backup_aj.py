# Legacy helper kept for reference. It simply re-exports the latest
# intent classifier so older scripts can continue to import from here
# without bringing back the Ollama dependency.
from core.intent_engine import understand_intent_llm as _current_intent_handler


def understand_intent_llm(msg: str, _legacy_client=None):
    return _current_intent_handler(msg, _legacy_client)

