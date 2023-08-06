from ._hash_agent import HashAgent
from ._img import *
from ._dir import Dir
from ._file import File


class ImageResizerConfig:
    def __init__(self, src_dir, dest_dir, hash_dir=None):
        """ 이미지 압축기 환경설정
        :src_dir: 압축 대상 폴더입니다.
        :dest_dir: 압축된 이미지를 담을 폴더입니다.
        :hash_dir: 현재 압축 대상 폴더(src_dir)의 상태를 해싱하여 저장해두는 폴더. 입력 값이 없으면, 해싱 프로세스를 하지 않습니다.
        """
        self.STATIC = src_dir
        self.HASH_DIR = hash_dir
        self.COMP_DIR = dest_dir
        self.HASH_ON = True if hash_dir else False

        self.DIR_IGNORE = ["comp"]
        self.COMP_LIST = [
            CompressMethod("w", 0, 200),
            CompressMethod("h", 1, 400),
            CompressMethod("half", 2, 200),
        ]


class ImageResizer:
    def __init__(
        self,
        static,
        hash_dir,
        comp_dir,
    ):
        self.config = ImageResizerConfig(static, hash_dir, comp_dir)
        self.path_static = self.config.STATIC

    def add_method(self, dir_name: str, comp_type: int, target_size: int):
        """압축 형식 추가하기
        :dir_name: 압축 폴더 (기본 - comp)의 서브 디렉토리 이름입니다.
        해당 압축형식으로 압축되는 이미지는 해당 서브 디렉토리에 저장됩니다. 예 ) '/comp/w'
        :comp_type: 숫자로 표현되는 압축 타입
            지원되는 압축 타입:
                0 -> 넓이 기준 압축: 넓이가 target_size가 되도록 비율을 유지한 채 압축
                1 -> 높이 기준 압축: 높이가 target_size가 되도록 비율을 유지한 채 압축
                2 -> 퍼센트로 압축하기: 전체 크기를 기존 이미지 * target_size(0~1) 만큼 줄이는 방식으로 압축
        :target_size: 얼마나 줄일 것인가에 대한 정보, 압축타입 별로 의미하는 바가 달라짐
        """
        self.config.COMP_LIST.append(CompressMethod(dir_name, comp_type, target_size))

    def pop_method(self, name):
        """압축 형식의 이름으로 제거"""
        self.config.COMP_LIST[:] = [method for method in self.config.COMP_LIST if method.name != name]

    def pop_method_many(self, name_set):
        """압축 형식의 이름 Set 으로 제거"""
        self.config.COMP_LIST[:] = [method for method in self.config.COMP_LIST if method.name not in name_set]

    def perform(self):
        changed_list = self.get_changed_file_list()

        for src_file in changed_list:
            try:
                changed_img = Img(src_file.path)

                for method in self.config.COMP_LIST:
                    dest = Path(f"{self.config.COMP_DIR}/{method.name}/")
                    dest_folder = self.get_dest_folder_path(src_file.parent, dest)
                    changed_img.compress_img_to(dest_folder, method)

            except UnsupportedExtensionError:
                pass

            if self.config.HASH_ON:
                hash_folder = self.get_dest_folder_path(src_file.parent, self.config.HASH_DIR)
                hash_file = hash_folder / src_file.name
                HashAgent.hash_src_save_to_dest(src_file.path, hash_file)

    def get_changed_file_list(self):
        static_dir = Dir(self.path_static)
        result = []
        for folder, dirs, files in static_dir.traverse(self.config.DIR_IGNORE):
            if self.config.HASH_ON:
                reference_folder = self.get_dest_folder_path(
                    folder, self.config.HASH_DIR
                )
                for file_name in files:
                    ref_hash = File(reference_folder / file_name).get_content(
                        mode="r", read_or_create=True
                    )
                    target = Path(folder) / file_name
                    if HashAgent.is_changed(target, ref_hash):
                        result.append(File(target))
            else:
                for file_name in files:
                    target = Path(folder) / file_name
                    result.append(File(target))

        return result

    def get_dest_folder_path(self, folder: Path, dest_folder: Path):
        dest_dir = dest_folder / folder.relative_to(self.path_static)
        if not dest_dir.exists():
            dest_dir.mkdir()
        return dest_dir
