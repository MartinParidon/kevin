import os
import sys
import fillpdf2


def main():
    # Template path as input argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <template_path>")
        print("Example: python script.py C:/path/to/template.pdf")
        sys.exit(1)

    template_path = sys.argv[1]

    # Check if file exists
    if not os.path.exists(template_path):
        print(f"Error: File not found: {template_path}")
        sys.exit(1)

    # Extract form fields
    print(f"Reading form fields from: {template_path}")
    form_fields = fillpdf2.write_fillable_pdf(template_path)

    # Extract only the keys (field names)
    field_names = list(form_fields.keys())

    print(f"\nFound fields ({len(field_names)}):")
    for i, field in enumerate(field_names, 1):
        print(f"  {i}. {field}")

    # Save list as text file next to the PDF file
    pdf_dir = os.path.dirname(os.path.abspath(template_path))
    pdf_basename = os.path.splitext(os.path.basename(template_path))[0]
    output_file = os.path.join(pdf_dir, f"{pdf_basename}_form_fields.txt")

    with open(output_file, 'w', encoding='utf-8') as f:
        for field in field_names:
            f.write(f"{field}\n")

    print(f"\nField names saved to: {output_file}")


if __name__ == "__main__":
    main()