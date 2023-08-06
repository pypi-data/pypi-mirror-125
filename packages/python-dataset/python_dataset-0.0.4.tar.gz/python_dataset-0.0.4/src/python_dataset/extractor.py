import pickle

import pathlib
from pathlib import Path

from typing import Generator

import shutil

from .wave import Wave


def iter_children(path: Path) -> Generator[int, None, None]:
    """path以下の構造をイテレーションする"""
    for i in path.iterdir():
        if i.is_dir():
            yield from iter_children(i)
        else:
            yield i


def extractor(folder_path: Path) -> None:

    # 初期値の設定
    wave_idx = None
    person_idx = None

    # 出力先の同一ディレクトリパス
    c_dir = Path(*folder_path.parts[:-1]) / ("ex_" + folder_path.parts[-1])

    for o_path in iter_children(folder_path):
        # 個別ファイルパス
        path = o_path.relative_to(folder_path)

        if path.suffix == ".wav":
            # wavの場合
            c_path = c_dir / path.with_suffix(".pkl")
            c_path.parent.mkdir(parents=True, exist_ok=True)

            # wave_nameとperson_nameの設定
            if wave_idx is None:
                [print(i, x) for i, x in enumerate(path.parts)]
                wave_idx = int(input("enter wave_name number: "))
                person_idx = int(input("enter person_name number: "))
            wave_name = path.parts[wave_idx]
            person_name = path.parts[person_idx]

            wav = Wave(
                wave_name=wave_name,
                person_name=person_name,
                path=path,
                folder_path=folder_path,
            )
            with open(c_path, "wb") as file:
                pickle.dump(wav, file)

        else:
            c_path = c_dir / path
            c_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(o_path, c_path)

    # 初期化
    wave_idx = None
    person_idx = None
