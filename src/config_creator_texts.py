update_captions_window_title = {'eng': 'Create New Configuration',
                                'ger': 'Neue Konfiguration Anlegen',
                                'esp': 'Crear nueva configuración',
                                'rus': 'Создать новую конфигурацию'}

on_pushButton_set_project_dir_clicked_dialog_title = {'eng': 'Select Project Directory',
                                                      'ger': 'Projektverzeichnis auswählen',
                                                      'esp': 'Seleccionar directorio del proyecto',
                                                      'rus': 'Выберите каталог проекта'}

on_pushButton_set_db_path_clicked_dialog_title = {'eng': 'Select Database File',
                                                  'ger': 'Datenbankdatei auswählen',
                                                  'esp': 'Seleccionar archivo de base de datos',
                                                  'rus': 'Выберите файл базы данных'}
on_pushButton_set_db_path_clicked_dialog_text = {'eng': 'Database File (*.xlsx)',
                                                 'ger': 'Datenbankdatei (*.xlsx)',
                                                 'esp': 'Archivo de base de datos (*.xlsx)',
                                                 'rus': 'Файл базы данных (*.xlsx)'}

on_pushButton_set_rows_path_clicked_dialog_title = {'eng': 'Select Rows File',
                                                    'ger': 'Zeilen-Datei auswählen',
                                                    'esp': 'Seleccionar archivo de filas',
                                                    'rus': 'Выберите файл строк'}
on_pushButton_set_rows_path_clicked_dialog_text = {'eng': 'Rows File (*.xlsx)',
                                                   'ger': 'Zeilen-Datei (*.xlsx)',
                                                   'esp': 'Archivo de filas (*.xlsx)',
                                                   'rus': 'Файл строк (*.xlsx)'}

on_pushButton_set_placeholder_path_clicked_dialog_title = {'eng': 'Select Placeholder File',
                                                           'ger': 'Wähle Platzhalterdatei',
                                                           'esp': 'Seleccionar archivo de marcadores',
                                                           'rus': 'Выберите файл-заполнитель'}
on_pushButton_set_placeholder_path_clicked_dialog_text = {'eng': 'Placeholder File (*.xlsx)',
                                                          'ger': 'Platzhalterdatei (*.xlsx)',
                                                          'esp': 'Archivo de marcadores (*.xlsx)',
                                                          'rus': 'Файл-заполнитель (*.xlsx)'}

on_pushButton_set_template_path_clicked_dialog_title = {'eng': 'Select Template File',
                                                        'ger': 'Vorlagen-Datei auswählen',
                                                        'esp': 'Seleccionar archivo de plantilla',
                                                        'rus': 'Выберите файл шаблона'}
on_pushButton_set_template_path_clicked_dialog_text = {'eng': 'Template File (*.docx *.pdf)',
                                                       'ger': 'Vorlagen-Datei (*.docx *.pdf)',
                                                       'esp': 'Archivo de plantilla (*.docx *.pdf)',
                                                       'rus': 'Файл шаблона (*.docx *.pdf)'}

update_captions_prompts = dict()
update_captions_prompts['eng'] = {'label_Language': 'Language',
                                  'label_Paths': 'Paths',
                                  'lineEdit_project_dir': 'Project Directory',
                                  'pushButton_set_project_dir': 'Set Project Directory',
                                  'lineEdit_db_path': 'Database File Path',
                                  'pushButton_set_db_path': 'Set Database File Path',
                                  'lineEdit_rows_path': 'Rows File Path',
                                  'pushButton_set_rows_path': 'Set Rows File Path',
                                  'lineEdit_template_path': 'Template File Path',
                                  'pushButton_set_template_path': 'Set Template File Path',
                                  'label_Fields': 'Fields',
                                  'checkBox_use_sheet_names': 'Use Sheet names from Database File',
                                  'checkBox_write_to_single_field': 'Write Output to single Form Field',
                                  'plainTextEdit_field_names_payload': 'Name(s) of Form Field(s) in Template File',
                                  'label_Placeholders': 'Placeholders (optional)',
                                  'lineEdit_placeholders_path': 'Placeholders File Path (optional)',
                                  'pushButton_set_placeholders_path': 'Set Placeholders File Path (optional)',
                                  'plainTextEdit_genders': 'Genders',
                                  'label_Save': 'Save',
                                  'pushButton_Save': 'Save',
                                  'pushButton_Cancel': 'Cancel',
                                  'checkBox_review_editable': 'Make reviews editable'}
