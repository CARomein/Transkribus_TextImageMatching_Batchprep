import os
import shutil
import argparse
from pathlib import Path

def organize_files_into_batches(source_dir, batch_size, folder_prefix, 
                                  text_ext='.txt', image_ext='.jpg', 
                                  combined_name='combined.txt', move_files=False):
    """
    Organizes text and image files into batched folders with concatenated text files.
    
    Args:
        source_dir: Path to directory containing the files
        batch_size: Number of file pairs per batch
        folder_prefix: Prefix for batch folder names (e.g., 'Batch' creates 'Batch_01', 'Batch_02')
        text_ext: Extension for text files (default '.txt')
        image_ext: Extension for image files (default '.jpg')
        combined_name: Name for the concatenated text file (default 'combined.txt')
        move_files: If True, move files instead of copying (default False)
    """
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"Error: Directory {source_dir} does not exist")
        return
    
    # Find all text files and their corresponding image files
    text_files = sorted(source_path.glob(f"*{text_ext}"))
    file_pairs = []
    
    print(f"Scanning directory: {source_dir}")
    print(f"Found {len(text_files)} {text_ext} files")
    
    for text_file in text_files:
        image_file = text_file.with_suffix(image_ext)
        if image_file.exists():
            file_pairs.append((text_file, image_file))
        else:
            print(f"Warning: No matching {image_ext} for {text_file.name}")
    
    print(f"Found {len(file_pairs)} complete file pairs")
    
    if not file_pairs:
        print("No file pairs found. Exiting.")
        return
    
    # Calculate number of batches needed
    num_batches = (len(file_pairs) + batch_size - 1) // batch_size
    print(f"\nCreating {num_batches} batches of up to {batch_size} pairs each")
    
    operation = "Moving" if move_files else "Copying"
    
    # Process each batch
    for batch_num in range(num_batches):
        # Create batch folder name with zero-padded number
        folder_name = f"{folder_prefix}_{batch_num + 1:02d}"
        batch_folder = source_path / folder_name
        
        # Create batch folder
        batch_folder.mkdir(exist_ok=True)
        print(f"\nProcessing {folder_name}...")
        
        # Get file pairs for this batch
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(file_pairs))
        batch_pairs = file_pairs[start_idx:end_idx]
        
        print(f"  {operation} {len(batch_pairs)} file pairs...")
        
        # Copy or move files to batch folder
        for text_file, image_file in batch_pairs:
            if move_files:
                shutil.move(str(text_file), str(batch_folder / text_file.name))
                shutil.move(str(image_file), str(batch_folder / image_file.name))
            else:
                shutil.copy2(text_file, batch_folder / text_file.name)
                shutil.copy2(image_file, batch_folder / image_file.name)
        
        # Concatenate text files with TRP_PAGEBREAK
        print(f"  Concatenating {text_ext} files...")
        combined_file = batch_folder / combined_name
        
        with open(combined_file, 'w', encoding='utf-8') as outfile:
            for i, (text_file, _) in enumerate(batch_pairs):
                txt_path = batch_folder / text_file.name
                with open(txt_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    # Add pagebreak after each file except the last one
                    if i < len(batch_pairs) - 1:
                        outfile.write("\nTRP_PAGEBREAK\n")
        
        print(f"  Created {combined_file.name} with {len(batch_pairs)} documents")
    
    print(f"\n{'=' * 60}")
    print(f"Processing complete!")
    print(f"Created {num_batches} batch folders")
    print(f"Total file pairs processed: {len(file_pairs)}")
    print(f"{'=' * 60}")

def main():
    parser = argparse.ArgumentParser(
        description='Organize paired text and image files into batches with concatenated text files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_organizer.py C:/Documents/MyFiles --batch-size 250 --prefix Batch
  python batch_organizer.py ./images --batch-size 100 --prefix Project --move
  python batch_organizer.py C:/Data --text-ext .txt --image-ext .png
        """)
    
    parser.add_argument('source_dir', 
                        help='Path to the directory containing the files to organize')
    parser.add_argument('--batch-size', type=int, default=250,
                        help='Number of file pairs per batch (default: 250)')
    parser.add_argument('--prefix', default='Batch',
                        help='Prefix for batch folder names (default: Batch)')
    parser.add_argument('--text-ext', default='.txt',
                        help='Extension for text files (default: .txt)')
    parser.add_argument('--image-ext', default='.jpg',
                        help='Extension for image files (default: .jpg)')
    parser.add_argument('--combined-name', default='combined.txt',
                        help='Name for the concatenated text file (default: combined.txt)')
    parser.add_argument('--move', action='store_true',
                        help='Move files instead of copying them (default: copy)')
    
    args = parser.parse_args()
    
    organize_files_into_batches(
        source_dir=args.source_dir,
        batch_size=args.batch_size,
        folder_prefix=args.prefix,
        text_ext=args.text_ext,
        image_ext=args.image_ext,
        combined_name=args.combined_name,
        move_files=args.move
    )

if __name__ == "__main__":
    main()
