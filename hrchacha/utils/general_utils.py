import random

from hrchacha.constants import HR_CHACHA_THINKING_LINES


def get_random_chacha_thinking_line() -> str:
    return random.choice(HR_CHACHA_THINKING_LINES)
