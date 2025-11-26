def generate_fixhr_reply(intent, api_result):
    """
    Lightweight textual response generator that keeps everything local.
    """
    success_phrases = {
        "apply_leave": "✅ Leave request submit ho gaya.",
        "apply_gatepass": "✅ Gatepass request bhej diya.",
        "apply_missed_punch": "✅ Missed punch request bhej diya.",
        "leave_balance": "ℹ️ Leave balance fetch kar liya.",
        "attendance_report": "📊 Attendance report ready hai.",
    }

    failure_prefix = "⚠️ "

    data = api_result or {}
    if not isinstance(data, dict):
        return str(data)

    message = data.get("message") or data.get("result_message") or ""
    status = data.get("status") or data.get("success")

    if status in [True, "true", "success"]:
        return success_phrases.get(intent, "✅ Task complete ho gaya.")

    return f"{failure_prefix}{message or 'Kuch error aa gaya, thodi der baad try karein.'}"
