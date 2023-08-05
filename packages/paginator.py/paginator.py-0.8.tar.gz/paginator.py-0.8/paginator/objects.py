from discord import Embed

class NavigationType:
    """
    For those who don't want to remember two numbers, use this in the send method type argument
    """
    Reactions = 1  # Change page with reactions
    Buttons = 2  # Change page with buttons

class Page:
    """
    Used in the pages list
    """
    def __init__(self, content: str = None, embed: Embed = None):
        self.content = content
        self.embed = embed

class PageEmojis:
    """
    This can be changed by setting the Paginator.page_emojis to your own class with the PageEmojis inheritance
    """
    def __init__(self):
        self.forward = "➡️"
        self.back = "⬅️"
