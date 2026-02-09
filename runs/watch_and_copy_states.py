#!/usr/bin/env python3
"""
VDM State File Watcher
Monitors a directory for new state_*.h5 files and copies them to a backup location.
"""

import os
import sys
import time
import shutil
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('state_watcher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class StateFileHandler(FileSystemEventHandler):
    """
    Handles file system events for state files.
    """
    
    def __init__(self, dest_dir, wait_stable=2.0, pattern='state_*.h5'):
        """
        Args:
            dest_dir: Destination directory for copied files
            wait_stable: Seconds to wait for file to stabilize before copying
            pattern: Glob pattern for files to watch (default: state_*.h5)
        """
        self.dest_dir = Path(dest_dir)
        self.dest_dir.mkdir(parents=True, exist_ok=True)
        self.wait_stable = wait_stable
        self.pattern = pattern
        self.processed_files = set()  # Track already-copied files
        
        logger.info(f"Initialized watcher: destination={dest_dir}, pattern={pattern}")
    
    def _matches_pattern(self, filename):
        """Check if filename matches our pattern."""
        from fnmatch import fnmatch
        return fnmatch(filename, self.pattern)
    
    def _wait_for_stable_file(self, filepath):
        """
        Wait for file to finish writing by checking if size stabilizes.
        Returns True if file is stable, False if it disappears or errors occur.
        """
        try:
            prev_size = -1
            curr_size = os.path.getsize(filepath)
            
            while prev_size != curr_size:
                time.sleep(self.wait_stable)
                prev_size = curr_size
                
                if not os.path.exists(filepath):
                    logger.warning(f"File disappeared while waiting: {filepath}")
                    return False
                
                curr_size = os.path.getsize(filepath)
            
            return True
            
        except Exception as e:
            logger.error(f"Error waiting for stable file {filepath}: {e}")
            return False
    
    def _copy_file_safe(self, src_path, dest_path):
        """
        Safely copy file with verification.
        Returns True on success, False on failure.
        """
        try:
            # Copy file
            shutil.copy2(src_path, dest_path)
            
            # Verify copy by comparing sizes
            src_size = os.path.getsize(src_path)
            dest_size = os.path.getsize(dest_path)
            
            if src_size != dest_size:
                logger.error(f"Size mismatch after copy: {src_path} ({src_size}) vs {dest_path} ({dest_size})")
                os.remove(dest_path)  # Remove corrupted copy
                return False
            
            logger.info(f"✓ Copied: {os.path.basename(src_path)} ({src_size:,} bytes)")
            return True
            
        except Exception as e:
            logger.error(f"Error copying {src_path} to {dest_path}: {e}")
            return False
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        filename = filepath.name
        
        # Check if this matches our pattern
        if not self._matches_pattern(filename):
            return
        
        # Skip if already processed
        if str(filepath) in self.processed_files:
            return
        
        logger.info(f"Detected new file: {filename}")
        
        # Wait for file to finish writing
        if not self._wait_for_stable_file(filepath):
            return
        
        # Copy to destination
        dest_path = self.dest_dir / filename
        
        # Skip if destination already exists with same size
        if dest_path.exists():
            if os.path.getsize(dest_path) == os.path.getsize(filepath):
                logger.info(f"Skipping (already exists): {filename}")
                self.processed_files.add(str(filepath))
                return
        
        # Perform the copy
        if self._copy_file_safe(filepath, dest_path):
            self.processed_files.add(str(filepath))
        else:
            logger.warning(f"Failed to copy: {filename}")
    
    def on_modified(self, event):
        """
        Handle file modification events.
        Some systems trigger 'modified' instead of 'created' for new files.
        """
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        filename = filepath.name
        
        # Only process if it matches pattern and hasn't been processed yet
        if self._matches_pattern(filename) and str(filepath) not in self.processed_files:
            self.on_created(event)


def scan_existing_files(watch_dir, dest_dir, pattern='state_*.h5'):
    """
    Scan for existing files that match the pattern and copy any missing ones.
    This handles files that already existed before the watcher started.
    """
    watch_path = Path(watch_dir)
    dest_path = Path(dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Scanning for existing {pattern} files in {watch_dir}...")
    
    copied_count = 0
    skipped_count = 0
    
    for src_file in watch_path.glob(pattern):
        dest_file = dest_path / src_file.name
        
        # Skip if destination exists with same size
        if dest_file.exists():
            if os.path.getsize(dest_file) == os.path.getsize(src_file):
                skipped_count += 1
                continue
        
        # Copy the file
        try:
            shutil.copy2(src_file, dest_file)
            src_size = os.path.getsize(src_file)
            dest_size = os.path.getsize(dest_file)
            
            if src_size == dest_size:
                logger.info(f"✓ Copied existing: {src_file.name} ({src_size:,} bytes)")
                copied_count += 1
            else:
                logger.error(f"Size mismatch: {src_file.name}")
                os.remove(dest_file)
        
        except Exception as e:
            logger.error(f"Error copying {src_file.name}: {e}")
    
    logger.info(f"Existing files: {copied_count} copied, {skipped_count} skipped")


def main():
    parser = argparse.ArgumentParser(
        description='Watch directory for new state_*.h5 files and copy them to backup location'
    )
    parser.add_argument(
        'watch_dir',
        help='Directory to watch for new state files'
    )
    parser.add_argument(
        'dest_dir',
        help='Destination directory for copied files'
    )
    parser.add_argument(
        '--pattern',
        default='state_*.h5',
        help='File pattern to watch (default: state_*.h5)'
    )
    parser.add_argument(
        '--wait',
        type=float,
        default=2.0,
        help='Seconds to wait for file stabilization (default: 2.0)'
    )
    parser.add_argument(
        '--no-scan',
        action='store_true',
        help='Skip scanning for existing files on startup'
    )
    
    args = parser.parse_args()
    
    # Validate directories
    watch_path = Path(args.watch_dir)
    if not watch_path.exists():
        logger.error(f"Watch directory does not exist: {args.watch_dir}")
        sys.exit(1)
    
    if not watch_path.is_dir():
        logger.error(f"Watch path is not a directory: {args.watch_dir}")
        sys.exit(1)
    
    # Create destination if needed
    dest_path = Path(args.dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    logger.info("=" * 80)
    logger.info("VDM STATE FILE WATCHER")
    logger.info("=" * 80)
    logger.info(f"Watch directory: {watch_path.absolute()}")
    logger.info(f"Destination:     {dest_path.absolute()}")
    logger.info(f"Pattern:         {args.pattern}")
    logger.info(f"Stabilization:   {args.wait}s")
    logger.info("=" * 80)
    
    # Scan for existing files first
    if not args.no_scan:
        scan_existing_files(watch_path, dest_path, args.pattern)
    
    # Set up the file watcher
    event_handler = StateFileHandler(
        dest_dir=dest_path,
        wait_stable=args.wait,
        pattern=args.pattern
    )
    
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)
    observer.start()
    
    logger.info("Watching for new files... (Press Ctrl+C to stop)")
    
    try:
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("\nStopping watcher...")
        observer.stop()
    
    observer.join()
    logger.info("Watcher stopped.")


if __name__ == '__main__':
    main()
