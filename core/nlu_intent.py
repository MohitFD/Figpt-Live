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


def get_intent(msg: str):
    intent, confidence, date, date_range, time, time_range, reason, other = intent_model_call(msg)
    mapped = INTENT_ALIAS.get((intent or "").strip().lower(), intent or "general")

    return {
        "task": mapped,
        "reason": reason or "",
        "language": _detect_language(msg),
        "text": msg,
        "confidence": confidence,
        "slots": {
            "date": date or date_range or "",
            "time": time or "",
            "time_range": time_range or "",
            "other_entities": other or {},
        },
    }
