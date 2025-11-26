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


def llm_understand_message(message):
    intent, confidence, date, date_range, time, time_range, reason, other = intent_model_call(message)
    normalized = INTENT_ALIAS.get((intent or "").strip().lower(), intent or "unknown")

    return {
        "intent": normalized,
        "date": date or date_range or "",
        "time_out": time or "",
        "time_in": time_range or "",
        "leave_type": (other or {}).get("leave_type"),
        "reason": reason or "",
        "language": _detect_language(message),
        "confidence": confidence,
        "slots": {
            "date": date,
            "date_range": date_range,
            "time": time,
            "time_range": time_range,
            "other_entities": other,
        },
    }
