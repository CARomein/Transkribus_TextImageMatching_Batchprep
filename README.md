# File Batch Organiser for Transkribus TIM

A Python script for organising pairs of text and image files into batches ready for upload to Transkribus Text Image Matching (TIM). The tool automatically creates appropriately sized batches with properly formatted concatenated text files, streamlining the TIM workflow for large document collections.

## Overview

Transkribus Text Image Matching (TIM) allows users to match corrected text against existing Transkribus documents. However, TIM requires specific input formatting:

- **Batch size limitation**: TIM works most efficiently with batches of approximately 250 image files
- **Text file format**: All text for a batch must be concatenated into a single file with `TRP_PAGEBREAK` markers separating individual documents
- **File organisation**: Image and text files must be organised together in batches

This script automates the entire batching process. It scans a directory containing matching pairs of text files (`.txt`) and image files (`.jpg` or other formats), sorts them alphabetically, divides them into batches of a specified size (default 250 pairs), creates numbered folders for each batch, copies or moves the files into these folders, and generates the properly formatted concatenated text file that TIM requires.

The result is a collection of ready-to-upload batch folders, each containing up to 250 image files, their corresponding individual text files, and a single `combined.txt` file formatted for TIM import.

## Transkribus TIM Requirements

TIM expects the following input structure for text matching:

**Text format:**
- A single text file containing the transcribed text for all images in the batch
- Documents must be separated by `TRP_PAGEBREAK` markers
- The pagebreak marker must appear on its own line between documents

**Example of properly formatted combined text file:**
```
Text content of first document goes here.
This can span multiple lines.
TRP_PAGEBREAK
Text content of second document.
Also with multiple lines of text.
TRP_PAGEBREAK
Text content of third document.
And so forth.
```

**Batch structure:**
Each batch folder should contain:
- Individual image files (`.jpg`, `.png`, or other image formats)
- Individual text files (optional, for reference)
- One `combined.txt` file with all text concatenated and separated by `TRP_PAGEBREAK` markers

This script creates exactly this structure automatically.

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

Download the `batch_organizer.py` script and place it in a convenient location. No installation is required beyond having Python installed on your system.

## Usage

### Basic Usage

The simplest form requires only the path to your source directory:

```bash
python batch_organizer.py /path/to/your/files
```

This will create batches of 250 file pairs, with folders named `Batch_01`, `Batch_02`, and so forth.

### Advanced Usage

The script accepts several optional parameters to customise its behaviour:

```bash
python batch_organizer.py SOURCE_DIR [options]
```

#### Parameters

**Required:**
- `SOURCE_DIR`: Path to the directory containing the files to organise

**Optional:**
- `--batch-size SIZE`: Number of file pairs per batch (default: 250)
- `--prefix PREFIX`: Prefix for batch folder names (default: Batch)
- `--text-ext EXT`: Extension for text files (default: .txt)
- `--image-ext EXT`: Extension for image files (default: .jpg)
- `--combined-name NAME`: Name for the concatenated text file (default: combined.txt)
- `--move`: Move files instead of copying them (default: copy)

### Examples

**Organise Latvian court records with custom prefix:**
```bash
python batch_organizer.py C:/Documents/Latvian1730 --prefix Latvian
```

**Create smaller batches of 100 pairs for testing:**
```bash
python batch_organizer.py ./scans --batch-size 100
```

**Work with PNG images instead of JPG:**
```bash
python batch_organizer.py ./images --image-ext .png
```

**Move files instead of copying:**
```bash
python batch_organizer.py ./originals --move
```

**Combine multiple options:**
```bash
python batch_organizer.py C:/Research/Documents --batch-size 150 --prefix Project --move
```

## Output Structure

The script creates batch folders in the source directory with the following structure:

```
Source_Directory/
├── Prefix_01/
│   ├── file_001.txt
│   ├── file_001.jpg
│   ├── file_002.txt
│   ├── file_002.jpg
│   ├── ...
│   └── combined.txt
├── Prefix_02/
│   ├── file_251.txt
│   ├── file_251.jpg
│   ├── ...
│   └── combined.txt
└── ...
```

Each `combined.txt` file contains all text files from that batch, separated by `TRP_PAGEBREAK` markers on individual lines, ready for direct upload to Transkribus TIM.

## How It Works

The script performs the following operations:

