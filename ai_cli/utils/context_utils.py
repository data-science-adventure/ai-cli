from rich.console import Console

class ContextUtils:
    CONTEXT_CLASS_INSTANCE = None
    CONSOLE_CLASS_INSTANCE = None

    @staticmethod
    def get_console() -> Console:
        if ContextUtils.CONSOLE_CLASS_INSTANCE is None:
            ContextUtils.CONSOLE_CLASS_INSTANCE = Console()
        return ContextUtils.CONSOLE_CLASS_INSTANCE
    
    
