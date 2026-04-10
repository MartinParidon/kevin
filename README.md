# Kevin

Kevin is a small desktop app that generates documents from a database file (.xlsx), a file (.xlsx) for names or other "row" values and a template file (.docx or .pdf) via a simple GUI.

## Requirements

- Python (tested with: 3.14)
- Windows (uses PySide6/pywin32)

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python .\src\main.py
```

## Build (Standalone executable)

```powershell
python .\scripts\make_release.py
python .\scripts\make_release.py --cmdline
```

Build artifacts are written to `dist/`.

## Documentation

- `docu/ger/*.pptx`

## License

MIT, see `LICENSE`.
