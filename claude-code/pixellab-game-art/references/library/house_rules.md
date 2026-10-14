# House rules that apply everywhere


- **Style anchor first.** Almost every production call passes a reference image of an approved
  asset, using `style_image_url` / `style_image` / `color_image_url` / `style_images`. A prompt
  alone drifts across a set. Reuse the same anchor for the whole family (all icons, all buildings,
  all heroes).
- **A fixed seed per family** (7 is the house default, then 11, 21, 3) keeps a batch consistent.
- **Say what is NOT wanted.** Most retries added negatives: `no characters`, `no people`,
  `no text, no letters`, `no frame, no square, no backdrop`, `not a dragon`, `NOT a lion`,
  `no metal, no armor plates`, `no guns`. A negative only guards against what nobody asked for:
  never add one that contradicts the user's request (a rifle-armed knight gets no `no guns`).
- **Say how it sits in the canvas.** `single object centred`, `filling the frame`,
  `fully inside the image with a small margin`, `feet in the same place`,
  `standing on a flat ground line`.
- **The palette words recur:** dark fantasy, muted colours, violet arcane glow, warm ember / gold
  light against cold blue / violet shadow, night.
- **Transparency:** `no_background: true` for every sprite, prop and icon. Backdrops and
  battle backgrounds use `false`.
