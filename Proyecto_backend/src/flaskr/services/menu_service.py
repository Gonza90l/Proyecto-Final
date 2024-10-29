from flaskr.models.menu import Menu

class MenuService:

    def __init__(self, mysql):
        self._mysql = mysql

    def get_menus(self):
        menu = Menu(self._mysql)
        menus = menu.find_all()
        return menus