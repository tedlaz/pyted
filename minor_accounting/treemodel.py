from PyQt5 import QtCore as qc
from treeitem import TreeItem


def find_start(txt, start_type='space'):
    position = 0
    while position < len(txt):
        if start_type == 'space':
            if txt[position] != ' ':
                break
        elif start_type == 'repeat':
            if txt[position] != '':
                break
        position += 1
    return position


class TreeModel(qc.QAbstractItemModel):
    def __init__(self, col_titles, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem(col_titles)
        self.setupModelData(data.split('\n'), self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != qc.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return qc.Qt.NoItemFlags
        return qc.Qt.ItemIsEnabled | qc.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == qc.Qt.Horizontal and role == qc.Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return qc.QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return qc.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return qc.QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return qc.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def setupModelData(self, lines, parent):
        parents = [parent]
        indentations = [0]
        number = 0
        while number < len(lines):
            position = find_start(lines[number])
            lineData = lines[number][position:].strip()
            if lineData:
                # Read the column data from the rest of the line.
                columnData = [s for s in lineData.split('\t') if s]
                if position > indentations[-1]:
                    # The last child of the current parent is now the new
                    # parent unless the current parent has no children.
                    if parents[-1].childCount() > 0:
                        parents.append(
                            parents[-1].child(parents[-1].childCount() - 1))
                        indentations.append(position)
                else:
                    while position < indentations[-1] and len(parents) > 0:
                        parents.pop()
                        indentations.pop()
                # Append a new item to the current parent's list of children.
                parents[-1].appendChild(TreeItem(columnData, parents[-1]))
            number += 1
        for line in lines:
            ldata = [i.strip() for i in line.split('\t')]
            print(len(ldata), ldata)


if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets as qw
    print('find_start', find_start('   malakia'))
    app = qw.QApplication(sys.argv)
    with open('minor_accounting/treedata.txt', 'r') as f:
        model = TreeModel(('Κωδικός', 'Περιγραφή'), f.read())
    view = qw.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.show()
    sys.exit(app.exec_())
