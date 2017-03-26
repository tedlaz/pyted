class Menu:
    def __init__(self, name, items=None):
        self.name = name
        self.items = items or []

    def add_item(self, item):
        self.items.append(item)
        if item.parent != self:
            item.parent = self

    def remove_item(self, item):
        self.items.remove(item)
        if item.parent == self:
            item.parent = None

    def draw(self):
        while True:
            print('\n' + self.name + ' Menu')
            num = 1
            for item in self.items:
                print('  %s. %s' % (num, item.name))
                num += 1
            try:
                choice = int ( input('Enter your choice (q for quit) : ') )
            except ValueError:
                choice = -1
            if (choice <= len(self.items)) and choice > 0:
                print(self.items[choice-1].function)
            else:
                break

class Item:
    def __init__(self, name, function, parent=None):
        self.name = name
        self.function = function
        self.parent = parent
        if parent:
            parent.add_item(self)

    def draw(self):
        # might be more complex later, better use a method.
        print("    " + self.name)


if __name__ == '__main__':
    mmm = Menu('main')
    mmm.add_item(Item('Create database', 'dbcreate'))
    mmm.add_item(Item('Show data', 'fake2'))
    mmm.draw()
