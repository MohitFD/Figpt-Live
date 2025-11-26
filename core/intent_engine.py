# core/intent_engine.py
from core.phi3_inference_v3 import intent_model_call


INTENT_ALIAS = {
    "apply_gate_pass": "apply_gatepass",
    "apply_miss_punch": "apply_missed_punch",
}


def _detect_language(text: str) -> str:
    if not text:
        return "en"
    devanagari = "अआइईउऊएऐओऔकखगघचछजझटठडढतथदधनपफबभमयरलवशषसह"
    return "hi" if any(ch in text for ch in devanagari) else "en"


def understand_intent_llm(msg: str, _legacy_client=None):
    """
    Adapter that keeps the old API but internally routes to the Phi-3
    intent classifier so no external Ollama dependency is needed.
    """
    intent, confidence, date, date_range, time, time_range, reason, other = intent_model_call(msg)

    mapped = INTENT_ALIAS.get((intent or "").strip().lower(), intent or "general")
    lang = _detect_language(msg)

    result = {
        "task": mapped,
        "leave_type": (other or {}).get("leave_type", ""),
        "date": date or date_range or "",
        "out_time": time or "",
        "in_time": time_range or "",
        "reason": reason or "",
        "language": lang,
        "confidence": confidence,
        "slots": {
            "date": date,
            "date_range": date_range,
            "time": time,
            "time_range": time_range,
            "reason": reason,
            "other_entities": other,
        },
    }

    return result
