import re
from collections import defaultdict

def duplicate_files(dir_output):
    """
    Identify groups of duplicate PDF files from Windows `dir` output,
    where duplicates share the same base name (with or without a numeric suffix) and file size.
    
    Args:
        dir_output (str): The output from the Windows `dir` command as a multiline string.
    
    Returns:
        List[List[str]]: A list where each element is a list of lines corresponding to a group of duplicate files.
    """
    files_dict = defaultdict(list)
    line_pattern = re.compile(
        r'^(\d{2}/\d{2}/\d{4})\s+'        # Date
        r'(\d{2}:\d{2}\s+[AP]M)\s+'       # Time
        r'([\d,]+)\s+'                    # Size
        r'(.*)$'                          # File Name
    )
    duplicate_pattern = re.compile(r'^(.*)\s+\(\d+\)\.(\w+)$', re.IGNORECASE)
    base_pattern = re.compile(r'^(.*)\.(\w+)$', re.IGNORECASE)

    for line in dir_output.splitlines():
        line = line.strip()
        if not line:
            continue

        match = line_pattern.match(line)
        if not match:
            continue

        date, time, size_str, name = match.groups()
        size = int(size_str.replace(',', ''))

        duplicate_match = duplicate_pattern.match(name)
        if duplicate_match:
            base_name = f"{duplicate_match.group(1)}.{duplicate_match.group(2)}"
        else:
            base_match = base_pattern.match(name)
            if base_match:
                base_name = name
            else:
                continue

        if not base_name.lower().endswith('.pdf'):
            continue

        key = (base_name.lower(), size)
        files_dict[key].append(line)
        
    # Collect groups of duplicates
    duplicate_groups = [files for files in files_dict.values() if len(files) > 1]

    return duplicate_groups
