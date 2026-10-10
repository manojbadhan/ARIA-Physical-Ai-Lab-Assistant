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
