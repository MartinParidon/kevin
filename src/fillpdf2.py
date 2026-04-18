import pdfrw
from pdfrw.objects.pdfname import BasePdfName
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfarray import PdfArray
from typing import Dict, Any, Optional, Union, List
from pathlib import Path


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_FIELD_PARENT_KEY = '/Parent'
ANNOT_FORM_type = '/FT'
ANNOT_FORM_button = '/Btn'
ANNOT_FORM_text = '/Tx'
ANNOT_FORM_combo = '/Ch'
ANNOT_FORM_options = '/Opt'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
ANNOT_FIELD_KIDS_KEY = '/Kids'
ANNOT_FORM_radio = '/Radio'
ANNOT_VAL_KEY = '/V'
ANNOT_APPEARANCE_KEY = '/AP'
ANNOT_FORM_OPTIONS_KEY = '/Opt'
ANNOT_FORM_KIDS_KEY = '/Kids'


def get_form_fields(
        input_pdf_path: Union[str, Path],
        sort: bool = False,
        page_number: Optional[int] = None
) -> Dict[str, Any]:
    """
    Extracts all form fields and their current values from a PDF form.

    Parameters
    ----------
    input_pdf_path : str or Path
        Path to the PDF file
    sort : bool, default=False
        If True, returns dictionary sorted by field names
    page_number : int, optional
        If provided, only extract fields from this specific page (1-indexed)

    Returns
    -------
    dict
        Dictionary with field names as keys and their current values as values

    Raises
    ------
    FileNotFoundError
        If the PDF file doesn't exist
    ValueError
        If page_number is invalid
    """
    # Validate input file
    pdf_path = Path(input_pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {input_pdf_path}")

    # Validate page_number
    if page_number is not None:
        if not isinstance(page_number, int):
            raise ValueError(f"page_number must be an integer, got {type(page_number).__name__}")
        if page_number < 1:
            raise ValueError(f"page_number must be >= 1, got {page_number}")

    # Read PDF
    pdf = pdfrw.PdfReader(str(pdf_path))

    # Validate page_number range
    if page_number is not None and page_number > len(pdf.pages):
        raise ValueError(f"page_number {page_number} exceeds total pages {len(pdf.pages)}")

    # Extract fields
    data_dict = {}

    for current_page_num, page in enumerate(pdf.pages, start=1):
        # Skip if we only want a specific page
        if page_number is not None and current_page_num != page_number:
            continue

        # Process annotations on this page
        annotations = page[ANNOT_KEY] if hasattr(page, ANNOT_KEY) and ANNOT_KEY in page else []
        for annotation in annotations:
            field_data = extract_field_data(annotation)
            if field_data:
                field_name, field_value = field_data

                # Handle nested field names (already handled in extract_field_data)
                if field_name not in data_dict:
                    data_dict[field_name] = field_value
                else:
                    # If field appears multiple times (e.g., radio button group),
                    # we might want to keep the first or merge. Here we keep the first.
                    pass

        # Stop if we processed the requested page
        if page_number is not None and current_page_num == page_number:
            break

    # Sort if requested
    if sort:
        return dict(sorted(data_dict.items()))
    return data_dict


def extract_field_data(annotation) -> Optional[tuple[str, Any]]:
    """
    Extract field name and value from a single annotation.
    Returns (field_name, field_value) or None if not a form field.
    """
    # Skip if not a widget annotation
    if annotation.get(SUBTYPE_KEY) != WIDGET_SUBTYPE_KEY:
        return None

    # Get the target field (handles parent hierarchy)
    target = get_target_field(annotation)

    # Get field name
    field_name = get_field_name(target)
    if not field_name:
        return None

    # Get field type
    field_type = target.get(ANNOT_FORM_type)

    # Extract value based on field type
    field_value = extract_field_value(target, annotation, field_type)

    return (field_name, field_value)


def get_target_field(annotation):
    """
    Get the target field that contains the actual field properties.
    Some annotations are just widgets that point to a parent with the field data.
    """
    # If this annotation has a field type, it's the target
    if annotation.get(ANNOT_FORM_type):
        return annotation

    # Check parent
    parent = annotation.get(ANNOT_FIELD_PARENT_KEY)
    if parent and parent.get(ANNOT_FORM_type):
        return parent

    # Check if it's a radio button widget (may not have FT but has AP)
    if annotation.get(ANNOT_APPEARANCE_KEY):
        # Try to find parent with field info
        if parent:
            return parent

    # Return original as fallback
    return annotation


def get_field_name(field) -> Optional[str]:
    """
    Get the fully qualified field name including parent hierarchy.
    Returns None if no name found.
    """
    name_parts = []
    current = field

    # Collect names from current field up to root
    while current:
        field_name = current.get(ANNOT_FIELD_KEY)
        if field_name:
            # Decode and clean the name
            if isinstance(field_name, pdfrw.objects.pdfstring.PdfString):
                name = field_name.decode()
            else:
                name = str(field_name)

            # Remove parentheses if present
            if name and name[0] == '(' and name[-1] == ')':
                name = name[1:-1]

            if name:
                name_parts.insert(0, name)

        current = current.get(ANNOT_FIELD_PARENT_KEY)

    return '.'.join(name_parts) if name_parts else None


def extract_field_value(target, widget, field_type) -> Any:
    """
    Extract the current value from a field based on its type.
    """
    # Try to get value from target first, then from widget
    value = target.get(ANNOT_VAL_KEY)
    if value is None and widget != target:
        value = widget.get(ANNOT_VAL_KEY)

    # Handle different field types
    if field_type == ANNOT_FORM_button:
        return extract_button_value(target, widget, value)
    elif field_type == ANNOT_FORM_combo:
        return extract_combo_value(target, value)
    elif field_type == ANNOT_FORM_text:
        return extract_text_value(value)
    else:
        # Unknown field type, try generic extraction
        return extract_generic_value(value)


def extract_button_value(target, widget, value) -> Any:
    """
    Extract value from button fields (checkboxes and radio buttons).
    """
    # Check if it's a radio button group
    is_radio = target.get('/Flags') and (int(target['/Flags']) & (1 << 15))

    if is_radio:
        return extract_radio_value(target, widget)
    else:
        return extract_checkbox_value(target, widget, value)


def extract_checkbox_value(target, widget, value) -> str:
    """
    Extract value from a checkbox.
    Returns 'Yes' if checked, 'Off' if unchecked, or the actual export value.
    """
    # Get the appearance state from the widget
    as_state = widget.get('/AS')
    if as_state:
        # Convert to string without leading slash
        state_str = str(as_state)
        if state_str.startswith('/'):
            state_str = state_str[1:]

        # Check if it's checked (not Off)
        if state_str.lower() != 'off':
            # Try to get the actual export value from V
            if value:
                if isinstance(value, pdfrw.objects.pdfname.BasePdfName):
                    export_str = str(value)
                    if export_str.startswith('/'):
                        export_str = export_str[1:]
                    return export_str
            return state_str
        else:
            return 'Off'

    # Fallback: check V value
    if value:
        if isinstance(value, pdfrw.objects.pdfname.BasePdfName):
            value_str = str(value)
            if value_str.startswith('/'):
                value_str = value_str[1:]
            return value_str if value_str.lower() != 'off' else 'Off'
        return str(value)

    return 'Off'


def extract_radio_value(target, widget) -> str:
    """
    Extract the selected value from a radio button group.
    Returns the export value of the selected button, or 'Off' if none selected.
    """
    # Check the V value of the target (parent)
    v_value = target.get(ANNOT_VAL_KEY)
    if v_value:
        if isinstance(v_value, pdfrw.objects.pdfname.BasePdfName):
            value_str = str(v_value)
            if value_str.startswith('/'):
                value_str = value_str[1:]
            return value_str if value_str.lower() != 'off' else ''

    # Check all kids to find which one is selected
    kids = target.get(ANNOT_FORM_KIDS_KEY, [])
    for kid in kids:
        as_state = kid.get('/AS')
        if as_state and str(as_state) != '/Off':
            # Found selected button, get its export value
            export_value = get_radio_export_value_from_kid(kid)
            if export_value:
                return export_value

    # No selection found
    return ''


def get_radio_export_value_from_kid(kid) -> Optional[str]:
    """
    Extract the export value from a radio button widget.
    """
    # Try to get from appearance states (non-Off state)
    ap = kid.get(ANNOT_APPEARANCE_KEY)
    if ap and ap.get('/N'):
        for state in ap['/N'].keys():
            if state != '/Off':
                state_str = str(state)
                if state_str.startswith('/'):
                    state_str = state_str[1:]
                return state_str

    # Try to get from the kid's V value
    v_value = kid.get(ANNOT_VAL_KEY)
    if v_value:
        if isinstance(v_value, pdfrw.objects.pdfname.BasePdfName):
            value_str = str(v_value)
            if value_str.startswith('/'):
                value_str = value_str[1:]
            if value_str.lower() != 'off':
                return value_str

    return None


def extract_combo_value(target, value) -> Any:
    """
    Extract value from combo box or list box.
    Returns string for single selection, list for multi-selection.
    """
    if value is None:
        return ''

    # Handle multi-select (PdfArray)
    if isinstance(value, pdfrw.objects.pdfarray.PdfArray):
        selected = []
        for item in value:
            if isinstance(item, pdfrw.objects.pdfstring.PdfString):
                selected.append(item.decode())
            else:
                selected.append(str(item))
        return selected if len(selected) > 1 else (selected[0] if selected else '')

    # Handle single select
    if isinstance(value, pdfrw.objects.pdfstring.PdfString):
        return value.decode()

    if isinstance(value, pdfrw.objects.pdfname.BasePdfName):
        value_str = str(value)
        if value_str.startswith('/'):
            value_str = value_str[1:]
        return value_str

    return str(value) if value is not None else ''


def extract_text_value(value) -> str:
    """
    Extract value from text field.
    """
    if value is None:
        return ''

    if isinstance(value, pdfrw.objects.pdfstring.PdfString):
        return value.decode()

    if isinstance(value, pdfrw.objects.pdfname.BasePdfName):
        value_str = str(value)
        if value_str.startswith('/'):
            value_str = value_str[1:]
        return value_str

    return str(value)


def extract_generic_value(value) -> str:
    """
    Generic value extraction for unknown field types.
    """
    if value is None:
        return ''

    if isinstance(value, pdfrw.objects.pdfstring.PdfString):
        return value.decode()

    if isinstance(value, pdfrw.objects.pdfname.BasePdfName):
        value_str = str(value)
        if value_str.startswith('/'):
            value_str = value_str[1:]
        return value_str

    return str(value)


# Convenience function to get field info including types and options
def get_form_fields_detailed(
        input_pdf_path: Union[str, Path],
        page_number: Optional[int] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Extracts detailed information about form fields including type, options, and current value.

    Returns a dictionary with field names as keys and dicts containing:
    - 'type': field type (text, button, combo)
    - 'value': current value
    - 'options': list of options (for combo boxes)
    - 'read_only': boolean indicating if field is read-only
    """
    pdf_path = Path(input_pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {input_pdf_path}")

    pdf = pdfrw.PdfReader(str(pdf_path))

    if page_number is not None:
        if not isinstance(page_number, int) or page_number < 1 or page_number > len(pdf.pages):
            raise ValueError(f"Invalid page_number: {page_number}")

    detailed_dict = {}

    for current_page_num, page in enumerate(pdf.pages, start=1):
        if page_number is not None and current_page_num != page_number:
            continue

        annotations = page.get(ANNOT_KEY, [])
        for annotation in annotations:
            if annotation.get(SUBTYPE_KEY) != WIDGET_SUBTYPE_KEY:
                continue

            target = get_target_field(annotation)
            field_name = get_field_name(target)

            if not field_name:
                continue

            field_type = target.get(ANNOT_FORM_type)
            field_info = {
                'type': get_field_type_name(field_type),
                'value': extract_field_value(target, annotation, field_type),
                'read_only': is_field_read_only(target),
            }

            # Add options for combo/list boxes
            if field_type == ANNOT_FORM_combo:
                options = get_field_options_from_target(target)
                if options:
                    field_info['options'] = options

            # Add radio button group info
            if field_type == ANNOT_FORM_button and is_radio_group(target):
                field_info['radio_options'] = get_radio_options(target)

            detailed_dict[field_name] = field_info

        if page_number is not None and current_page_num == page_number:
            break

    return detailed_dict


def get_field_type_name(field_type) -> str:
    """Convert PDF field type to readable string."""
    type_map = {
        ANNOT_FORM_button: 'button',
        ANNOT_FORM_text: 'text',
        ANNOT_FORM_combo: 'combo',
    }
    return type_map.get(field_type, 'unknown')


def is_field_read_only(field) -> bool:
    """Check if a field is read-only."""
    ff = field.get('/Ff')
    if ff:
        read_only_flag = 1  # Bit 0
        return bool(int(ff) & read_only_flag)
    return False


def is_radio_group(field) -> bool:
    """Check if a button field is a radio button group."""
    flags = field.get('/Flags')
    if flags:
        radio_flag = 1 << 15  # Bit 15
        return bool(int(flags) & radio_flag)
    return False


def get_field_options_from_target(target) -> Optional[List[str]]:
    """Extract options from a combo/list box."""
    current = target
    while current:
        options = current.get(ANNOT_FORM_OPTIONS_KEY)
        if options is not None and len(options) > 0:
            decoded = []
            for opt in options:
                if isinstance(opt, pdfrw.objects.pdfarray.PdfArray):
                    # Export/Value pair - take the display value
                    if len(opt) > 1:
                        value = opt[1]
                    else:
                        value = opt[0]
                else:
                    value = opt

                if isinstance(value, pdfrw.objects.pdfstring.PdfString):
                    decoded.append(value.decode())
                else:
                    decoded.append(str(value))
            return decoded
        current = current.get(ANNOT_FIELD_PARENT_KEY)
    return None


def get_radio_options(target) -> List[str]:
    """Get all export values from a radio button group."""
    options = []
    kids = target.get(ANNOT_FORM_KIDS_KEY, [])
    for kid in kids:
        export_value = get_radio_export_value_from_kid(kid)
        if export_value:
            options.append(export_value)
    return options


def write_fillable_pdf(input_pdf_path: str, output_pdf_path: str, data_dict: Dict[str, Any], flatten: bool = False):
    """
    Fills a PDF form with data from a dictionary.

    Parameters
    ----------
    input_pdf_path : str
        Path to the input PDF form
    output_pdf_path : str
        Path for the output PDF
    data_dict : dict
        Dictionary with field names and values
    flatten : bool, default=False
        If True, flattens the form (makes fields uneditable)
    """
    # Convert all values to strings for consistency
    data_dict = {k: convert_value_to_string(v) for k, v in data_dict.items()}

    # Read the template PDF
    template_pdf = pdfrw.PdfReader(input_pdf_path)

    # Process each page
    for page in template_pdf.pages:
        if page.get(ANNOT_KEY):
            for annotation in page[ANNOT_KEY]:
                process_annotation(annotation, data_dict)

    # Set NeedAppearances to ensure proper rendering
    if template_pdf.Root.AcroForm:
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    else:
        template_pdf.Root.AcroForm = pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'))

    # Write the output PDF
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


def convert_value_to_string(value: Any) -> str:
    """Convert any value to a string representation."""
    if isinstance(value, list):
        return ','.join(str(v) for v in value)
    return str(value) if value is not None else ""


def get_full_field_name(field) -> str:
    """
    Get the fully qualified field name including parent hierarchy.
    Example: 'Parent.Child.Grandchild'
    """
    name_parts = []
    current = field

    # Collect names from current field up to root
    while current:
        if current.get(ANNOT_FIELD_KEY):
            # Remove parentheses if present
            name = current[ANNOT_FIELD_KEY]
            if name and name[0] == '(' and name[-1] == ')':
                name = name[1:-1]
            name_parts.insert(0, str(name))
        current = current.get(ANNOT_FIELD_PARENT_KEY)

    return '.'.join(name_parts)


def get_target_field(annotation):
    """
    Get the target field (the one with the actual field properties).
    For widgets without /FT, look at parent.
    """
    if annotation.get(ANNOT_FORM_type):
        return annotation
    if annotation.get(ANNOT_FIELD_PARENT_KEY):
        parent = annotation[ANNOT_FIELD_PARENT_KEY]
        if parent.get(ANNOT_FORM_type):
            return parent
    return annotation


def get_field_options(field) -> Optional[List[str]]:
    """
    Recursively search for /Opt options in field hierarchy.
    Returns a list of option values (decoded strings).
    """
    current = field
    while current:
        options = current.get(ANNOT_FORM_options)
        if options is not None and len(options) > 0:
            return decode_options(options)
        current = current.get(ANNOT_FIELD_PARENT_KEY)
    return None


def decode_options(options) -> List[str]:
    """
    Decode PDF option arrays into a list of strings.
    Handles both simple arrays and export/value pairs.
    """
    decoded = []

    for opt in options:
        if isinstance(opt, PdfArray):
            # Export/Value pair: take the display value (second element)
            if len(opt) > 1:
                value = opt[1]
            else:
                value = opt[0]
        else:
            value = opt

        # Decode if it's a PdfString
        if isinstance(value, PdfString):
            decoded.append(value.decode())
        else:
            decoded.append(str(value))

    return decoded


def process_annotation(annotation, data_dict: Dict[str, str], flatten=False):
    """Process a single annotation."""
    # Skip non-widget annotations
    if annotation.get(SUBTYPE_KEY) != WIDGET_SUBTYPE_KEY:
        return

    # Get the target field (where the actual field properties are)
    target = get_target_field(annotation)

    # Skip fields without type
    field_type = target.get(ANNOT_FORM_type)
    if not field_type:
        return

    # Get the full field name
    field_name = get_full_field_name(target)

    # Check if we have data for this field
    if field_name not in data_dict:
        return

    field_value = data_dict[field_name]

    # Process based on field type
    if field_type == ANNOT_FORM_button:
        process_button_field(target, annotation, field_name, field_value)
    elif field_type == ANNOT_FORM_combo:
        process_combo_field(target, annotation, field_name, field_value)
    elif field_type == ANNOT_FORM_text:
        process_text_field(target, annotation, field_name, field_value)

    # Flatten if requested (make read-only)
    if flatten:
        make_field_read_only(annotation)


def process_button_field(target, widget, field_name: str, field_value: str):
    """Process button fields (checkboxes and radio buttons)."""
    # Check if it's a radio button group
    is_radio = target.get('/Flags') and (target['/Flags'] & (1 << 15))  # 15 = Radio flag

    if is_radio:
        process_radio_button(target, widget, field_name, field_value)
    else:
        process_checkbox(target, widget, field_name, field_value)


def process_checkbox(target, widget, field_name: str, field_value: str):
    """Process a checkbox field."""
    # Determine the state name (usually 'Yes' for checked, 'Off' for unchecked)
    # Convert common true/false values
    if field_value.lower() in ['true', 'yes', '1', 'on', 'checked']:
        state = '/Yes'
    elif field_value.lower() in ['false', 'no', '0', 'off', 'unchecked']:
        state = '/Off'
    else:
        # Use the value directly (might be custom export value)
        state = f'/{field_value}' if not field_value.startswith('/') else field_value

    # Convert to PdfName
    state_name = BasePdfName(state)

    # Update the field
    target.update(pdfrw.PdfDict(V=state_name, AS=state_name))

    # Also update the widget if it's a separate object
    if widget != target and widget.get(ANNOT_FIELD_PARENT_KEY) == target:
        widget.update(pdfrw.PdfDict(AS=state_name))


def process_radio_button(target, widget, field_name: str, field_value: str):
    """Process a radio button group."""
    # For radio buttons, we need to find the specific button with matching export value
    kids = target.get(ANNOT_FIELD_KIDS_KEY, [])

    # Convert field value to expected format
    expected_state = f'/{field_value}' if not field_value.startswith('/') else field_value

    # Update each radio button in the group
    for kid in kids:
        # Get the export value for this radio button
        export_value = get_radio_export_value(kid)

        if export_value == expected_state:
            # This button should be selected
            kid.update(pdfrw.PdfDict(AS=BasePdfName(export_value)))
            target.update(pdfrw.PdfDict(V=BasePdfName(export_value)))
        else:
            # This button should be off
            kid.update(pdfrw.PdfDict(AS=BasePdfName('/Off')))


def get_radio_export_value(radio_button) -> str:
    """Extract the export value from a radio button."""
    # Try to get from appearance states
    ap = radio_button.get('/AP')
    if ap and ap.get('/N'):
        # Get the first non-Off state
        for state in ap['/N'].keys():
            if state != '/Off':
                return state

    # Fallback: try the 'V' value from parent or current
    parent = radio_button.get(ANNOT_FIELD_PARENT_KEY)
    if parent and parent.get('/V'):
        return str(parent['/V'])

    return '/Off'


def process_combo_field(target, widget, field_name: str, field_value: str):
    """Process combo box (dropdown) fields."""
    # Get available options
    options = get_field_options(target)
    if not options:
        raise KeyError(f"No options found for combo box '{field_name}'")

    # Handle multi-select (value as list)
    if isinstance(field_value, list):
        selected_values = []
        for val in field_value:
            if val in options:
                selected_values.append(PdfString.encode(val))
            elif val != "None" and val != "":
                raise KeyError(f"'{val}' not an option for '{field_name}'. Options: {options}")

        pdf_value = PdfArray(selected_values) if selected_values else PdfArray()
    else:
        # Single select
        if field_value in options:
            pdf_value = PdfString.encode(field_value)
        elif field_value != "None" and field_value != "":
            raise KeyError(f"'{field_value}' not an option for '{field_name}'. Options: {options}")
        else:
            pdf_value = PdfString.encode('')

    # Update the field
    target.update(pdfrw.PdfDict(V=pdf_value, AS=pdf_value))

    # Also update the widget if different from target
    if widget != target and widget.get(ANNOT_FIELD_PARENT_KEY) == target:
        widget.update(pdfrw.PdfDict(AS=pdf_value))

    # Update any kids
    if target.get(ANNOT_FIELD_KIDS_KEY):
        for kid in target[ANNOT_FIELD_KIDS_KEY]:
            kid.update(pdfrw.PdfDict(V=pdf_value, AS=pdf_value))


def process_text_field(target, widget, field_name: str, field_value: str):
    """Process text fields."""
    # Convert value to string and encode as PdfString
    pdf_value = PdfString.encode(str(field_value))

    # Update the field (only V, not AP!)
    target.update(pdfrw.PdfDict(V=pdf_value))

    # Also update the widget if it's a separate object
    if widget != target and widget.get(ANNOT_FIELD_PARENT_KEY) == target:
        widget.update(pdfrw.PdfDict(V=pdf_value))

    # Update any kids
    if target.get(ANNOT_FIELD_KIDS_KEY):
        for kid in target[ANNOT_FIELD_KIDS_KEY]:
            kid.update(pdfrw.PdfDict(V=pdf_value))


def make_field_read_only(annotation):
    """Make a field read-only by setting the appropriate flags."""
    # Get current flags
    current_ff = annotation.get('/Ff')
    if current_ff is None:
        current_ff = 0
    else:
        current_ff = int(current_ff)

    # Set the read-only flag (bit 0)
    # Bit 0 = 1 = Read-only
    # For more details: PDF spec Table 226 - Field flags
    read_only_flag = 1
    new_ff = current_ff | read_only_flag

    annotation.update(pdfrw.PdfDict(Ff=new_ff))