1. Scans the source directory for all text files with the specified extension
2. Identifies matching image files (same filename, different extension)
3. Sorts all file pairs alphabetically by filename
4. Divides the pairs into batches of the specified size (last batch may contain fewer than the specified number)
5. Creates numbered folders with zero-padded batch numbers (01, 02, 03, etc.)
6. Copies or moves the file pairs into their respective batch folders
7. Concatenates all text files within each batch into a single `combined.txt` file, inserting `TRP_PAGEBREAK` on its own line between each document

## Transkribus TIM Workflow

After running this script, your Transkribus TIM workflow becomes straightforward:

1. **Run the batch organiser** on your collection of paired text and image files
2. **Upload to Transkribus**: For each batch folder:
   - Upload the image files to create a new Transkribus document
   - Upload the `combined.txt` file as the source text for matching
3. **TIM matching**: TIM will attempt to match the text in `combined.txt` to the appropriate regions in your images, using the `TRP_PAGEBREAK` markers to determine document boundaries
4. **Review and correct**: Review TIM's matching results and make any necessary corrections in Transkribus

The script ensures that your text is properly formatted with pagebreaks and that your batches are appropriately sized for efficient TIM processing.

## Important Notes

**File Matching:** The script only processes files that have matching pairs. If a text file has no corresponding image file (or vice versa), a warning will be displayed, but processing continues with the matched pairs.

**File Safety:** By default, the script copies files rather than moving them, preserving your original directory structure. Use the `--move` flag only if you are certain you want to relocate the original files.

**Encoding:** Text files are read and written using UTF-8 encoding, which handles most character sets correctly, including historical texts with diacritics and special characters.

**Existing Folders:** If batch folders with the same names already exist, the script will add files to those folders. Exercise caution if re-running the script on the same directory.

**Batch Size Flexibility:** The last batch may contain fewer file pairs than the specified batch size. This is normal and TIM handles variable batch sizes without issue.

**Alphabetical Order:** Files are organised alphabetically within each batch and the concatenated text file maintains this alphabetical order, ensuring consistency between images and text.

## Troubleshooting

**"Directory does not exist" error:** Verify that the path to your source directory is correct. On Windows, you may need to use forward slashes (/) or escape backslashes (\\\\).

**"No file pairs found" message:** Ensure that your text and image files have matching filenames (excluding extensions) and that you have specified the correct file extensions if they differ from the defaults.

**Permission errors:** Ensure you have read and write permissions for the source directory.

**Script window closes immediately (Windows):** Run the script from Command Prompt or PowerShell rather than double-clicking it, so you can see any error messages.

**TIM not matching correctly:** Verify that your `combined.txt` file contains `TRP_PAGEBREAK` on its own line between documents. Open the file in a text editor to confirm the format.

**Text encoding issues:** If TIM displays garbled characters, ensure your original text files are UTF-8 encoded. Most modern text editors can convert files to UTF-8.

## Performance

### Processing Speed

- **File organisation**: Near-instantaneous for typical collections (<5000 files)
- **Text concatenation**: 1-5 seconds per batch depending on text file sizes
- **Overall processing**: Usually completes in under a minute for most collections

### Scalability

The script efficiently handles collections of various sizes:
- Small collections (100-500 files): Seconds to complete
- Medium collections (1000-3000 files): Under a minute
- Large collections (5000+ files): 1-2 minutes

Memory usage remains minimal regardless of collection size.

## Limitations

- **In-place operation**: Creates batch folders in the source directory
- **Single file format**: Expects one text file and one image file per document
- **No validation**: Does not verify file contents or TIM compatibility
- **Manual upload**: Does not automatically upload to Transkribus (upload must be done manually through Transkribus interface)
- **Fixed pagebreak format**: Uses standard `TRP_PAGEBREAK` format only

## Best Practices

1. **Test on subset first**: Before processing your entire collection, test the script on a small subset to verify the output format
2. **Use default batch size**: The default of 250 pairs works well with TIM; adjust only if you have specific requirements
3. **Keep originals**: Use the default copy mode rather than move mode until you are confident the batches are correct
4. **Verify alphabetical order**: Check that your filenames sort correctly alphabetically (use leading zeros for numbers: 001, 002, 003, etc.)
5. **Check combined.txt**: Open one or two `combined.txt` files in a text editor to verify the `TRP_PAGEBREAK` markers appear correctly
6. **Document your batches**: Keep notes on which batch numbers correspond to which archival units or date ranges
7. **Consistent naming**: Ensure all your text and image files follow a consistent naming convention before batching

## Licence

This project is licensed under the MIT Licence - see the [LICENCE](LICENCE) file for details.
