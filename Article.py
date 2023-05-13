class Article:
    __category__ = None
    __author_name__ = None
    __creation_date__ = None
    __last_editor__ = None
    __last_edit_date__ = None
    __title__ = None
    __text__ = None

    def __init__(
            self,
            category,
            author,
            creation_date,
            last_editor,
            last_edit_date,
            title,
            text

    ):
        self.__category__ = category
        self.__author_name__ = author
        self.__creation_date__ = creation_date
        self.__last_editor__ = last_editor
        self.__last_edit_date__ = last_edit_date
        self.__title__ = title
        self.__text__ = text

    def get_category(self):
        return self.__category__

    def get_author(self):
        return self.__author_name__

    def get_creation_date(self):
        return self.__creation_date__

    def get_last_editor(self):
        return self.__last_editor__

    def get_last_edit_date(self):
        return self.__last_edit_date__

    def get_title(self):
        return self.__title__

    def get_text(self):
        return self.__text__
