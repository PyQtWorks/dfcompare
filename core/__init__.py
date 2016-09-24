from core.foldercompare import FolderComparator
import logging

if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    comparator = FolderComparator('..\\tests\\leftdir', '..\\tests\\rightdir')
    comparator.rescan(False)
    comparator.print_result()

