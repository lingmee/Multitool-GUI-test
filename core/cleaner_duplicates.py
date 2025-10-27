def remove_duplicate_and_empty_lines(text: str) -> tuple[str, dict]:
    """Removes duplicate and empty lines from text while preserving order.
    
    Returns:
        tuple: (cleaned_text, stats_dict) where stats_dict contains:
            - 'original_lines': total lines in original text
            - 'empty_lines_removed': number of empty lines removed
            - 'duplicate_lines_removed': number of duplicate lines removed
            - 'final_lines': number of lines in cleaned text
    """
    seen = set()
    result_lines = []
    original_lines = text.splitlines()
    
    empty_count = 0
    duplicate_count = 0
    
    for line in original_lines:
        stripped = line.strip()
        
        if not stripped:
            empty_count += 1
            continue  # skip empty lines
        
        if stripped not in seen:
            seen.add(stripped)
            result_lines.append(line)
        else:
            duplicate_count += 1
    
    stats = {
        'original_lines': len(original_lines),
        'empty_lines_removed': empty_count,
        'duplicate_lines_removed': duplicate_count,
        'final_lines': len(result_lines)
    }
    
    cleaned_text = "\n".join(result_lines) + "\n" if result_lines else ""
    
    return cleaned_text, stats
