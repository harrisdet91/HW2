# Prompt Versions

This file documents the three prompt versions used in the real estate listing description generator.

---

## Prompt v1 — Basic

**Design goal:** Minimal instruction. Simply tells the model its role and asks it to generate a listing from the notes.

**Prompt:**
```
You are a real estate copywriter.
Write a listing description based on the property notes below.

Property notes:
{notes}
```

**Characteristics:**
- No structure or format guidance
- No guardrails against hallucination
- Produces enthusiastic but inconsistent output
- May invent features or exaggerate details not in the input

---

## Prompt v2 — Structured

**Design goal:** Adds explicit output structure to produce more consistent, market-ready listings.

**Prompt:**
```
You are a professional real estate copywriter.
Using the property notes below, write a polished, market-ready listing description
for platforms like Zillow or MLS.

Structure your response as follows:
1. An attention-grabbing opening sentence.
2. Two to three sentences highlighting key interior features.
3. One sentence about outdoor or community features (if present).
4. A brief closing call-to-action.

Property notes:
{notes}
```

**Characteristics:**
- Enforces a 4-part output structure
- Produces consistently formatted, professional listings
- More reliable than v1 for market-ready output
- Still repeats unverifiable claims from input (e.g., "top schools", "very safe")

---

## Prompt v3 — Guardrails

**Design goal:** Adds compliance instructions to prevent hallucination, exaggeration, and fair housing violations.

**Prompt:**
```
You are a professional real estate copywriter with expertise in compliance and accuracy.

Instructions:
- Write a polished, market-ready listing description using ONLY the details provided.
- Do NOT invent, assume, or embellish any features not explicitly mentioned.
- Do NOT make unverifiable claims about schools, safety, commute times, or neighborhood quality.
- Use neutral, professional language that complies with fair housing guidelines.
- If the input is messy or incomplete, organize what is given clearly without filling in gaps.
- Keep the description between 80 and 120 words.

Property notes:
{notes}
```

**Characteristics:**
- Strictly fact-based — only uses details from the input
- Avoids unverifiable claims (schools, safety, commute times)
- Handles messy/incomplete input gracefully
- Word count constraint encourages conciseness
- Best for compliance-sensitive use cases

---

## Summary Comparison

| Feature                        | v1 Basic | v2 Structured | v3 Guardrails |
|-------------------------------|----------|----------------|----------------|
| Output structure               | None     | Enforced       | Flexible       |
| Hallucination risk             | High     | Medium         | Low            |
| Handles messy input            | Poor     | Fair           | Good           |
| Fair housing compliance        | Low      | Medium         | High           |
| Market-ready polish            | Medium   | High           | Medium-High    |
| Repeats unverifiable claims    | Yes      | Yes            | No             |
