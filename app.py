import os
import argparse
import requests
import json

# ---------------------------------------------------------------------------
# Evaluation set – 5 example inputs
# ---------------------------------------------------------------------------
TEST_CASES = {
    "case1": "3 bed, 2.5 bath single-family home. Updated kitchen with quartz countertops, "
             "finished basement, fenced backyard, and two-car garage.",

    "case2": "2 bed, 2 bath condo with 1,250 sq ft. Open layout, attached garage, "
             "HOA-maintained exterior, close to shopping and highways.",

    "case3": "Townhome end unit more windows nice kitchen near hospital deck "
             "unfinished basement bath updated maybe 2022",

    "case4": "4 bed, 3 bath home in great neighborhood, top schools, very safe, "
             "10 minutes from downtown",

    "case5": "3 bed, 2.5 bath townhome for rent. Smart switches, automated shades, "
             "finished basement, deck, quick highway access, near Cleveland Clinic.",
}

# ---------------------------------------------------------------------------
# Prompt versions
# ---------------------------------------------------------------------------
PROMPTS = {
    "v1": (
        "You are a real estate copywriter. "
        "Write a listing description based on the property notes below.\n\n"
        "Property notes:\n{notes}"
    ),

    "v2": (
        "You are a professional real estate copywriter. "
        "Using the property notes below, write a polished, market-ready listing description "
        "for platforms like Zillow or MLS.\n\n"
        "Structure your response as follows:\n"
        "1. An attention-grabbing opening sentence.\n"
        "2. Two to three sentences highlighting key interior features.\n"
        "3. One sentence about outdoor or community features (if present).\n"
        "4. A brief closing call-to-action.\n\n"
        "Property notes:\n{notes}"
    ),

    "v3": (
        "You are a professional real estate copywriter with expertise in compliance and accuracy.\n\n"
        "Instructions:\n"
        "- Write a polished, market-ready listing description using ONLY the details provided.\n"
        "- Do NOT invent, assume, or embellish any features not explicitly mentioned.\n"
        "- Do NOT make unverifiable claims about schools, safety, commute times, or neighborhood quality.\n"
        "- Use neutral, professional language that complies with fair housing guidelines.\n"
        "- If the input is messy or incomplete, organize what is given clearly without filling in gaps.\n"
        "- Keep the description between 80 and 120 words.\n\n"
        "Property notes:\n{notes}"
    ),
}

# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def build_prompt(prompt_version: str, notes: str) -> str:
    template = PROMPTS[prompt_version]
    return template.format(notes=notes)


def call_llm(prompt: str) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        },
    }
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()
    parts = result["candidates"][0]["content"]["parts"]
    # Concatenate all text parts, skipping any internal "thought" parts
    text = " ".join(p["text"] for p in parts if "text" in p).strip()
    return text


def save_output(case_key: str, prompt_version: str, notes: str, output: str) -> str:
    filename = f"output_{case_key}_{prompt_version}.txt"
    with open(filename, "w") as f:
        f.write(f"CASE: {case_key}\n")
        f.write(f"PROMPT VERSION: {prompt_version}\n")
        f.write("-" * 50 + "\n")
        f.write("INPUT:\n")
        f.write(notes + "\n")
        f.write("-" * 50 + "\n")
        f.write("OUTPUT:\n")
        f.write(output + "\n")
    return filename


def print_result(case_key: str, prompt_version: str, notes: str, output: str) -> None:
    print("\n" + "=" * 60)
    print(f"  CASE:           {case_key}")
    print(f"  PROMPT VERSION: {prompt_version}")
    print("=" * 60)
    print("\n--- INPUT ---")
    print(notes)
    print("\n--- OUTPUT ---")
    print(output)
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a real estate listing description using an LLM."
    )
    parser.add_argument(
        "--case",
        choices=TEST_CASES.keys(),
        default="case1",
        help="Test case to run (default: case1)",
    )
    parser.add_argument(
        "--prompt",
        choices=PROMPTS.keys(),
        default="v1",
        help="Prompt version to use (default: v1)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    notes = TEST_CASES[args.case]
    prompt = build_prompt(args.prompt, notes)

    print(f"\nRunning {args.case} with prompt {args.prompt}...")
    output = call_llm(prompt)

    print_result(args.case, args.prompt, notes, output)

    saved_file = save_output(args.case, args.prompt, notes, output)
    print(f"Output saved to: {saved_file}\n")


if __name__ == "__main__":
    main()
