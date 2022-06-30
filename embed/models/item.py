from embed.models.dao import DAO


class Item(DAO):
    def __init__(self, dispatch, name, attrs):
        super().__init__(dispatch)
        self.name: str = name
        self.__attrs: dict = attrs

    def get(self, key):
        """Get an attribute"""
        return self.__attrs.get(key)

    async def set(self, key, val):
        """Set an attribute"""
        self.__attrs[key] = val
        # Update the db
