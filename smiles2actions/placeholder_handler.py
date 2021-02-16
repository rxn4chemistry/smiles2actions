class InvalidPlaceholder(ValueError):

    def __init__(self, name: str):
        super().__init__(f'"{name}" is not a valid placeholder')


class PlaceholderHandler:
    """
    Handles the placeholder conversion to and from integers.

    For instance:
    * 1 -> $1$
    * 4 -> #4#
    * -1 -> ##-1##
    * etc.
    """

    def __init__(self, default_affix: str):
        """
        Args:
            default_affix: characters to put before and after a given index.
                Must consist of exactly one character type.
        """

        if len(set(default_affix)) != 1:
            raise ValueError(
                f'Invalid affix: "{default_affix}". It contains'
                f'more than one character type.'
            )

        self.default_prefix = default_affix
        self.default_postfix = default_affix

    def to_placeholder(self, index: int) -> str:
        """Converts a given index to a placeholder."""
        return self.default_prefix + str(index) + self.default_postfix

    @classmethod
    def for_compounds(cls) -> 'PlaceholderHandler':
        return cls(default_affix='$')

    @classmethod
    def for_durations(cls) -> 'PlaceholderHandler':
        return cls(default_affix='@')

    @classmethod
    def for_temperatures(cls) -> 'PlaceholderHandler':
        return cls(default_affix='#')
