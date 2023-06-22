import io


class Source:
    EOL = ['\n', '\r']

    def __init__(self, stream) -> None:
        self.stream = stream
        self.column = 0
        self.line = 1
        self.current_char = self.get_next_char()

    def __del__(self) -> None:
        if hasattr(self, 'stream') and self.stream:
            self.stream.close()

    def get_current_char(self) -> str:
        return self.current_char

    def get_next_char(self) -> str:
        self.current_char = self.stream.read(1)
        if self.current_char != '':
            self.column += 1
        if self.current_char in self.EOL:
            self.line += 1
            self.column = 0
        return self.current_char

    def get_position(self) -> tuple:
        return (self.column, self.line)

    def set_start_position(self) -> None:
        self.column = 0
        self.line = 1
        self.stream.seek(0)
        self.current_char = self.get_next_char()

    def get_line(self, line) -> str:
        current_position = self.stream.tell()
        self.stream.seek(0)
        for _ in range(line - 1):
            self.stream.readline()
        readed_line = self.stream.readline()
        self.stream.seek(current_position)
        return readed_line

    def seek_next(self) -> str:
        current_position = self.stream.tell()
        self.get_next_char()
        next_char = self.get_current_char()
        self.stream.seek(current_position)
        return next_char


class FileSource(Source):
    def __init__(self, path: str) -> None:
        super().__init__(open(path, 'r'))
        self.path = path


class StringSource(Source):
    def __init__(self, string: str) -> None:
        super().__init__(io.StringIO(string))
