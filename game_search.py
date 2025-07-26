#!/usr/bin/env python3
"""
Game Similarity Scoring Utilities

This module provides enhanced similarity scoring algorithms for matching game names.
Used by both the main application search and CSV import functionality.
"""
import re


# Common game edition suffixes for normalization
EDITION_SUFFIXES = [
    ' (pre-purchase)',
    ' - standard edition',
    ' - deluxe edition',
    ' - ultimate edition',
    ' - game of the year edition',
    ' - goty edition',
    ' - collector\'s edition',
    ' - special edition',
    ' - limited edition',
    ' - enhanced edition',
    ' - definitive edition',
    ' - complete edition',
    ' - gold edition',
    ' - platinum edition',
    ' - premium edition',
    ' - remastered edition',
    ' remastered edition',
    ' - remastered',
    ' remastered',
    'standard edition (pre-purchase)',
    # Variations without dashes
    ' standard edition',
    ' deluxe edition',
    ' ultimate edition',
    ' game of the year edition',
    ' goty edition',
    ' collector\'s edition',
    ' special edition',
    ' limited edition',
    ' enhanced edition',
    ' definitive edition',
    ' complete edition',
    ' gold edition',
    ' platinum edition',
    ' premium edition',
]


def extract_numbers(text):
    """Extract all numbers from text as a set."""
    numbers = re.findall(r'\d+', text)
    return set(numbers)


