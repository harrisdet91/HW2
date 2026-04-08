# Report: Real Estate Listing Description Generator

## Overview

This project builds a Python prototype that uses the Google Gemini API (gemini-2.5-flash) to automatically generate real estate listing descriptions from structured or semi-structured property notes. The goal is to evaluate how different prompt strategies affect output quality, accuracy, and compliance.

---

## Workflow

**Task:** Generate professional real estate listing descriptions from property notes.

**User:** Real estate agents, leasing agents, or homeowners preparing listings.

**Input:** Structured or semi-structured property details (bedrooms, bathrooms, sq ft, features, location highlights).

**Output:** A polished, market-ready listing description suitable for Zillow, MLS, or rental sites.

---

## Evaluation Setup

The app was tested across 5 cases and 3 prompt versions (15 total runs).

### Test Cases

| Case   | Description              | Key Challenge                          |
|--------|--------------------------|----------------------------------------|
| case1  | Standard single-family home | Baseline — clean, complete input     |
| case2  | Basic condo              | Avoid luxury/exaggerated language      |
| case3  | Messy/incomplete input   | Organize without guessing missing info |
| case4  | Hallucination risk       | Avoid unverifiable claims              |
| case5  | Rental listing           | Use rental-focused language            |

### Prompt Versions

| Version | Strategy     | Description                                              |
|---------|--------------|----------------------------------------------------------|
| v1      | Basic        | Minimal instruction, no structure or guardrails          |
| v2      | Structured   | Enforces a 4-part output format                          |
| v3      | Guardrails   | Adds compliance rules and hallucination prevention       |

---

## Results by Case

### Case 1 — Standard Single-Family Home
- **v1:** Generated a decent listing but lacked consistent structure.
- **v2:** Produced a polished, well-structured description with a strong opening and call-to-action.
- **v3:** Delivered a factual, concise listing using only provided details — no embellishment.

### Case 2 — Basic Condo
- **v1:** Enthusiastic tone but introduced unsupported lifestyle claims.
- **v2:** Well-structured and professional; emphasized low-maintenance and convenience.
- **v3:** ✅ Best result — neutral, accurate, and realistic without exaggeration.

### Case 3 — Messy Input
- **v1:** Filled in missing details freely, inventing features not in the input.
- **v2:** Organized the input but still added unverified flair (e.g., "perfect for culinary adventures").
- **v3:** ✅ Best result — organized the messy notes clearly, flagged uncertainty, avoided guessing.

### Case 4 — Hallucination Risk
- **v1:** Repeated all unverifiable claims (top schools, very safe, 10 min from downtown) without hesitation.
- **v2:** Repeated claims in polished language — still included safety and school references.
- **v3:** ✅ Best result — stripped unverifiable claims entirely, kept only factual bedroom/bathroom details.

### Case 5 — Rental Listing
- **v1:** Used rental language but leaned heavily into marketing fluff.
- **v2:** ✅ Best result — most complete and polished rental description with a clear call-to-action.
- **v3:** Factual and compliant rental description; practical but less engaging.

---

## Key Findings

1. **v1 (Basic)** is unreliable for professional use. It freely invents details and repeats unverifiable claims. Useful only for quick, informal drafts.

2. **v2 (Structured)** produces the most market-ready, engaging listings. The enforced structure makes output consistent and professional. However, it does not filter out unverifiable claims from the input.

3. **v3 (Guardrails)** is the safest and most compliant prompt. It excels at handling messy input and avoiding hallucination. It is the best choice for compliance-sensitive scenarios (fair housing, MLS submissions).

4. **Prompt design has a significant impact** on output quality, tone, and factual accuracy — even with the same input and model.

---

## Recommendation

For a production real estate listing tool, a **hybrid approach** is ideal:
- Use **v2 structure** for formatting consistency.
- Apply **v3 guardrails** for compliance and accuracy.
- Allow agents to review and edit the draft before publishing.

---

## Technical Notes

- **Model:** Google Gemini 2.5 Flash via REST API
- **Language:** Python 3.8
- **API Call Method:** Direct HTTP requests using the `requests` library
- **Token Limit:** 1024 output tokens per call
- **Temperature:** 0.7
- **Output:** Printed to terminal and saved to `.txt` files per run
