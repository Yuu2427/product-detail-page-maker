---
name: ecommerce-gpt-image2-pdp-high-fidelity
description: Generate high-fidelity Chinese ecommerce product hero images and six sequential detail-page slices with GPT Image 2 for real merchandise. Use when product photos, 商品头图, 商品主图, 详情页长图, 批量生图, 卖点梳理, 商品参数表, 银发群体商品, 商品细节大图, 人物使用场景, 小于500KB压缩, or strict product fidelity is required. The skill preserves the exact product appearance, logo, packaging text, bottle label, printed copy, colors, shape, buttons, accessories, and visible product details from the source photo while generating one 960x540 hero image, six separate detail slices, a stitched complete detail page, and compressed delivery files after user confirmation.
---

# Ecommerce GPT Image 2 PDP High Fidelity

## Fixed Delivery Contract

For one product, the required output is exactly:

- One hero image: `960 x 540 px`.
- Six detail-page slice images: `01` to `06`, generated one by one. Each slice must be under `500KB` after delivery compression.
- One stitched complete detail page made after all six slices are generated and pass internal review.

Do not generate all images in one batch. Use this mandatory confirmation flow:

1. Generate the hero image, save it to the preview/output area, open the hero preview window, report the preview file path, and stop for explicit user approval.
2. After hero approval, generate detail slice `01`, open its preview window, report its file path, and stop for explicit approval of the detail-page direction.
3. After slice `01` is approved, generate detail slices `02` through `06` sequentially. Do not open a preview window or ask for confirmation after each of these slices. Continue automatically unless a slice fails the internal review requirements.
4. After all six slices pass internal review, stitch the complete detail page, open the complete-detail-page preview window, report its file path, summarize the six-slice sequence, and stop for final visual approval.

If any generated image changes the product, misses required content, repeats the same scene/viewpoint, or exceeds delivery constraints, stop that generation sequence and regenerate the failed image before moving on.

Only after the user approves the complete detail page, proactively ask for the product name, product code, and any special folder-naming requirement. If the user has no special requirement, create the final folder named:

```text
商品编码_商品名称
```

The final product folder must contain:

```text
商品名称_头图.png
商品名称_完整详情页.png
详情页切片01.png
详情页切片02.png
详情页切片03.png
详情页切片04.png
详情页切片05.png
详情页切片06.png
```

Do not create or rename the final product folder before the user approves the complete detail page and provides the required naming information.

## Runtime Environment Check

Handle the runtime check internally before starting the first product task in a new environment. Do not ask the user to run environment commands or explain Python/Pillow setup unless automatic setup fails.

1. Confirm that Python 3.10 or newer is available.
2. Install the dependencies from `requirements.txt` when they are missing.
3. Run `python scripts/check_environment.py` or the platform-equivalent Python command.
4. Do not claim that the workflow is ready until the environment check exits successfully.

The required local Python dependency is Pillow. Installing or copying the Skill directory alone does not install this runtime dependency.

If automatic setup fails, stop before image generation and give the user one concise failure reason. Do not silently skip the stitching or compression steps, and do not ask the user to decide whether to continue with an incomplete delivery workflow.

## Required Image Model

- Every image-generation and image-editing operation must use `gpt-image-2`.
- This is a mandatory requirement, not a default or preference.
- Confirm that `gpt-image-2` is available before generating the hero image.
- Never substitute or silently fall back to another image model.
- If `gpt-image-2` is unavailable or cannot be selected, stop before image generation and tell the user concisely.
- Planning, spreadsheet processing, compositing, stitching, compression, previewing, and file organization may use appropriate non-image tools.

## Required Input Collection

Before generating images, require a product information table and at least one real product photo. The product information table must help the user provide or complete:

- Product name and category.
- Real product photo path(s), photo angle(s), and which visual details must remain unchanged.
- Core selling points and user-facing copy.
- Basic parameters: size/capacity/specification, material, color, thickness/weight when relevant.
- Product details to show: at least two different close-up targets, such as texture, handle, label, opening, button, interface, edge, inside/outside structure, packaging, or accessory.
- Use scenarios and scene props.
- Cleaning, maintenance, storage, safety tips, contraindications, or use steps when relevant.
- Unsupported or unknown fields that must not be invented.

If the user provides only one photo and partial information, first help complete a draft selling-point and image plan from the available evidence. Then clearly list missing fields that need user confirmation. Do not start image generation until the minimum fields are sufficiently clear for faithful output.

