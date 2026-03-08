from pathlib import Path
from typing import BinaryIO


BASE_DIR = Path(__file__).resolve().parents[3]
UPLOAD_DIR = BASE_DIR / "data" / "uploads"


def ensure_upload_dir() -> None:
    """确保上传目录存在。"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_bytes_to_file(data: bytes, filename: str) -> Path:
    """将二进制内容保存到上传目录下的文件中。"""
    ensure_upload_dir()
    target = UPLOAD_DIR / filename
    with target.open("wb") as f:
        f.write(data)
    return target


def save_file_like(file_obj: BinaryIO, filename: str) -> Path:
    """保存类文件对象到上传目录。"""
    ensure_upload_dir()
    target = UPLOAD_DIR / filename
    with target.open("wb") as f:
        for chunk in iter(lambda: file_obj.read(4096), b""):
            f.write(chunk)
    return target

