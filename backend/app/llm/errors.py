class LLMProviderError(Exception):
    pass


class MissingProviderKeyError(LLMProviderError):
    pass


class UnsupportedProviderError(LLMProviderError):
    pass


class ProviderCallError(LLMProviderError):
    pass
