ALL_VARIATION_SELECTOR_RANGES = ["\\U0000fe00-\\U0000fe0f", "\\U000e0100-\\U000e01ef"]
EMOJI_VARIATION_SELECTOR_RANGES = ["\\U0000fe0e-\\U0000fe0f"]
EMOJI_VARIATION_SELECTOR_RANGES_STR = "".join(EMOJI_VARIATION_SELECTOR_RANGES)
"""All variation selectors are in Nonspacing Mark (Mn), but it is more apt to
mark these two as punctuation, since they are used exclusively for rendering
emoji. But it's best to use the Emoji filter.
"""
