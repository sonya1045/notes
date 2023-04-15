from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout,\
    QVBoxLayout, QLineEdit, QTextEdit, QInputDialog
import json
app = QApplication([])# створення додатку
'''Замітки в json'''
notes = {
    "Ласкаво просимо!": {
        "текст": "Це найкращий додаток для заміток у світі!",
        "теги": ["добро", "інструкція"]
    }
  }
with open("notes_data.json", "w") as file:# записуємо замітки в json
    json.dump(notes, file)
    
window = QWidget()# створення вікна додатку
window.resize(1400, 800)# розмір вікна
window.setWindowTitle("Notes")# заголовок вікна
'''ІНТЕРФЕЙС ПРОГРАМИ'''
text_field = QTextEdit()# велике поля для вводу

list_notes = QListWidget()# список заміток
list_notes_label = QLabel("Список заміток")
# кнопки для дій з замітками
btn_create_note = QPushButton("Створити замітку")
btn_del_note = QPushButton("Видалити замітку")
btn_save_note = QPushButton("Зберегти замітку")

list_tags = QListWidget()# список тегів
list_tags_label = QLabel("Список тегів")
# кнопки для дій з тегами
btn_add_tag = QPushButton("Додати до замітки")
btn_del_tag = QPushButton("Відкріпити від замітки")
btn_search_note = QPushButton("Шукати замітки по тегу")

input_tag = QLineEdit()# поле для вводу тегу
input_tag.setPlaceholderText("Введіть тег.......")
# Створюємо лінії та кладеом на них віджети
col1 = QVBoxLayout()
col1.addWidget(text_field)

col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)

row1 = QHBoxLayout()
row1.addWidget(btn_create_note)
row1.addWidget(btn_del_note)

row2 = QHBoxLayout()
row2.addWidget(btn_save_note)

col2.addLayout(row1)
col2.addLayout(row2)
col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(input_tag)

row3 = QHBoxLayout()
row3.addWidget(btn_add_tag)
row3.addWidget(btn_del_tag)

row4 = QHBoxLayout()
row4.addWidget(btn_search_note)

col2.addLayout(row3)
col2.addLayout(row4)

layout_notes = QHBoxLayout()
layout_notes.addLayout(col1, stretch=5)
layout_notes.addLayout(col2, stretch=4)

window.setLayout(layout_notes)
'''ФУНКЦІОНАЛ ПРОГРАМИ'''
'''Робота з текстом замітки'''
def show_note():# функція показу замітки
    key = list_notes.selectedItems()[0].text()
    text_field.clear()
    text_field.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

def add_note():# функція додати нову замітку
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки:")#вікно для введення назви замітки
    if ok and note_name != "":#Якщо поле не пусте
        notes[note_name] = {"текст": "", "теги": []}#Створюємо пусту замітку з іменем, яке ми ввели
        list_notes.addItem(note_name)#відображаємо нову замітку в списку заміток
        list_tags.addItems(notes[note_name]["теги"])#відображаємо список тегів нової замітки

def del_note():# функція видалити замітку
    if list_notes.selectedItems():#перевіряємо чи вибрана замітка
        key = list_notes.selectedItems()[0].text()#зберігаємо назву замітки
        del notes[key]#видаляємо всю замітку
        text_field.clear()#чистимо поле для тексту
        list_notes.clear()#чистимо список з замітками
        list_tags.clear()#чистимо список з тегами
        list_notes.addItems(notes)#відображаємо оновлений список заміток
        with open('notes_data.json', 'w') as file:#записуємо в  json файл
            json.dump(notes, file, sort_keys=True)

def save_note():#зберігає замітки
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = text_field.toPlainText()# зберігаємо текст в замітку
        with open('notes_data.json', 'w') as file:#записуємо в  json файл
            json.dump(notes, file, sort_keys=True)

def add_tag():#додаємо тег до замітки
    if list_notes.selectedItems():#перевіряємо натискання
        key = list_notes.selectedItems()[0].text()# зберігаємо назву замітки
        if input_tag.text():#якщо вибране текстове поле
            tag = input_tag.text()
            if not tag in notes[key]['теги']:#якщо поле не пусте
                notes[key]['теги'].append(tag)# зберігаємо нотатки 
                list_tags.addItem(tag)#додаємо нотатку
                input_tag.clear()#чистимо поле
                with open('notes_data.json', 'w') as file:#записуємо в файл
                    json.dump(notes, file, sort_keys=True)

def del_tag():# функція видалення нотаток
    if list_notes.selectedItems():# якщо нотатка виділена
        key = list_notes.selectedItems()[0].text()#зберігаємо назву замітки
        tag = list_tags.selectedItems()[0].text()# зберігаємо теги
        notes[key]['теги'].remove(tag)
        list_tags.clear()# чистимо поле з тегами
        list_tags.addItems(notes[key]['теги'])# 
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
        
def search_note():
    if input_tag.text() and btn_search_note.text() == "Шукати замітки по тегу":
        tag = input_tag.text()
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        btn_search_note.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif input_tag.text() and btn_search_note.text() == "Скинути пошук":
        input_tag.clear()
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        btn_search_note.setText("Шукати замітки по тегу")
    
    

#ПЕРЕВІРКА НАТИСКАННЯ НА КНОПКИ
btn_del_note.clicked.connect(del_note)
btn_save_note.clicked.connect(save_note)
btn_create_note.clicked.connect(add_note)
btn_add_tag.clicked.connect(add_tag)
btn_del_tag.clicked.connect(del_tag)
btn_search_note.clicked.connect(search_note)

list_notes.itemClicked.connect(show_note)

window.show()

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)


app.exec_()