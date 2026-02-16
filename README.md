# Dot Matrix PDF
A Python utility to convert CSV and TXT files into PDFs with a "Dot Matrix" visual style. It mimics the look of old printer output, complete with a customizable header box, page numbering, and styled column headers for tabular data.

Inspired by Andrew Schmelyun's project ***Getting my daily news from a dot matrix printer***
https://aschmelyun.com/blog/getting-my-daily-news-from-a-dot-matrix-printer/

## Features

```
                                     ┌───────────────────────────────────────────────────────────┐                                   
                                     │DOC ID : <DOCUMENT-ID>                      16 - 02 - 2026 │                                   
┌────────────────────────────────────└───────────────────────────────────────────────────────────┘──────────────────────────────────┐
│                                                                                                                                   │
│ <TITLE>                                                                                                   TAG: <TAG>              │
│                                                                                                                                   │
│ <DESCRIPTION>                                                                                                                     │
│                                                                                                                                   │
│                                                                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘                                                                                                                                                                                
────HEADER─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────(1/2)─
```

-   **Format Support**: Handles both `.csv` (Table format) and `.txt` (Plain text) files.
-   **Header Box**: Customizable header with Title, Description, Doc ID, Date, Tag, and Author.
-   **Page Numbering**: Automatically adds `(Current/Total)` page numbers to every page header.
-   **Column Headers (CSV only)**: Automatically extracts the first row as column headers and styles them with **Bold** (simulated) and <u>Underline</u> on every page.
-   **Custom Font**: Default support for `Doto` font (or any TTF provided) for that authentic 80s look.
-   **Pagination**: Automatic page breaks based on content length.

## Setup

1.  **Install Python 3.x**

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Linux/Mac
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
    *(The main dependency is `reportlab`)*

3.  **Fonts**:
    Ensure `Doto.ttf` is in the script directory or provide a path to a custom TTF font.

## Usage

Run the script from the command line:

```bash
python dot_matrix.py <input_file> [options]
```

### Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `input_file` | Path to the source `.csv` or `.txt` file. | (Required) |
| `--output` | Path to the destination PDF file. | `<input_filename>.pdf` |
| `--title` | Text to display **inside** the main header box. | "REPORT" |
| `--header` | Text to display **below** the header box (e.g., Section Name). | "" |
| `--description`| Description text inside the header box. | "" |
| `--doc-id` | Document ID inside the header box. | Random UUID |
| `--tag` | Tag text (top right of box). | "" |
| `--author` | Author Name (below Tag). | "" |
| `--font` | Path to TTF font file. | `Doto.ttf` |
| `--font-size` | Font size of the content. | 10 |

### Examples

**Convert a CSV Table:**
```bash
python dot_matrix.py data.csv --title "SALES REPORT" --header "Q1 FY2026" --doc-id "SALES-001"
```

**Convert a Text Document:**
```bash
python dot_matrix.py notes.txt --title "MEETING NOTES" --header "INTERNAL ONLY" --author "Jane Doe"
```

## Output

The script generates a PDF file in the same directory as the input file (unless `--output` is specified).

-   **CSV files**: Rendered as a fixed-width table.
-   **TXT files**: Rendered as plain text lines.

## License

MIT
