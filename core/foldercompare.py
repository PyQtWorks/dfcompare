import os
import hashlib
import logging


class FolderNotExistsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FolderComparator(object):
    def __init__(self, left_dir, right_dir):
        self.left_tree = {}
        self.right_tree = {}
        self.left_dir = left_dir
        self.right_dir = right_dir
        self.rescan()

    def rescan(self, fast=True):
        self.left_tree = self._scan_dir(self.left_dir, fast)
        self.right_tree = self._scan_dir(self.right_dir, fast)

    def get_tries(self):
        return self.left_tree, self.right_tree

    def get_root_dirs(self):
        return self.left_dir, self.right_dir

    def print_result(self):
        """

        :return:
        """
        diff = {}
        for file, file_hash in sorted(self.left_tree.items()):
            # Find new files and updated
            if file in self.right_tree.keys():
                if file_hash != self.right_tree[file]:
                    # File is present in right side
                    diff[file] = 'U'
                else:
                    # TODO: compare more deeper?
                    diff[file] = '='
            else:
                diff[file] = '+'

        for file, file_hash in sorted(self.right_tree.items()):
            # Find removed files
            if file not in self.left_tree.keys():
                diff[file] = '-'
        for filename, status in sorted(diff.items()):
            print('[%s] %s' % (filename, status))

    def _calc_hash(self, path, filename, fast=True):
        """calculate sha1 of file"""
        full_path = os.path.join(path, filename)
        if not fast:
            with open(full_path, 'rb') as f:
                content = f.read()
            f.close()
            hash_data = hashlib.sha1(content).hexdigest()
        else:
            info = os.stat(full_path)
            content = str(info.st_mtime) + str(info.st_size)
            hash_data = hashlib.sha1(content.encode('utf-8')).hexdigest()
        logging.debug('Hash of %s is %s', full_path, str(hash_data))
        return hash_data

    def _dir_snapshot(self, root_dir, fast):
        """Perform recursive scan of folder and calculate fast hash of every file"""
        logging.debug('directory %s scanning...', root_dir)
        file_hash = {}
        for base, dirs, files in os.walk(root_dir):
            for filename in files:
                # Remove only first occurrence of root directory
                path_inside = base.replace(root_dir, '', 1)
                # Add path + sha1 to hash table
                file_hash[os.path.join(path_inside, filename)] = self._calc_hash(base, filename, fast)

        # TODO: save snapshot
        return file_hash

    def _scan_dir(self, root_dir, fast=True):
        if not os.path.exists(root_dir):
            raise FolderNotExistsException('Folder %s not found' % root_dir)

        logging.info('scan directory: %s' % root_dir)
        file_hash = {}
        # TODO: load snapshot
        file_hash = self._dir_snapshot(root_dir, fast)
        return file_hash

