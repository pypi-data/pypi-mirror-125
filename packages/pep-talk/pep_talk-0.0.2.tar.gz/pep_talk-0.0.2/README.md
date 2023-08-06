# Pep Talk!
A little library to give your day a little pep!

# Install

```bash
$ pip install pep-talk
```

# Running

```bash
$ pep-talk 
Okay, listen up: the way you roll deserves the Nobel Prize, period.
```

## Colour Options
This module uses the `colored` module from [https://pypi.org/project/colored/](https://pypi.org/project/colored/).
Check the link to see the colour options.

To enable the colour features, use the following:
```bash
--fg Foreground colour
--bg Background colour
--attr Text attributes, bold etc.
```

```python
$ pep-talk --bg black --fg green --attr bold
```
