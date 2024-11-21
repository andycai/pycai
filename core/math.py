import math
from typing import List, Union, Tuple
from decimal import Decimal, ROUND_HALF_UP

Number = Union[int, float, Decimal]

def round_up(value: Number, decimals: int = 0) -> Number:
    """
    Round up to specified decimal places.
    
    Args:
        value: Number to round
        decimals: Number of decimal places
    """
    multiplier = 10 ** decimals
    return math.ceil(float(value) * multiplier) / multiplier

def round_down(value: Number, decimals: int = 0) -> Number:
    """
    Round down to specified decimal places.
    
    Args:
        value: Number to round
        decimals: Number of decimal places
    """
    multiplier = 10 ** decimals
    return math.floor(float(value) * multiplier) / multiplier

def round_decimal(value: Number, decimals: int = 0) -> Decimal:
    """
    Round decimal number (banking rounding).
    
    Args:
        value: Number to round
        decimals: Number of decimal places
    """
    return Decimal(str(value)).quantize(
        Decimal('0.1') ** decimals,
        rounding=ROUND_HALF_UP
    )

def clamp(value: Number, min_value: Number, max_value: Number) -> Number:
    """
    Clamp value between min and max.
    
    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value
    """
    return max(min_value, min(max_value, value))

def percentage(part: Number, total: Number, decimals: int = 2) -> float:
    """
    Calculate percentage.
    
    Args:
        part: Part value
        total: Total value
        decimals: Number of decimal places
    """
    if total == 0:
        return 0.0
    return round((float(part) / float(total)) * 100, decimals)

def average(numbers: List[Number]) -> float:
    """Calculate average of numbers."""
    if not numbers:
        return 0.0
    return sum(float(x) for x in numbers) / len(numbers)

def median(numbers: List[Number]) -> float:
    """Calculate median of numbers."""
    if not numbers:
        return 0.0
    sorted_numbers = sorted(float(x) for x in numbers)
    length = len(sorted_numbers)
    mid = length // 2
    if length % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    return sorted_numbers[mid]

def mode(numbers: List[Number]) -> List[Number]:
    """
    Calculate mode (most common values) of numbers.
    Returns list in case of multiple modes.
    """
    if not numbers:
        return []
    counts = {}
    for num in numbers:
        counts[num] = counts.get(num, 0) + 1
    max_count = max(counts.values())
    return [num for num, count in counts.items() if count == max_count]

def variance(numbers: List[Number]) -> float:
    """Calculate variance of numbers."""
    if not numbers:
        return 0.0
    avg = average(numbers)
    return sum((float(x) - avg) ** 2 for x in numbers) / len(numbers)

def std_dev(numbers: List[Number]) -> float:
    """Calculate standard deviation of numbers."""
    return math.sqrt(variance(numbers))

def is_prime(n: int) -> bool:
    """Check if number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def factors(n: int) -> List[int]:
    """Get factors of number."""
    result = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            result.append(i)
            if i != n // i:
                result.append(n // i)
    return sorted(result)

def gcd(a: int, b: int) -> int:
    """Calculate Greatest Common Divisor."""
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    """Calculate Least Common Multiple."""
    return abs(a * b) // gcd(a, b)

def fibonacci(n: int) -> List[int]:
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def is_perfect_square(n: int) -> bool:
    """Check if number is perfect square."""
    root = int(math.sqrt(n))
    return root * root == n

def distance_2d(x1: Number, y1: Number, x2: Number, y2: Number) -> float:
    """Calculate Euclidean distance between two 2D points."""
    return math.sqrt((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2)

def angle_between_points(x1: Number, y1: Number, x2: Number, y2: Number) -> float:
    """Calculate angle between two points in degrees."""
    return math.degrees(math.atan2(float(y2) - float(y1), float(x2) - float(x1)))

"""
from core.math import (
    round_up, round_down, percentage, average,
    median, mode, is_prime, fibonacci
)

# Rounding
value = round_up(3.14159, decimals=2)    # 3.15
value = round_down(3.14159, decimals=2)  # 3.14

# Statistics
nums = [1, 2, 3, 4, 5]
avg = average(nums)       # 3.0
med = median(nums)        # 3.0
modes = mode([1,2,2,3])  # [2]
std = std_dev(nums)      # Standard deviation

# Percentages
pct = percentage(75, 100)  # 75.0

# Number Theory
prime = is_prime(17)      # True
facts = factors(12)       # [1, 2, 3, 4, 6, 12]
fib = fibonacci(10)       # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Geometry
dist = distance_2d(0, 0, 3, 4)  # 5.0
angle = angle_between_points(0, 0, 1, 1)  # 45.0
"""