update_captions_prompts['ger'] = {'label_Language': 'Sprache',
                                  'label_Paths': 'Pfade',
                                  'lineEdit_project_dir': 'Projektordner',
                                  'pushButton_set_project_dir': 'Projektordner auswählen',
                                  'lineEdit_db_path': 'Datenbankdatei',
                                  'pushButton_set_db_path': 'Datenbankdatei auswählen',
                                  'lineEdit_rows_path': 'Zeilendatei',
                                  'pushButton_set_rows_path': 'Zeilendatei auswählen',
                                  'lineEdit_template_path': 'Vorlagendatei',
                                  'pushButton_set_template_path': 'Vorlagendatei auswählen',
                                  'label_Fields': 'Felder',
                                  'checkBox_use_sheet_names': 'Verwende Tabellenamen aus Datenbankdatei',
                                  'checkBox_write_to_single_field': 'Schreibe Ausgabe in einzelnes Feld',
                                  'plainTextEdit_field_names_payload': 'Name(n) des Feldes / der Felder in der Vorlagendatei',
                                  'label_Placeholders': 'Platzhalter (optional)',
                                  'lineEdit_placeholders_path': 'Platzhalterdatei (optional)',
                                  'pushButton_set_placeholders_path': 'Platzhalterdatei auswählen (optional)',
                                  'plainTextEdit_genders': 'Geschlechter',
                                  'label_Save': 'Speichern',
                                  'pushButton_Save': 'Speichern',
                                  'pushButton_Cancel': 'Abbrechen',
                                  'checkBox_review_editable': 'Reviews bearbeitbar machen'}
update_captions_prompts['esp'] = {'label_Language': 'Idioma',
                                  'label_Paths': 'Rutas',
                                  'lineEdit_project_dir': 'Directorio del proyecto',
                                  'pushButton_set_project_dir': 'Seleccionar directorio del proyecto',
                                  'lineEdit_db_path': 'Archivo de base de datos',
                                  'pushButton_set_db_path': 'Seleccionar archivo de base de datos',
                                  'lineEdit_rows_path': 'Archivo de filas',
                                  'pushButton_set_rows_path': 'Seleccionar archivo de filas',
                                  'lineEdit_template_path': 'Archivo de plantilla',
                                  'pushButton_set_template_path': 'Seleccionar archivo de plantilla',
                                  'label_Fields': 'Campos',
                                  'checkBox_use_sheet_names': 'Usar nombres de hoja de archivo de base de datos',
                                  'checkBox_write_to_single_field': 'Escribir salida en un solo campo',
                                  'plainTextEdit_field_names_payload': 'Nombre(s) del campo(s) en el archivo de plantilla',
                                  'label_Placeholders': 'Marcadores (opcional)',
                                  'lineEdit_placeholders_path': 'Archivo de marcadores (opcional)',
                                  'pushButton_set_placeholders_path': 'Seleccionar archivo de marcadores (opcional)',
                                  'plainTextEdit_genders': 'Géneros',
                                  'label_Save': 'Guardar',
                                  'pushButton_Save': 'Guardar',
                                  'pushButton_Cancel': 'Cancelar',
                                  'checkBox_review_editable': 'Hacer revisiones editables'}
update_captions_prompts['rus'] = {'label_Language': 'Язык',
                                  'label_Paths': 'Пути',
                                  'lineEdit_project_dir': 'Каталог проекта',
                                  'pushButton_set_project_dir': 'Выберите каталог проекта',
                                  'lineEdit_db_path': 'Файл базы данных',
                                  'pushButton_set_db_path': 'Выберите файл базы данных',
                                  'lineEdit_rows_path': 'Файл строк',
                                  'pushButton_set_rows_path': 'Выберите файл строк',
                                  'lineEdit_template_path': 'Файл шаблона',
                                  'pushButton_set_template_path': 'Выберите файл шаблона',
                                  'label_Fields': 'Поля',
                                  'checkBox_use_sheet_names': 'Использовать имена листов из файла базы данных',
                                  'checkBox_write_to_single_field': 'Записать вывод в одно поле',
                                  'plainTextEdit_field_names_payload': 'Имя(имена) поля(полей) в файле шаблона',
                                  'label_Placeholders': 'Заполнители (необязательно)',
                                  'lineEdit_placeholders_path': 'Файл-заполнитель (необязательно)',
                                  'pushButton_set_placeholders_path': 'Выберите файл-заполнитель (необязательно)',
                                  'plainTextEdit_genders': 'Пол',
                                  'label_Save': 'Сохранить',
                                  'pushButton_Save': 'Сохранить',
                                  'pushButton_Cancel': 'Отмена',
                                  'checkBox_review_editable': 'Сделать редактируемыми обзоры'}

on_pushButton_set_project_dir_clicked_msgbox_title = {'eng': 'Error',
                                                      'ger': 'Fehler',
                                                      'esp': 'Error',
                                                      'rus': 'Ошибка'}
on_pushButton_set_project_dir_clicked_msgbox_text = {
    'eng': 'Project directory not empty. Please select an empty folder as project directory.',
    'ger': 'Projektordner nicht leer. Bitte  einen leeren Ordner als Projektordner wählen.',
    'esp': 'Directorio del proyecto no vacío. Seleccione una carpeta vacía como directorio del proyecto.',
    'rus': 'Каталог проекта не пуст. Пожалуйста, выберите пустую папку в качестве каталога проекта.'}

are_all_paths_given_msgbox_title = {'eng': 'Error',
                                    'ger': 'Fehler',
                                    'esp': 'Error',
                                    'rus': 'Ошибка'}
are_all_paths_given_msgbox_text = {'eng': 'Please fill out all paths.',
                                   'ger': 'Bitte alle Pfade ausfüllen.',
                                   'esp': 'Por favor, rellene todos los campos.',
                                   'rus': 'Пожалуйста, заполните все поля.'}

