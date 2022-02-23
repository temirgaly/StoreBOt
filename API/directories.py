from Database import Database
CRUD = Database.GetInstance()


def init():
    global categories
    global brands
    global variants

    categories = CRUD.GetValuesList('CATEGORY')
    brands = CRUD.GetValuesList('BRANDS')
    variants = CRUD.GetValuesList('VARIANTS')


def GetBrands():
    brands = CRUD.GetValuesList('BRANDS')


def GetCategories():
    categories = CRUD.GetValuesList('CATEGORY')


if __name__ == '__main__':
    init()
    print(GetBrands())
