class Article:
    __categories__ = None
    __creator__ = None
    __creation_date__ = None
    __title__ = None
    __text__ = None

    def __init__(
            self,
            categories,
            creator,
            creation_date,
            title,
            text

    ):
        self.__categories__ = categories
        self.__creator__ = creator
        self.__creation_date__ = creation_date
        self.__title__ = title
        self.__text__ = text

    def get_categories(self):
        return self.__categories__

    def get_creator(self):
        return self.__creator__

    def get_creation_date(self):
        return self.__creation_date__

    def get_title(self):
        return self.__title__

    def get_text(self):
        return self.__text__
