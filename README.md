# Guitarians Scraping Tools

A collection of Python scripts used to scrape chord sheets from Guitarians.com, a popular Cantopop chord database. These tools help automate the process of collecting, converting, and organizing guitar chord sheets into PDF format.

## Scripts

### 1. url_to_pdf.py
Convert Guitarians URLs to PDF files.

```bash
uv run url_to_pdf.py -i <input_file> -o <output_file> [-clicks <number>]
```

**Parameters:**
- `-i, --input`: Input text file containing the URL (required)
- `-o, --output`: Output PDF file path (required)
- `-clicks, --clicks`: Number of times to click the font larger button (default: 0)

**Example:**
```bash
uv run url_to_pdf.py -i songs/eason.txt -o eason_chord.pdf -clicks 3
```

### 2. list_artist_songs.py
Scrape song lists from Guitarians artist profile pages.

```bash
uv run list_artist_songs.py <artist_url>
```

**Parameters:**
- `<artist_url>`: URL of the Guitarians artist page to scrape (required)

**Example:**
```bash
uv run list_artist_songs.py "https://zh-hk.guitarians.com/artist/{artist-id}-{artist-name}"
```

### 3. unicode_fix.py
Fix URL-encoded Unicode characters in text files to display properly.

```bash
uv run unicode_fix.py -i <file_path>
```

**Parameters:**
- `-i, --input`: Path to the text file to fix Unicode characters in (required)

**Example:**
```bash
uv run unicode_fix.py -i songs/size1.txt
```

### 4. merge_pdfs.py
Merge multiple PDF files into a single PDF.

```bash
uv run pdfs/merge_pdfs.py -o <output_file> [-i <input_file> | -dir <directory> | <pdf_files>...]
```

**Parameters:**
- `-o, --output`: Output PDF file path (required)
- `-i, --input`: Text file containing list of PDF files to merge (one per line)
- `-dir, --directory`: Directory containing PDF files to merge
- `<pdf_files>`: PDF files to merge directly (alternative to -i or -dir)

**Examples:**
```bash
# Merge PDFs from a text file list
uv run merge_pdfs.py -o merged.pdf -i pdf_list.txt

# Merge all PDFs in a directory
uv run merge_pdfs.py -o combined.pdf -dir ./chord/

# Merge specific PDF files directly
uv run merge_pdfs.py -o final.pdf file1.pdf file2.pdf file3.pdf
```

### 5. scrape_user_chords.py
Scrape all chord links from a Guitarians user profile page.

```bash
uv run scrape_user_chords.py <user_id>
```

**Parameters:**
- `<user_id>`: User ID to scrape chord links from (required, e.g., 320385)

**Example:**
```bash
uv run scrape_user_chords.py 320385
```

### 6. process_user_chords.py
Orchestrate the complete workflow to scrape, process, and merge user chord PDFs. This script automates the entire process from scraping chord links to generating a merged PDF.

```bash
uv run process_user_chords.py <user_id> [-clicks <number>]
```

**Parameters:**
- `<user_id>`: User ID to process (required, e.g., 320385)
- `-clicks, --clicks`: Number of times to click the font larger button when generating PDFs (default: 0)

**Example:**
```bash
uv run process_user_chords.py 320385 -clicks 3
```