Minimum fields before generation:

- Product name or temporary product name.
- Product category.
- At least one source photo.
- 3-5 supported selling points.
- Material/color/size or a clear statement that these are unknown and must not appear in generated copy.
- Two detail close-up targets.
- One specs/usage/safety/maintenance section.

## Product Information Table Maintenance

Use one fixed selling-point/product-information workbook for ongoing calls. Do not create a new Excel workbook every time product information is adjusted unless the user explicitly asks for a versioned copy, backup, or separate deliverable.

Default fixed workbook:

```text
商品详情页生成表.xlsx
```

When a user provides new or corrected product information:

- Update the matching product row in the fixed workbook when the product already exists.
- Add a new row in the fixed workbook when the product does not exist.
- Keep user-supplied facts, inferred safe fields, missing-field notes, and "do not invent" constraints in that same row.
- Do not generate a separate `v1.2`, `v1.3`, or product-specific workbook for ordinary information updates.
- If the fixed workbook path changes, follow the user-specified workbook as the new fixed source for subsequent calls.

## Core Rule

Product truth comes first. The product itself is not a design suggestion.

Preserve exactly:

- Product shape, color, material, proportions, ports, buttons, straps, caps, labels, packaging layout, and visible accessories.
- Product-owned copy such as logo, bottle labels, box text, printed slogans, capacity text, English/Chinese label text, and package graphics.
- Any real wording already printed on the product or package. Do not translate, rewrite, simplify, remove, replace, or hallucinate it.

Generate or adjust only:

- Background, lighting, atmosphere, props, people usage scenes, supporting scene elements, graphic callouts, ecommerce layout, and added marketing copy outside the product.

## Workflow

1. Read the fixed user table and image folder. Match each row to its product image. If product name conflicts with the image, prioritize the image and flag the mismatch.
2. For each product, identify whether the source is a clean product photo or a marketplace/app screenshot.
3. If the source is a screenshot, use only the physical product area. Ignore app UI, status bar, IDs, price, exchange count, promo labels, page cards, and unrelated screenshot text.
4. Use `product_fidelity: exact_product` by default.
5. Generate the fixed delivery set: one `960 x 540 px` hero image plus six detail-page slices.
6. For exact product fidelity, prefer this production method when available:
   - Generate background/layout and text-safe areas with `gpt-image-2`.
   - Keep the original product photo/crop as the product layer.
   - Composite the original product layer into the generated layout when exact label/package text matters.
7. Follow the mandatory preview gates: hero approval, slice `01` direction approval, automatic generation of slices `02` through `06`, then complete-detail-page approval.
8. When using `gpt-image-2` edits directly, include strict prompt language that the product and product-owned text must remain unchanged. Reject outputs that alter label text, logo, package copy, buttons, colors, or packaging structure.
9. Save temporary outputs with clear filenames. Open previews only for the hero, detail slice `01`, and the stitched complete detail page by default. Ask for final naming information only after the complete-detail-page approval.

## Defaults

- Required image model: `gpt-image-2`. This is mandatory and cannot be replaced by another image model.
- Hero size: `960x540`.
- Detail slices: exactly 6 standalone vertical posters. Generate one slice at a time and keep final delivery slices as PNG. Compress each final delivery slice under `500KB` when possible without changing the layout.
- Detail long image: stitch the 6 internally reviewed slices vertically into a true long detail page PNG, then request approval of the complete page.
- Audience: 中老年银发群体 unless the user says otherwise.
- Style: warm, clear, trustworthy, practical, large readable Chinese text, simple hierarchy, low visual noise.
- Hero image: product-first composition, simple headline/subheadline, no dense text.
- Detail page: richer than a standard PDP; include product overview, selling-point scenes, product close-up modules, basic information, specs, and usage or necessary safety notes. Build it from six individual slices rather than one monolithic generated image.
- Delivery format: PNG only by default. Export every detail-page slice as PNG under `500KB` when possible without changing the layout. Do not create duplicate JPG files unless the user explicitly asks for them.
- Prohibited promotional wording unless explicitly supplied: 优惠、折扣、赠礼、低价、秒杀、限时、福利、临期特惠、热门兑换.
- For health-adjacent products, avoid medical claims such as 治疗、止痛、祛湿、抗炎、改善疾病、疗效、医用、认证.

## Six-Slice Detail Page Structure

