#!/usr/bin/env python3
"""Assemble six ecommerce detail slices without cropping their heights."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps


def fit_canvas(image: Image.Image, size: tuple[int, int], fill: str) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGB")
    fitted = ImageOps.contain(image, size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, fill)
    x = (size[0] - fitted.width) // 2
    y = (size[1] - fitted.height) // 2
    canvas.paste(fitted, (x, y))
    return canvas


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGB")
    height = round(image.height * (width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def save_png_under(path: Path, image: Image.Image, max_kb: int | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=True)
    if max_kb is None or path.stat().st_size <= max_kb * 1024:
        return
    rgb = image.convert("RGB")
    for colors in [256, 192, 160, 128, 96, 64]:
        quantized = rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
        quantized.save(path, "PNG", optimize=True)
        if path.stat().st_size <= max_kb * 1024:
            return


def load_slices(paths: Iterable[str], width: int) -> list[Image.Image]:
    slices = []
    for raw in paths:
        p = Path(raw)
        if not p.exists():
            raise FileNotFoundError(p)
        with Image.open(p) as img:
            slices.append(resize_to_width(img, width))
    return slices


def stitch_vertical(slices: list[Image.Image], blank_height: int, fill: str) -> Image.Image:
    width = slices[0].width
    height = sum(img.height for img in slices) + blank_height
    long_img = Image.new("RGB", (width, height), fill)
    y = 0
    for img in slices:
        long_img.paste(img, (0, y))
        y += img.height
    return long_img


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modules", nargs="+", required=True, help="Six generated detail slice images in order.")
    parser.add_argument("--out-long", required=True, help="Output stitched complete detail page PNG.")
    parser.add_argument("--slice-dir", required=True, help="Directory for compressed detail slice PNGs.")
    parser.add_argument("--hero", help="Optional hero image to compress.")
    parser.add_argument("--hero-out", help="Optional compressed hero output path.")
    parser.add_argument("--slice-width", type=int, default=750, help="Common detail slice width. Heights are preserved proportionally.")
    parser.add_argument("--blank-height", type=int, default=0)
    parser.add_argument("--max-kb", type=int, default=500)
    parser.add_argument("--fill", default="#F8F5EF")
    args = parser.parse_args()

    if len(args.modules) != 6:
        raise SystemExit("Exactly six detail slice images are required.")

    slices = load_slices(args.modules, args.slice_width)
    slice_dir = Path(args.slice_dir)
    for idx, img in enumerate(slices, 1):
        save_png_under(slice_dir / f"详情页切片{idx:02d}.png", img, args.max_kb)

    long_img = stitch_vertical(slices, args.blank_height, args.fill)
    out_long = Path(args.out_long)
    save_png_under(out_long, long_img, None)

    if args.hero:
        hero_path = Path(args.hero)
        if not hero_path.exists():
            raise FileNotFoundError(hero_path)
        hero_out = Path(args.hero_out) if args.hero_out else hero_path.with_suffix(".jpg")
        with Image.open(hero_path) as hero:
            hero_img = fit_canvas(hero, (960, 540), args.fill)
        save_png_under(hero_out, hero_img, args.max_kb)


if __name__ == "__main__":
    main()
