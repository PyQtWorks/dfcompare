from core.filecompare import DiffTwoSides
from core.foldercompare import FolderComparator
import logging

if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    comparator = FolderComparator('..\\tests\\leftdir', '..\\tests\\rightdir')
    comparator.rescan(False)
    comparator.print_result()

    # Compare files
    left_text = open('..\\tests\\file_compare\\left.txt').read()
    right_text = open('..\\tests\\file_compare\\right.txt').read()

    lines = DiffTwoSides(left_text.splitlines(1), right_text.splitlines(1))
    for line in lines:
        print(line)

