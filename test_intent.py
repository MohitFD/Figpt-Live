from core.intent_engine import understand_intent_llm

# -------- TEST INPUTS --------
test_inputs = [
    "aj 2 bje thodi der ke liye jana h",
    "kal ghar jana hai",
    "gatepass lagana hai",
    "Doctor ke paas jaana hai",
    "just checking"
]

# -------- RUN TEST --------
for msg in test_inputs:
    print("\n💬 USER:", msg)
    result = understand_intent_llm(msg)
    print("🔍 OUTPUT:", result)

print("\n🎉 TEST COMPLETE!")
