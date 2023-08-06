from pathlib import Path


class File:
    BLOCK_SIZE = 65536

    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.parent = (path / "..").resolve()

    def get_content(self, mode="rb", read_or_create=False):
        """파일에서 값 가지고 오기
        mode는 r이나 rb로 하지 않으면 어떻게 될 지 잘모릅니다.
        """
        if read_or_create:
            mode = mode if self.path.exists() else "w+"
        else:
            mode = mode

        buf_list = [b""]
        result = None
        with self.path.open(mode) as file:
            if mode == "r":
                result = file.read()
            else:
                buf = file.read(self.BLOCK_SIZE)
                while buf:
                    buf_list.append(buf)
                    buf = file.read(self.BLOCK_SIZE)

        result = result if result else b"".join(buf_list)
        return result

    def save_content(self, content):
        with self.path.open(mode="w") as f:
            f.write(content)

    def get_extension(self):
        ext = self.path.suffix.replace(".", "")
        return ext