Use this exact six-slice structure for enriched detail pages. Each item must be generated as one separate vertical image and internally reviewed. After slice `01` direction approval, slices `02` through `06` do not require individual user confirmation; stack all six and request approval of the complete page:

1. 详情页切片01 - 商品总览与核心卖点: large exact product view, product name if provided, one short value proposition, and 2-3 strongest supported selling points.
2. 详情页切片02 - 使用场景与卖点呈现: a practical lifestyle scene with changed camera angle/framing from the hero, showing how the product is used.
3. 详情页切片03 - 细节展示一: close-up from a specific angle showing product detail, material, texture, label, opening, handle, button, interface, or packaging. Preserve built-in text exactly.
4. 详情页切片04 - 细节展示二: a different detail and different angle from slice 03. Avoid repeating the same crop or front-view product display.
5. 详情页切片05 - 商品基本信息: readable basic information such as size, material, color, thickness, weight, capacity, included accessories, or structure. Use only supported fields. Unknown fields must be omitted or marked as not supplied in the planning table, never invented.
6. 详情页切片06 - 参数/使用注意事项: product parameters, cleaning, maintenance, storage, safety tips, contraindications, or use steps. Keep the bottom safe area uncropped and text fully visible.

Do not make every slice the same card. Vary scenes, camera distance, angle, orientation, crop scale, and layout type. The six slices must collectively show product characteristics more fully than one repeated studio view: front/side/top/bottom/inside/use-in-hand/detail texture as applicable. Do not place two slices side by side. The final long image should look like full-width posters stitched top-to-bottom.

## Visual Variety Rules

Use the reference effect only as a style-quality target: warm natural light, clean home/kitchen/lifestyle atmosphere, large readable Chinese text, soft shadows, whitespace, product-first composition, and detail callouts. Do not quote, copy, reuse, or depend on any reference image or reference asset.

Across the hero and six detail slices:

- Change scene or viewpoint on every image.
- Include at least one clean studio/product overview.
- Include at least one real use scene.
- Include two different close-up detail images.
- Include one information/specification layout.
- Include one usage, cleaning, maintenance, storage, or safety layout.
- Avoid repeating the same front-view product shot more than twice.
- Avoid abstract backgrounds when a real product scenario is needed.

## Product Logic Check

Before generating any use-scene, operation-detail, step, or caution slice, identify the product's real use logic from the product photo, supplied facts, and common mechanical constraints. Treat operation direction, hand position, force point, opening direction, and contact point as product-truth constraints.

For kitchen hand tools:

- Do not invent impossible hand positions, reversed directions, or decorative gestures that do not operate the product.
- Show the product in its real use orientation. For a spice grinder, the grinder mouth faces downward toward the food, and the user holds/rotates the metal top section to grind.
- Do not show fingers prying, picking, or pressing a small adjustment knob when the real action is rotating the metal grinder top.
- Do not repeat the same "front upright product plus text" view across detail slices. Use operation-in-hand, top/underside/detail, side macro, exploded/structure, step sequence, storage/tabletop, or parameter layout as appropriate.
- Do not default to cleaning/maintenance sections for simple kitchen tools. Include cleaning/maintenance only when supplied by the user or genuinely necessary for safe use. Otherwise use concise operation steps and practical cautions.
- Remove repeated information across slices. Each slice must have a distinct job: scenario, operation, material/detail, structure/parameter, or steps/cautions.
- Do not put internal missing-field notes in customer-facing detail-page images. Phrases such as "未提供重量", "不作展示", "信息未提供", "未知参数", or similar audit notes belong in the final user-facing work summary, not in ecommerce images.
- Do not force numbered step blocks into every operation-detail slice. Use numbered steps only when the slice topic is explicitly a usage-step slice. For detail close-ups, use concise callouts that describe the visible structure or correct operation without adding inaccurate procedural claims.

## Stitching And Compression Workflow

Use this workflow when the user asks for a true super-long detail page or upload-ready slices:

1. Generate each detail slice separately and sequentially from `01` to `06`.
2. Save slice images in order.
3. Run [scripts/assemble_detail_modules.py](scripts/assemble_detail_modules.py) to:
   - scale each slice to the same width while preserving its proportional height,
   - stitch all six slices top-to-bottom without cropping slice height,
   - add a bottom blank area,
   - export each detail slice as PNG under `500KB` when possible,
   - optionally compress the hero image PNG under `500KB`.

Example:

