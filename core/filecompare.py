import difflib


class DiffType:
    EQUAL = 0,
    LEFT_ONLY = 1,
    RIGHT_ONLY = 2,
    CHANGED = 3


class DiffTwoSides:
    def __init__(self, text_left, text_right):
        self.__text_left = text_left
        self.__text_right = text_right
        self.__diff_line = 0
        self.__text_line = 1
        self.__diff = list(difflib.ndiff(text_left, text_right))
        for i in self.__diff:
            print(i)

    def __iter__(self):
        return self

    def __next__(self):

        # check eof
        if self.__diff_line >= len(self.__diff):
            raise StopIteration

        result = {}
        diff_line = self.__diff[self.__diff_line]
        code = diff_line[:2]
        line = diff_line[2:]
        result['line_num'] = self.__text_line
        result['line'] = line
        if code == '  ':
            result['code'] = DiffType.EQUAL
        elif code == '+ ':
            result['code'] = DiffType.RIGHT_ONLY
        elif code == '- ':
            changed_lines = self._change_block_handler(self.__diff_line)
            if not changed_lines:
                result['code'] = DiffType.LEFT_ONLY
            else:
                result['code'] = DiffType.CHANGED
                result['left_changes'] = changed_lines['left'] if 'left' in changed_lines else None
                result['right_changes'] = changed_lines['right'] if 'right' in changed_lines else None
                result['new_line'] = changed_lines['new_line']
                self.__diff_line += changed_lines['skipped']
        self.__diff_line += 1
        self.__text_line += 1
        return result

    def _change_block_handler(self, line):
        # Get four lines
        lines = []
        for i in range(line, line + 4):
            lines += [self.__diff[i] if i < len(self.__diff) else None]
        changes = {}
        # case (-, ?, +, ?)
        if lines[0] and lines[0][:2] == '- ' and \
                lines[1] and lines[1][:2] == '? ' and \
                lines[2] and lines[2][:2] == '+ ' and \
                lines[3] and lines[3][:2] == '? ':
            changes['left'] = [i for (i, c) in enumerate(lines[1][2:]) if c in ['-', '^']]
            changes['right'] = [i for (i, c) in enumerate(lines[3][2:]) if c in ['+', '^']]
            changes['new_line'] = lines[2][2:]
            changes['skipped'] = 3
        # case (-, +, ?)
        elif lines[0] and lines[0][:2] == '- ' and \
                lines[1] and lines[1][:2] == '+ ' and \
                lines[2] and lines[2][:2] == '? ':
            changes['left'] = []
            changes['right'] = [i for (i, c) in enumerate(lines[2][2:]) if c in ['+', '^']]
            changes['new_line'] = lines[1][2:]
            changes['skipped'] = 2
            pass
        # case (-, ?, +)
        elif lines[0] and lines[0][:2] == '- ' and \
                lines[1] and lines[1][:2] == '? ' and \
                lines[2] and lines[2][:2] == '+ ':
            changes['left'] = [i for (i, c) in enumerate(lines[1][2:]) if c in ['-', '^']]
            changes['right'] = []
            changes['new_line'] = lines[2][2:]
            changes['skipped'] = 2
        # No changes
        else:
            return None
        # Changes is detected
        return changes
