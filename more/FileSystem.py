class FileSystem:
    def __init__(self):
        self.root = {"type": "dir", "children": {}}

    def create_file(self, path, size):
        dirs = path.split("/")
        current = self.root
        for dir in dirs[:-1]:
            if dir not in current["children"]:
                current["children"][dir] = {"type": "dir", "children": {}}
            current = current["children"][dir]
        filename = dirs[-1]
        current["children"][filename] = {"type": "file", "size": size, "data": bytearray(size)}

    def read_file(self, path):
        dirs = path.split("/")
        current = self.root
        for dir in dirs:
            if dir not in current["children"]:
                raise FileNotFoundError(f"File not found: {path}")
            current = current["children"][dir]
        if current["type"] != "file":
            raise IsADirectoryError(f"Path is a directory: {path}")
        return current["data"]

    def write_file(self, path, data):
        dirs = path.split("/")
        current = self.root
        for dir in dirs[:-1]:
            if dir not in current["children"]:
                raise FileNotFoundError(f"Directory not found: {path}")
            current = current["children"][dir]
        filename = dirs[-1]
        if filename not in current["children"]:
            raise FileNotFoundError(f"File not found: {path}")
        current["children"][filename]["data"] = data