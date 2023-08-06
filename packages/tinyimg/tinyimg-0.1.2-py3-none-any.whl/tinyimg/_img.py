from dataclasses import dataclass
from pathlib import Path

from PIL import Image
import PIL

from ._file import File


class UnsupportedExtensionError(Exception):
    pass


@dataclass
class CompressMethod:
    name: str
    fix_side: int  # width: 0, height: 1, ratio: 2
    target_scale: int


class Img(File):
    W = 0
    H = 1
    RELY_ON_RATIO = 2

    def __init__(self, src: Path):
        super().__init__(src)
        self.img = src
        self.support_ext = {""}
        self.ext = self.get_extension()
        self.image = Image.open(self.img)

    def compress_img_to(self, dest_folder: Path, comp_method: CompressMethod):
        filename = self.image.filename.split("/")[-1]
        fix_side = comp_method.fix_side
        target_scale = comp_method.target_scale

        if fix_side == self.RELY_ON_RATIO:
            fix_side = self.W
            target_scale = self._get_size(fix_side, target_scale)

        im = self.get_resized_img(fix_side, target_scale)
        im.save(dest_folder / filename, self.ext.upper())

    def get_resized_img(self, fixed_side, fixed_scale):
        """비율 유지 이미지 압축
        fixed_side -> 0: width, 1: height
        """
        W = self.W
        H = self.H
        opposite_side = {W: H, H: W}[fixed_side]

        size = {W: self.image.size[W], H: self.image.size[H]}

        scale_percent = fixed_scale / float(size[fixed_side])
        variable_scale = int((float(size[opposite_side]) * float(scale_percent)))

        if size[fixed_side] > fixed_scale and size[opposite_side] > variable_scale:
            size[fixed_side] = fixed_scale
            size[opposite_side] = variable_scale

        image = self.image.resize((size[W], size[H]), PIL.Image.NEAREST)

        return image

    def _get_size(self, side, rank):
        return self.image.size[side] * rank

    def get_extension(self):
        ext = super().get_extension()

        if ext == "jpg":
            ext = "jpeg"

        if ext not in ["png", "jpeg"]:
            raise UnsupportedExtensionError("지원되지 않는 이미지" "")

        return ext
