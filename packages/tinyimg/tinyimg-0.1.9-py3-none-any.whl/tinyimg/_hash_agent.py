import hashlib
from pathlib import Path
from ._file import File


class HashAgent:
    @classmethod
    def is_changed(cls, path, hash_val):
        return cls.hash_file(path) != hash_val

    @classmethod
    def hash_file(cls, path: Path):
        hasher = hashlib.sha1()
        content = File(path).get_content()
        hasher.update(content)
        return hasher.hexdigest()

    @classmethod
    def hash_src_save_to_dest(cls, src: Path, dest: Path):
        """예상: dest가 반드시 존재합니다."""
        result = cls.hash_file(src)
        File(dest).save_content(result)
