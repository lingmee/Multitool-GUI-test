import json


def extract_json_prompts(text: str) -> str:
    """
    Takes the whole .json file content as a string,
    extracts the 'text' field from each prompt,
    and returns them 1 per line.
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return "ERROR: Input file is not valid JSON."

    prompts = data.get("prompts", [])
    extracted = []

    for item in prompts:
        p = item.get("text", "")
        if p:
            p = p.replace("\n", " ").strip()
            extracted.append(p)

    return "\n".join(extracted)
