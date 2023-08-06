#!/usr/bin/env python3

import glob
import os
import struct
from collections import deque
from dataclasses import asdict, dataclass, replace
from itertools import chain
from typing import Deque, Iterable, Iterator, List, Optional, Sequence, Set

import numpy as np
from PIL import Image

from nutcracker.codex.codex import get_encoder
from nutcracker.graphics.image import ImagePosition
from nutcracker.kernel.element import Element
from nutcracker.smush import ahdr, anim, fobj
from nutcracker.smush.preset import smush
from nutcracker.utils.fileio import write_file

UINT16LE = struct.Struct('<H')


@dataclass(frozen=True)
class FrameGenCtx(object):
    idx: int
    frame: Optional[Element] = None
    seq_ind: Optional[int] = None


def convert_fobj_meta(datam: bytes) -> int:
    meta, data = fobj.unobj(datam)
    if meta.codec == 47:
        return UINT16LE.unpack(data[:2])[0]
    elif meta.codec == 37:
        return UINT16LE.unpack(data[2:4])[0]
    return 0


def decode_frame(header: ahdr.AnimationHeader, idx: int, frame: Element) -> FrameGenCtx:
    ctx = FrameGenCtx(idx=idx, frame=frame)
    for comp in frame.children:
        if comp.tag == 'FOBJ':
            decoded = convert_fobj_meta(comp.data)
            ctx = replace(ctx, seq_ind=decoded)
        elif comp.tag == 'ZFOB':
            data = fobj.decompress(comp.data)
            decoded = convert_fobj_meta(data)
            ctx = replace(ctx, seq_ind=decoded)
    return ctx


def get_sequence_frames(
    header: ahdr.AnimationHeader,
    frames: Iterator[FrameGenCtx],
    saved: Deque[FrameGenCtx],
) -> Iterator[FrameGenCtx]:
    assert not saved
    for frame in frames:
        if frame.seq_ind == 0:
            saved.append(frame)
            break
        yield frame


def get_frame_image(directory: str, idx: int) -> Sequence[Sequence[int]]:
    im = Image.open(os.path.join(directory, f'FRME_{idx:05d}.png'))
    return list(np.asarray(im))


def encode_fake(image: Sequence[Sequence[int]], chunk: bytes) -> bytes:
    meta = fobj.unobj(chunk).header
    codec = meta.codec
    if codec == 1:
        return chunk
    encode = get_encoder(codec)
    loc = ImagePosition(x1=0, y1=0, x2=len(image[0]), y2=len(image))
    meta = fobj.FrameObjectHeader(codec=codec, **asdict(loc))
    print('CODEC', meta)
    encoded = encode(image)
    return fobj.mkobj(meta, encoded)


def encode_seq(sequence: Iterable[FrameGenCtx], directory: str) -> Iterator[bytes]:
    for frame in sequence:
        fdata: List[bytes] = []
        for comp in frame.frame:
            if comp.tag == 'ZFOB':
                screen = get_frame_image(directory, frame.idx)
                encoded = encode_fake(screen, fobj.decompress(comp.data))
                fdata += [smush.mktag('ZFOB', fobj.compress(encoded))]
            elif comp.tag == 'FOBJ':
                screen = get_frame_image(directory, frame.idx)
                fdata += [smush.mktag('FOBJ', encode_fake(screen, comp.data))]
            else:
                fdata += [smush.mktag(comp.tag, comp.data)]
        yield smush.write_chunks(fdata)


def split_sequences(
    header: ahdr.AnimationHeader,
    frames: Iterable[Element],
) -> Iterator[Iterator[FrameGenCtx]]:
    saved = deque(maxlen=1)
    frames = (decode_frame(header, idx, frame) for idx, frame in enumerate(frames))
    saved.append(next(frames))
    while saved:
        frame = saved.pop()
        assert frame.seq_ind == 0, frame.seq_ind
        it = chain([frame], get_sequence_frames(header, frames, saved))
        yield it
        # Consume iterator
        for _ in it:
            pass


def check_dirty(frame_range: Iterable[int], files: Set[str]) -> bool:
    return any(f'FRME_{num:05d}.png' in files for num in frame_range)


def replace_dirty_sequences(
    header: ahdr.AnimationHeader,
    frames: Iterable[Element],
    directory: str,
) -> Iterator[bytes]:
    # split frames to sequences
    # for frames in each sequence (range?)
    # if any of the frame images in the sequence exists in parameter
    # re-encode sequence
    # yield each frame
    files = {
        os.path.basename(file) for file in glob.iglob(os.path.join(directory, '*.png'))
    }
    for sequence in split_sequences(header, frames):
        seq = list(sequence)
        frame_range = range(seq[0].idx, 1 + seq[-1].idx)
        dirty = check_dirty(frame_range, files)
        if dirty:
            yield from encode_seq(seq, directory)
        else:
            yield from (frame.frame.data for frame in seq)


def encode_san(root: Element, directory: str) -> bytes:
    header, frames = anim.parse(root)
    frames = replace_dirty_sequences(header, frames, directory)
    return anim.compose(header, (smush.mktag('FRME', frame) for frame in frames))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='read smush file')
    parser.add_argument('filename', help='filename to read from')
    args = parser.parse_args()

    root = anim.from_path(args.filename)
    write_file(
        'NEW_VIDEO2.SAN',
        encode_san(root, os.path.join('out', os.path.basename(args.filename))),
    )
    # assert encode_san(
    #     root, os.path.join('out', os.path.basename(args.filename))
    # ) == read_file(args.filename)

    print('ALL OK')
