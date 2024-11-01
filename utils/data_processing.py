import uuid
from typing import Dict, List, Set
import pandas as pd

def generate_uuid() -> str:
    """Generate a unique UUID string"""
    return str(uuid.uuid4())

def create_uuid_mapping(values) -> Dict[str, str]:
    """
    Create a mapping of values to UUIDs, handling duplicates and NA values.
    
    Args:
        values: An iterable of values to map to UUIDs
        
    Returns:
        Dict mapping unique values to UUIDs
        
    Example:
        >>> values = ['A', 'B', 'A', 'C', None]
        >>> mapping = create_uuid_mapping(values)
        >>> len(mapping) == 3  # Only unique values are mapped
        True
        >>> mapping['A'] == mapping['A']  # Same value maps to same UUID
        True
    """
    # Convert to set to get unique values, filtering out NA/None
    unique_values: Set = {value for value in values if pd.notna(value)}
    
    # Create mapping with consistent UUIDs for duplicate values
    return {value: generate_uuid() for value in unique_values}

def verify_mapping_integrity(mapping: Dict[str, str], values) -> bool:
    """
    Verify the integrity of a UUID mapping.
    
    Args:
        mapping: Dict mapping values to UUIDs
        values: Original values used to create the mapping
        
    Returns:
        bool: True if mapping is valid, False otherwise
        
    Checks:
    1. All non-NA values have a mapping
    2. Each unique value maps to a unique UUID
    3. Same value always maps to same UUID
    """
    # Get unique non-NA values
    unique_values = {value for value in values if pd.notna(value)}
    
    # Check all values have mappings
    mapped_values = set(mapping.keys())
    if unique_values != mapped_values:
        return False
    
    # Check UUID uniqueness (no two different values map to same UUID)
    if len(set(mapping.values())) != len(mapping):
        return False
    
    # Check consistency (same value always maps to same UUID)
    for value in values:
        if pd.notna(value) and value in mapping:
            uuid_val = mapping[value]
            # Verify this is the only value that maps to this UUID
            if sum(1 for v, u in mapping.items() if u == uuid_val) > 1:
                return False
    
    return True

def get_mapping_stats(mapping: Dict[str, str], values) -> Dict[str, int]:
    """
    Get statistics about a UUID mapping.
    
    Args:
        mapping: Dict mapping values to UUIDs
        values: Original values used to create the mapping
        
    Returns:
        Dict with statistics:
        - total_values: Total number of input values
        - unique_values: Number of unique values
        - mapped_values: Number of values with UUID mappings
        - na_values: Number of NA values
    """
    total_values = len(values)
    na_values = sum(1 for v in values if pd.isna(v))
    unique_values = len({v for v in values if pd.notna(v)})
    mapped_values = len(mapping)
    
    return {
        "total_values": total_values,
        "unique_values": unique_values,
        "mapped_values": mapped_values,
        "na_values": na_values
    }
