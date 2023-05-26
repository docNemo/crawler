class Article:
    __categories = None
    __creator = None
    __creation_date = None
    __title = None
    __text = None

    def __init__(
            self,
            categories,
            creator,
            creation_date,
            title,
            text

    ):
        self.__categories = categories
        self.__creator = creator
        self.__creation_date = creation_date
        self.__title = title
        self.__text = text

    def get_categories(self):
        return self.__categories

    def get_creator(self):
        return self.__creator

    def get_creation_date(self):
        return self.__creation_date

    def get_title(self):
        return self.__title

    def get_text(self):
        return self.__text
