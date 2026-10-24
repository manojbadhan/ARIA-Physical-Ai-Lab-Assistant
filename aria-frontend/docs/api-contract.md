# ask(query) contract

`async ask(query: string)` in `js/api.js`.

Returns `null` when nothing is retrieved, otherwise:

```json
{
  "t": ["paragraph", "paragraph"],
  "f": "optional formula string",
  "s": [[0, "Section name", 0.91, "Passage text"]]
}
```

- `t`: answer paragraphs
- `f`: optional formula, shown in a monospace block
- `s`: sources as `[docIndex, sectionName, relevance 0-1, passageText]`; `docIndex` is a 0-based index into `DOCS`

Answers must come only from retrieved lab documents.

## askImage(imageDataUrl, query)

`async askImage(imageDataUrl: string, query: string)` in `js/api.js`, called by the Camera button.

- `imageDataUrl`: one captured frame as a JPEG data URL (`data:image/jpeg;base64,...`), at most 1024 px on the longest side
- `query`: the optional question typed in the camera view, `""` if none

Returns `null` or the same shape as `ask()`. `s` may be an empty array when the answer has no document sources; the sources block is then hidden.
