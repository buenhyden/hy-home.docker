---
trigger: always_on
glob: "**/*.py,**/*.sh,**/*.c"
description: "FFmpeg: Multimedia Processing Standards."
---
# FFmpeg Standards

## 1. Command Line usage

- **Order Matters**: Input options (`-ss`, `-t`) must come BEFORE `-i`. Output options come after.
- **Stream mapping**: Always explicitly map streams (`-map 0:v:0 -map 1:a:0`) if there are multiple inputs or logical streams.

### Example: Seeking

**Good** (Fast seek)
`ffmpeg -ss 00:00:30 -i input.mp4 ...`

**Bad** (Slow seek)
`ffmpeg -i input.mp4 -ss 00:00:30 ...` (Decodes until timestamp)

## 2. Encoding

- **Codecs**: Prefer modern, royalty-free codecs if possible/compatible (`libaom-av1`, `libopus`).
- **CRF**: Use Constant Rate Factor (`-crf`) for file-based encoding (quality-based) rather than fixed bitrate, unless streaming.

## 3. Filters

- **Filter Chains**: Combine simple filters into a single filter graph (`-vf`) for efficiency rather than chaining multiple ffmpeg processes.
- **Complex Graphs**: Use `-filter_complex` for mixing multiple inputs (overlays, side-by-side).

## 4. API Usage (libav)

- **Memory**: Ensure proper allocation and freeing (`av_frame_alloc`, `av_frame_free`) to leak checks.
- **Errors**: Check return codes. FFmpeg uses negative error codes (e.g., `AVERROR(EAGAIN)`).
