import re


def strip_leading_numbers(text: str) -> str:
    """Removes leading numeric labels like '1.' or '15.' at line start."""
    pattern = re.compile(r"^\s*\d+\.\s*", flags=re.MULTILINE)
    return pattern.sub("", text)