```bash
python3 scripts/assemble_detail_modules.py \
  --modules 详情页切片01.png 详情页切片02.png 详情页切片03.png 详情页切片04.png 详情页切片05.png 详情页切片06.png \
  --out-long ./outputs/乳香精油_完整详情页.png \
  --slice-dir ./outputs/乳香精油_详情页切片_小于500KB \
  --hero ./outputs/乳香精油_头图.png \
  --blank-height 260
```

Default output is PNG. Do not export duplicate JPG/PNG pairs unless the user explicitly asks for multiple formats.

## Specification Block Rules

The specs block must be complete and readable.

- Put specs in an independent light-background panel at the bottom.
- Leave generous internal padding and a visible bottom safe margin.
- Use large readable text, short lines, and no overflowing text.
- Do not include brand or style in specs unless the user explicitly asks.
- Prefer useful safe fields: 品类、使用方式、使用场景、存储方式、注意事项.
- Do not invent dimensions, capacity, ingredients, power, Bluetooth version, shelf life, certification, warranty, treatment effects, or other unsupported parameters.
- If prior outputs crop the specs block, regenerate with fewer spec lines and explicit bottom safety margin.

## Prompt Requirements

Every prompt must include:

- "The product itself and all product-owned printed text must remain exactly as shown in the source photo."
- "Do not redraw, rewrite, translate, simplify, remove, replace, or hallucinate the product label, logo, box text, bottle text, package graphics, or visible product copy."
- "Only generate the surrounding ecommerce scene, background, layout, props, callouts, people usage scenes, and added marketing copy outside the product."
- "The specs block must be fully visible, not cropped, not close to the canvas edge, and all text must fit."

### Fidelity Block

Use this block in every GPT Image 2 prompt:

```text
Use the source photo as the exact product reference.
The product itself and all product-owned printed text must remain exactly as shown in the source photo.
Do not redraw, rewrite, translate, simplify, remove, replace, or hallucinate the product label, logo, box text, bottle text, package graphics, visible capacity text, buttons, ports, colors, shape, material, strap, cap, or accessories.
Only generate the surrounding ecommerce scene, background, layout, props, callouts, people usage scenes, and added marketing copy outside the product.
```

### Screenshot Cleanup Block

Use when the product image is a screenshot:

```text
The source image may contain app UI. Ignore and do not reproduce phone status bar, app title, ID, price, points, exchange count, promotion text, marketplace card, rounded screenshot frame, or page chrome. Use only the physical product area as the product reference.
```

### Hero Pattern

```text
Create a 960x540 Chinese ecommerce hero image for [product].
[Fidelity Block]
[Screenshot Cleanup Block if needed]
Target audience: 中老年银发群体.
Style: [style], warm, clear, trustworthy, practical, large readable Chinese text, simple layout.
Add only external marketing copy: "[headline]" and "[subheadline]".
Scene: [home/study/lifestyle scene], with clean copy-safe space.
Avoid promotional wording, prices, discounts, gifts, fake certifications, medical claims, QR codes, and dense small text.
```

### Rich Detail Long Pattern

```text
Create one standalone vertical ecommerce detail-page slice for [product].
[Fidelity Block]
[Screenshot Cleanup Block if needed]
Target audience: 中老年银发群体.
Overall style: [style], warm, clean, readable, practical, not crowded.
Slice intent: one of six sequential detail-page slices, later compressed under 500KB and stitched with the other five slices.
This slice number and topic: [01 overview and selling points / 02 usage scene / 03 close-up detail one / 04 close-up detail two / 05 basic information / 06 parameters and usage notes].
Slice content: [specific image and copy].
The specs block must be fully visible, not cropped, not close to the canvas edge, and all text must fit. Use a taller panel, fewer lines, large readable text, and generous bottom safe margin.
Avoid promotional wording, prices, discounts, gifts, medical claims, fake certifications, QR codes, and dense small text.
```

## Differentiated Layout Ideas

- Speaker/audio product: 居家学习功能分区式, alternating people learning scenes with grille/strap/button close-ups.
- Moxibustion patch/warm-care product: 草本护理步骤式, vertical flow sections, packaging close-ups, hand-take detail, home rest scenes.
- Essential oil/aroma product: 日系香氛画册式, more whitespace, soft split panels, bottle label close-up, dropper close-up, reading/tea/sleep scenes.
- Bedding/textile product: 居家卧室体验式, large fabric texture close-ups, making-bed scene, rest scene, storage scene.
- Food/nutrition product: 餐桌日常场景式, package close-up, ingredient atmosphere, serving scene, storage scene; avoid health treatment claims.