def roman_to_int(roman):
    """Convert Roman numeral to integer."""
    if not roman:
        return None
    
    roman = roman.upper()
    roman_numerals = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    for char in reversed(roman):
        if char not in roman_numerals:
            return None
        value = roman_numerals[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    
    return total


def int_to_roman(num):
    """Convert integer to Roman numeral."""
    if not isinstance(num, int) or num <= 0 or num > 3999:
        return None
    
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    
    result = ''
    for i, value in enumerate(values):
        count = num // value
        result += numerals[i] * count
        num -= value * count
    
    return result


def normalize_numbers_in_title(title):
    """Convert numbers to both Roman and Arabic numerals for comparison."""
    # Pattern to find Roman numerals (I, II, III, IV, V, etc.)
    roman_pattern = r'\b([IVX]+)\b'
    # Pattern to find Arabic numbers
    arabic_pattern = r'\b(\d+)\b'
    
    # Normalize punctuation for better matching
    normalized_title = re.sub(r'[:\-\–\—]', ' ', title)  # Replace colons, hyphens, dashes with spaces
    normalized_title = re.sub(r'\s+', ' ', normalized_title).strip()  # Collapse multiple spaces
    
    variations = [normalized_title.lower()]
    
    # Convert Roman numerals to Arabic
    for match in re.finditer(roman_pattern, normalized_title, re.IGNORECASE):
        roman = match.group(1)
        arabic = roman_to_int(roman)
        if arabic:
            # Create variation with Arabic numeral
            variation = normalized_title[:match.start()] + str(arabic) + normalized_title[match.end():]
            variation = re.sub(r'\s+', ' ', variation).strip()  # Clean up spaces
            variations.append(variation.lower())
    
    # Convert Arabic numbers to Roman
    for match in re.finditer(arabic_pattern, normalized_title):
        num = int(match.group(1))
        roman = int_to_roman(num)
        if roman:
            # Create variation with Roman numeral
            variation = normalized_title[:match.start()] + roman + normalized_title[match.end():]
            variation = re.sub(r'\s+', ' ', variation).strip()  # Clean up spaces
            variations.append(variation.lower())
    
    return variations


def extract_cost_from_string(cost_str):
    """Extract numeric cost from a string like '$39.94' or '($1.11)'."""
    if not cost_str:
        return 0
    
    # Remove currency symbols and spaces
    clean_str = re.sub(r'[^\d\.\-\(\)]', '', cost_str)
    
    # Handle parentheses (negative values)
    if '(' in clean_str and ')' in clean_str:
        clean_str = clean_str.replace('(', '').replace(')', '')
        negative = True
    else:
        negative = False
    
    try:
        value = float(clean_str)
        return -value if negative else value
    except ValueError:
        return 0


def normalize_game_name(game_name):
    """
    Normalize a game name by removing common edition suffixes.
    
    Args:
        game_name (str): The game name to normalize
        
    Returns:
        tuple: (base_name, removed_suffix) where removed_suffix is None if no suffix was found
    """
    clean_name = game_name.lower().strip()
    
    for suffix in EDITION_SUFFIXES:
        if clean_name.endswith(suffix):
            base_name = clean_name[:-len(suffix)].strip()
            return base_name, suffix
    
    return clean_name, None


def is_edition_variant(game_name1, game_name2):
    """
    Check if two game names are likely the same game with different editions.
    
    Args:
        game_name1 (str): First game name
        game_name2 (str): Second game name
        
    Returns:
        bool: True if they appear to be edition variants of the same game
    """
    base1, suffix1 = normalize_game_name(game_name1)
    base2, suffix2 = normalize_game_name(game_name2)
    
    # If base names match, they're likely edition variants
    return base1 == base2 and (suffix1 or suffix2)


def calculate_missing_text_penalty(search_term, game_name):
    """Calculate penalty based on missing text between search and game name."""
    # Clean and normalize both strings
    search_clean = search_term.lower().strip()
    game_clean = game_name.lower().strip()
    
    # Calculate how much of the search term is missing from the game name
    search_words = set(search_clean.split())
    game_words = set(game_clean.split())
    
    # Find missing words
    missing_words = search_words - game_words
    
    # Calculate character-level missing percentage
    search_chars = set(search_clean.replace(' ', ''))
    game_chars = set(game_clean.replace(' ', ''))
    missing_chars = search_chars - game_chars
    
    penalty = 0
    
    # Word-level penalty
    if search_words:
        missing_word_ratio = len(missing_words) / len(search_words)
        penalty += missing_word_ratio * 120  # Heavy penalty for missing words
    
    # Character-level penalty
    if search_chars:
        missing_char_ratio = len(missing_chars) / len(search_chars)
        penalty += missing_char_ratio * 80  # Moderate penalty for missing characters
    
    # Length difference penalty - penalize if game name is much longer than search
    length_diff = len(game_clean) - len(search_clean)
    if length_diff > 0:
        # Penalty grows with length difference, but caps out
        penalty += min(length_diff * 2, 60)
    
    # Extra penalty if search term is very short and game name is long
    if len(search_clean) <= 3 and len(game_clean) > 10:
        penalty += 40
    
    return penalty


def levenshtein_distance(s1, s2):
    """Calculate Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def calculate_similarity_score(search_term, game_name):
    """
    Calculate similarity score between search term and game name (higher = better match).
    
    This algorithm considers:
    - Exact matches (highest score)
    - Number matching for sequels
    - Missing text penalties
    - Word and character overlap
    - Common abbreviations
    - Position-based bonuses
    
    Args:
        search_term (str): The search query
        game_name (str): The game name to compare against
        
    Returns:
        float: Similarity score (higher = better match)
    """
    # Exact match gets highest score
    if search_term == game_name:
        return 1000
    
    # Calculate different types of matches and assign scores
    score = 0
    
    # Number matching bonus - prioritize games with numbers if search has numbers
    search_numbers = extract_numbers(search_term)
    game_numbers = extract_numbers(game_name)
    
    if search_numbers and game_numbers:
        # Both have numbers - big bonus for matching numbers
        common_numbers = search_numbers.intersection(game_numbers)
        if common_numbers:
            score += len(common_numbers) * 150  # High bonus for matching numbers
        # Penalty for mismatched numbers
        mismatched_numbers = len(search_numbers.symmetric_difference(game_numbers))
        score -= mismatched_numbers * 30
    elif search_numbers and not game_numbers:
        # Search has numbers but game doesn't - significant penalty
        score -= len(search_numbers) * 80
    elif not search_numbers and game_numbers:
        # Game has numbers but search doesn't - small penalty
        score -= len(game_numbers) * 20
    
    # Missing text penalty - penalize based on how much text is missing
    missing_text_penalty = calculate_missing_text_penalty(search_term, game_name)
    
    # Special bonus for common abbreviations
    abbreviation_mappings = {
        'gta': 'grand theft auto',
        'cod': 'call of duty',
        'ac': 'assassins creed',
        'bf': 'battlefield',
        'csgo': 'counter strike global offensive',
        'dota': 'defense of the ancients',
        'lol': 'league of legends',
        'wow': 'world of warcraft'
    }
    
    # Check if search is an abbreviation
    search_lower = search_term.lower()
    abbreviation_matched = False
    for abbr, full_name in abbreviation_mappings.items():
        if search_lower.startswith(abbr) and full_name in game_name.lower():
            score += 300  # Stronger bonus for recognized abbreviations
            # Also reduce missing text penalty for abbreviations
            missing_text_penalty *= 0.3  # Reduce penalty significantly for abbreviations
            abbreviation_matched = True
            break
    
    # Apply missing text penalty (after potential abbreviation reduction)
    score -= missing_text_penalty
    
    # Bonus for exact word matches
    search_words = set(search_term.split())
    game_words = set(game_name.split())
    common_words = search_words.intersection(game_words)
    
    # High bonus for exact word matches
    score += len(common_words) * 100
    
    # Bonus for search term being at the start of game name
    if game_name.startswith(search_term):
        score += 80
    
    # Bonus for search term being at the start of any word in game name
    for word in game_words:
        if word.startswith(search_term):
            score += 60
            break
    
    # Length-based scoring - prefer shorter games when search is short
    if len(search_term) <= 5:
        # For short searches, prefer shorter game names
        score += max(0, 50 - len(game_name))
    
    # Character overlap percentage
    search_chars = set(search_term)
    game_chars = set(game_name)
    char_overlap = len(search_chars.intersection(game_chars))
    total_chars = len(search_chars.union(game_chars))
    if total_chars > 0:
        score += (char_overlap / total_chars) * 30
    
    # Levenshtein distance (similarity) bonus
    distance = levenshtein_distance(search_term, game_name)
    max_len = max(len(search_term), len(game_name))
    if max_len > 0:
        similarity = (max_len - distance) / max_len
        score += similarity * 40
    
    # Bonus for game name containing search term as substring
    if search_term in game_name:
        score += 50
    
    # Bonus for search term containing game name (if game name is short)
    if len(game_name) <= len(search_term) and game_name in search_term:
        score += 30
    
    return score


def find_best_matches(search_term, game_list, threshold=50, max_results=10):
    """
    Find the best matching games from a list based on similarity scoring.
    
    Args:
        search_term (str): The search query
        game_list (list): List of game names or dict objects with 'name' key
        threshold (float): Minimum score to consider a match
        max_results (int): Maximum number of results to return
        
    Returns:
        list: List of matches sorted by score (highest first)
    """
    matches = []
    
    for game in game_list:
        # Handle both string lists and dict lists
        game_name = game if isinstance(game, str) else game.get('name', '')
        if not game_name:
            continue
            
        score = calculate_similarity_score(search_term.lower(), game_name.lower())
        
        if score >= threshold:
            match_info = {
                'name': game_name,
                'score': score
            }
            
            # If original was a dict, preserve other data
            if isinstance(game, dict):
                match_info.update({k: v for k, v in game.items() if k != 'name'})
            
            matches.append(match_info)
    
    # Sort by score (highest first) and limit results
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:max_results]


if __name__ == "__main__":
    # Test the similarity scoring
    print("🔍 Testing Game Similarity Scoring")
    print("=" * 50)
    
    test_cases = [
        ("call of duty 2", ["Call of Duty", "Call of Duty 2", "Call of Duty 3"]),
        ("gta 5", ["Grand Theft Auto", "Grand Theft Auto V", "GTA V"]),
        ("assassins creed", ["Assassin's Creed", "Assassin's Creed II", "Assassin's Creed Valhalla"])
        
    ]
    
    for search, games in test_cases:
        print(f"\nSearch: '{search}'")
        matches = find_best_matches(search, games)
        for match in matches:
            print(f"  {match['name']}: {match['score']:.1f}")