is_fields_logic_consistent_field_names_inconsistent_msgbox_title = {'eng': 'Error',
                                                                    'ger': 'Fehler',
                                                                    'esp': 'Error',
                                                                    'rus': 'Ошибка'}
is_fields_logic_consistent_field_names_inconsistent_msgbox_text = {
    'eng': 'Field names in template do not match your configuration. Please revise.',
    'ger': 'Feldnamen in Vorlage stimmen nicht mit Ihrer Konfiguration überein. Bitte überprüfen.',
    'esp': 'Los nombres de campo en la plantilla no coinciden con su configuración. Por favor revise.',
    'rus': 'Имена полей в шаблоне не соответствуют вашей конфигурации. Пожалуйста, пересмотрите.'}
is_fields_logic_consistent_num_given_fields_inconsistent_msgbox_title = {'eng': 'Error',
                                                                         'ger': 'Fehler',
                                                                         'esp': 'Error',
                                                                         'rus': 'Ошибка'}
is_fields_logic_consistent_num_given_fields_inconsistent_msgbox_text = {
    'eng': 'Number of given fields in template does not match your configuration. Please revise.',
    'ger': 'Anzahl der Felder in Vorlage stimmt nicht mit Ihrer Konfiguration überein. Bitte überprüfen.',
    'esp': 'El número de campos en la plantilla no coincide con su configuración. Por favor revise.',
    'rus': 'Количество полей в шаблоне не соответствует вашей конфигурации. Пожалуйста, пересмотрите.'}

is_template_consistent_error_opening_db_msgbox_title = {'eng': 'Error',
                                                        'ger': 'Fehler',
                                                        'esp': 'Error',
                                                        'rus': 'Ошибка'}
is_template_consistent_error_opening_db_msgbox_text = {'eng': 'Error opening database file:\n_exception',
                                                       'ger': 'Fehler beim Öffnen der Datenbankdatei:\n_exception',
                                                       'esp': 'Error al abrir el archivo de base de datos:\n_exception',
                                                       'rus': 'Ошибка при открытии файла базы данных:\n_exception'}
is_template_consistent_field_names_inconsistent_msgbox_title = {'eng': 'Error',
                                                                'ger': 'Fehler',
                                                                'esp': 'Error',
                                                                'rus': 'Ошибка'}
is_template_consistent_field_names_inconsistent_msgbox_text = {
    'eng': 'Field names in template do not match your configuration. Please revise.',
    'ger': 'Feldnamen in Vorlage stimmen nicht mit Ihrer Konfiguration überein. Bitte überprüfen.',
    'esp': 'Los nombres de campo en la plantilla no coinciden con su configuración. Por favor revise.',
    'rus': 'Имена полей в шаблоне не соответствуют вашей конфигурации. Пожалуйста, пересмотрите.'}

is_database_consistent_bad_shape_msgbox_title = {'eng': 'Error',
                                                 'ger': 'Fehler',
                                                 'esp': 'Error',
                                                 'rus': 'Ошибка'}
is_database_consistent_bad_shape_msgbox_text = {'eng': 'Database file has wrong shape. Please revise.',
                                                'ger': 'Datenbankdatei hat falsche Form. Bitte überprüfen.',
                                                'esp': 'El archivo de base de datos tiene una forma incorrecta. Por favor revise.n',
                                                'rus': 'Файл базы данных имеет неправильную форму. Пожалуйста, пересмотрите.'}

is_template_consistent_error_reading_rows_msgbox_title = {'eng': 'Error',
                                                          'ger': 'Fehler',
                                                          'esp': 'Error',
                                                          'rus': 'Ошибка'}
is_template_consistent_error_reading_rows_msgbox_text = {'eng': 'Error reading rows file:\n_exception',
                                                         'ger': 'Fehler beim Lesen der Zeilendatei:\n_exception',
                                                         'esp': 'Error al leer el archivo de filas:\n_exception',
                                                         'rus': 'Ошибка чтения файла строк:\n_exception'}

on_pushButton_Save_clicked_success_msgbox_title = {'eng': 'Success',
                                                   'ger': 'Erfolg',
                                                   'esp': 'Éxito',
                                                   'rus': 'Успех'}
on_pushButton_Save_clicked_success_msgbox_text = {'eng': 'Configuration successfully created.',
                                                  'ger': 'Konfiguration erfolgreich angelegt.',
                                                  'esp': 'Configuración creada con éxito.',
                                                  'rus': 'Конфигурация успешно создана.'}
on_pushButton_Save_clicked_failure_msgbox_title = {'eng': 'Failure',
                                                   'ger': 'Fehlgeschlagen',
                                                   'esp': 'Fracaso',
                                                   'rus': 'Неудача'}
on_pushButton_Save_clicked_failure_msgbox_text = {'eng': 'Error creating configuration.',
                                                  'ger': 'Fehler beim Anlegen der Konfiguration.',
                                                  'esp': 'Error al crear la configuración.',
                                                  'rus': 'Ошибка создания конфигурации.'}