## Safe Specs Templates

Use only supplied or safe category-level fields.

Speaker:

```text
品类：便携小音箱
使用方式：放置桌面或随身携带使用
使用场景：听课、听书、居家休闲、户外散步
存储方式：保持干燥，避免重压和长时间暴晒
```

Moxibustion patch / warm-care patch:

```text
品类：艾灸贴
使用方式：按需贴用，注意皮肤感受
使用场景：居家休息、日常放松、外出备用
存储方式：阴凉干燥处保存，避免阳光直射
```

Essential oil:

```text
品类：乳香精油
使用方式：按需取用少量，配合日常护理或香氛场景使用
使用场景：居家放松、学习听课、睡前安静时光
存储方式：密封后置于阴凉干燥处，避免阳光直射和高温
```

## Silver-Age Copy Style

Use calm, practical wording:

- 清楚外放，听课听书更方便
- 拿取轻松，日常使用省心
- 温和陪伴，居家更从容
- 字体清楚，信息一眼看懂
- 课程搭配，学习更自在
- 居家片刻，温和陪伴日常
- 外出居家，随手备用
- 安静片刻，陪伴学习时光

Avoid:

- 优惠、折扣、赠礼、低价、秒杀、限时、福利
- 强力推荐、热门兑换、老师推荐
- 治疗、止痛、祛湿、抗炎、改善疾病、医美功效、疗效承诺

## Review Checklist

Reject and regenerate if:

- Product logo or printed package text changed.
- Bottle/box label text is rewritten, garbled, translated, removed, or replaced.
- Product color, cap, strap, buttons, mesh, ports, box layout, or visible accessories changed.
- Screenshot UI, price, exchange count, promotion text, or page chrome appears.
- Added copy mentions discounts, gifts, price, popularity, medical efficacy, or unsupported specs.
- Detail-page slices all look the same, repeat the same view, or lack two distinct close-up detail slices.
- The bottom specs block is cropped, too close to the edge, incomplete, or text overflows.

## Spec Shape

```json
{
  "batch_name": "product-detail-page-maker",
  "audience": "中老年银发群体",
  "product_fidelity": "exact_product",
  "preserve_product_text": true,
  "detail_mode": "rich_people_scenes_and_closeups",
  "module_output": {
    "hero_size": "960x540",
    "detail_slice_count": 6,
    "stitch_direction": "vertical",
    "bottom_blank_height": 260,
    "compressed_slice_max_kb": 500
  },
  "avoid": ["优惠", "折扣", "赠礼", "低价", "秒杀", "热门兑换", "价格", "医疗功效"],
  "products": [
    {
      "product_name": "兴趣岛小音箱",
      "product_image": "/absolute/path/兴趣岛小音箱.jpg",
      "style": "简约、明亮温暖、银发友好",
      "selling_points": ["小巧便捷", "课程搭配", "声音清楚", "家用省心"],
      "people_scenes": ["居家听课", "客厅听书", "户外散步携带"],
      "detail_closeups": ["正面网面和logo", "挂绳", "顶部按键"],
      "specs": [
        "品类：便携小音箱",
        "使用方式：放置桌面或随身携带使用",
        "使用场景：听课、听书、居家休闲、户外散步",
        "存储方式：保持干燥，避免重压和长时间暴晒"
      ],
      "notes": "不要写优惠、折扣、赠礼；商品logo和机身细节必须完全按原图保留。"
    }
  ]
}
```

## Batch Output Rules

- Generate one `960x540` hero image and exactly six detail slices per product by default.
- Stitch six internally reviewed detail slices into one true long page after generation; do not rely on one image-generation call for the whole long page.
- Export compressed delivery files: every detail slice under `500KB`, and the hero image under `500KB`.
- Do not add a product name line if the product name is missing.
- Do not invent specs. If the table says "按照图片上的信息来写", use only visibly present product information and safe category-level usage/storage fields.
- Replace risky selling words with safer wording:
  - 强力推荐 -> 家用省心 / 使用安心
  - 热门兑换 -> 居家常备 / 日常适用
  - 老师推荐 -> 课程搭配 / 学习陪伴
  - 价格实惠 -> 日常适用 / 轻松使用
- Detail sections should include close-ups and related atmosphere scenes; not every slice should show the full product.
- For multiple products in one batch, make detail-page layouts visibly different by category.
