from core.phi3_inference_v3 import intent_model_call


INTENT_ALIAS = {
    "apply_gate_pass": "apply_gatepass",
    "apply_miss_punch": "apply_missed_punch",
    "general": "general_info",
}


def _detect_language(text: str) -> str:
    if not text:
        return "en"
    devanagari = "अआइईउऊएऐओऔकखगघचछजझटठडढतथदधनपफबभमयरलवशषसह"
    return "hi" if any(ch in text for ch in devanagari) else "en"


def understand_and_decide(message: str) -> dict:
    """
    Lightweight helper that reuses Phi-3 intent classification so the rest
    of the codebase can keep consuming the legacy structure.
    """
    intent, confidence, date, date_range, time, time_range, reason, other = intent_model_call(message)

    mapped_intent = INTENT_ALIAS.get((intent or "").strip().lower(), intent or "general_info")
    lang = _detect_language(message)

    slots = {
        "date": date or "",
        "date_range": date_range or "",
        "time": time or "",
        "time_range": time_range or "",
        "reason": reason or "",
        "other_entities": other or {},
    }

    if not slots["date"] and slots["date_range"]:
        slots["date"] = slots["date_range"]

    result = {
        "intent": mapped_intent,
        "date": slots["date"],
        "leave_type": slots["other_entities"].get("leave_type", ""),
        "reason": slots["reason"],
        "start_time": slots["time"],
        "end_time": slots["time_range"],
        "language": lang,
        "confidence": confidence,
        "slots": slots,
    }

    return result
