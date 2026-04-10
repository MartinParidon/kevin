messageBoxYesText = {'eng': 'Yes',
                     'ger': 'Ja',
                     'esp': 'Si',
                     'rus': 'Да'}
messageBoxNoText = {'eng': 'No',
                    'ger': 'Nein',
                    'esp': 'No',
                    'rus': 'Нет'}

messageBoxOkText = {'eng': 'Ok',
                    'ger': 'Ok',
                    'esp': 'Aceptar',
                    'rus': 'Ок'}
messageBoxCancelText = {'eng': 'Cancel',
                        'ger': 'Abbrechen',
                        'esp': 'Cancelar',
                        'rus': 'Отмена'}

load_session_msgbox1_title = {'eng': 'Error',
                              'ger': 'Fehler',
                              'esp': 'Error',
                              'rus': 'Ошибка'}
load_session_msgbox1_text = {'eng': 'Config file not found. Aborting.',
                             'ger': 'Konfigurationsdatei nicht gefunden. Abbruch.',
                             'esp': 'Archivo de configuración no encontrado. Abortando.',
                             'rus': 'Файл конфигурации не найден. Прерывание.'}
load_session_msgbox3_title = {'eng': 'Error loading config file',
                              'ger': "Fehler beim Laden der Konfigurationsdatei",
                              'esp': 'Error al cargar el archivo de configuración',
                              'rus': 'Ошибка загрузки файла конфигурации'}
load_session_msgbox3_text = {'eng': 'Config file "_cfg_path" could not be loaded.',
                             'ger': 'Konfig-Datei "_cfg_path" konnte nicht geladen werden.',
                             'esp': 'No se pudo cargar el archivo de configuración "_cfg_path".',
                             'rus': 'Файл конфигурации "_cfg_path" не может быть загружен.'}
load_session_msgbox4_title = {'eng': 'Error',
                              'ger': "Fehler",
                              'esp': 'Error',
                              'rus': 'Ошибка'}
load_session_msgbox4_text = {'eng': 'Error reading session file. Is it corrupted?\n\nException: _exception',
                             'ger': 'Fehler beim Lesen der session Datei. Ist sie beschädigt?\n\nException: _exception',
                             'esp': 'Error al leer el archivo de sesión. ¿Está corrupto?\n\nException: _exception',
                             'rus': 'Ошибка чтения файла сеанса. Он поврежден?\n\nИсключение: _exception'}
load_session_msgbox5_title = {'eng': 'Version Error',
                              'ger': "Versionsfehler",
                              'esp': 'Error de versión',
                              'rus': 'Ошибка версии'}
load_session_msgbox5_text = {
    'eng': 'Session _session_filepath was created with version _version_session. Please use at least version _version_minimum.',
    'ger': 'Session _session_filepath wurde mit Version _version_session erstellt. Bitte mindestens Version _version_minimum verwenden.',
    'esp': 'La sesión _session_filepath se creó con la versión _version_session. Utilice al menos la versión _version_minimum.',
    'rus': 'Сеанс _session_filepath был создан с версией _version_session. Пожалуйста, используйте версию _version_minimum или выше.'}

send_mail_subject = {'eng': "Report%20Issue%20Kevin%20v_version_string",
                     'ger': 'Fehler%20melden%20Kevin%20v_version_string',
                     'esp': 'Reportar%20problema%20Kevin%20v_version_string',
                     'rus': 'Сообщить%20об%20ошибке%20Kevin%20v_version_string'}
send_mail_msgbox_title_exception_title = {'eng': 'Error',
                                          'ger': 'Fehler',
                                          'esp': 'Error',
                                          'rus': 'Ошибка'}
send_mail_msgbox_title_exception_text = {'eng': 'Error sending mail. Exception: _exception',
                                         'ger': 'Fehler beim Senden der E-Mail. Exception: _exception',
                                         'esp': 'Error al enviar el correo. Exception: _exception',
                                         'rus': 'Ошибка отправки почты. Исключение: _exception'}

load_cfg_msgbox_title = {'eng': 'Error',
                         'ger': 'Fehler',
                         'esp': 'Error',
                         'rus': 'Ошибка'}
load_cfg_msgbox_text = {'eng': 'Error reading config file.\n\n_exception',
                        'ger': 'Fehler beim Lesen der Konfigurationsdatei.\n\n_exception',
                        'esp': 'Error al leer el archivo de configuración.\n\n_exception',
                        'rus': 'Ошибка чтения файла конфигурации.\n\n_exception'}

is_list_in_template_form_names_msgbox_title = {'eng': 'Error',
                                               'ger': 'Fehler',
                                               'esp': 'Error',
                                               'rus': 'Ошибка'}
is_list_in_template_form_names_msgbox_text = {'eng': 'Error opening template file:\n\n_exception',
                                              'ger': 'Fehler beim Öffnen der Vorlagendatei:\n\n_exception',
                                              'esp': 'Error al abrir el archivo de plantilla:\n\n_exception',
                                              'rus': 'Ошибка при открытии файла шаблона:\n\n_exception'}

read_rows_data_msgbox_title1 = {'eng': 'Error',
                                'ger': 'Fehler',
                                'esp': 'Error',
                                'rus': 'Ошибка'}
read_rows_data_msgbox_text1 = {'eng': 'Error reading rows data file:\n\nPlaceholder \'_individual_option\' not found in table \'_key\'',
                               'ger': 'Fehler beim Lesen der Zeilendaten:\n\nPlatzhalter \'_individual_option\' nicht gefunden in Tabelle \'_key\'',
                               'esp': 'Error al leer el archivo de datos de filas:\n\nEl marcador de posición \'_individual_option\' no se encontró en la tabla \'_key\'',
                               'rus': 'Ошибка чтения файла данных строк:\n\nЗаполнитель \'_individual_option\' не найден в таблице \'_key\''}

read_rows_data_msgbox_title2 = {'eng': 'Error',
                                'ger': 'Fehler',
                                'esp': 'Error',
                                'rus': 'Ошибка'}
read_rows_data_msgbox_text2 = {'eng': 'Error reading rows data file:\n\n\'_key\' is used as playeholder name, but there\'s no table with that name',
                               'ger': 'Fehler beim Lesen der Zeilendaten:\n\n\'_key\' wird als Platzhaltername verwendet, aber es gibt keine Tabelle mit diesem Namen',
                               'esp': 'Error al leer el archivo de datos de filas:\n\n\'_key\' se usa como nombre de marcador de posición, pero no hay ninguna tabla con ese nombre',
                               'rus': 'Ошибка чтения файла данных строк:\n\n\'_key\' используется как имя заполнителя, но нет таблицы с таким именем'}
