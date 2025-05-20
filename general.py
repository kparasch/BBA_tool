
def select_all(my_list):
    for i in range(my_list.count()):
        my_list.item(i).setSelected(True)

def remove_selected(selectedBPMs):
    row = selectedBPMs.count()
    for item in selectedBPMs.selectedItems():
        selectedBPMs.takeItem(selectedBPMs.row(item))
        row -= 1

def transfer_selection(source_list, target_list):
    items_before = [target_list.item(row).text() for row in range(target_list.count())]
    for item in source_list.selectedItems():
        itemtext = item.text()
        if itemtext in items_before:
            continue
        target_list.addItem(itemtext)