# library.qai.utilities

Helper functions and classes for interacting with the rest of the Writer platform. The main components are:

- `qai.issues.make_issue`: makes a dictionary that conforms to Writer platform standards
- `qai.spacy_factor.SpacyFactor`: a helper class which turns a spaCy Span into an issue
- `qai.server.QRest`: a helper class which builds a Sanic REST server for you
- `qai.validation.Validator`: a simple validator class that can be used to skip segments without processing them, e.g. for being empty or having HTML. You would only want to import this yourself if you aren't using `QRest`

If you are building a Sanic app without using `QRest`, you still may be interested in the following middleware:

- `qai.server.set_valid_segments`: stores valid segments to `request.ctx.segments` and also sets `request.ctx.info`
- `qai.server.postprocess_issues`: changes the string indexing to be utf-16 based, and filters no ops

(See GitHub history for older docs - QAI used to do a lot more!)

## Testing QAI services

With QAI >=6.0.0, it is easy to test a QAI-based service running in k8s, first start the k8s proxy with `$kubectl proxy` and then `$ python` (or, if you are fancy, `$ python -m IPython`)

```python
from qai.testing import *

name_test_qai("testing string", "service name")
```

That's all! The meta is inferred from the service name.

You can also test a service running on localhost port 5000 by:

```python
from qai.testing import *

test_qai("testing string", url=5000)
# or to imply meta by name
test_qai("testing string", "service name", url=5000)
# or to explicitly specify meta
test_qai("testing string", meta={"some key": val}, url=5000)
```

## Upgrading to v5

- `Analyzer` class must now be callable. It will be passed `(segment: str, meta: dict, all_info: dict)` - `segment` is the string to analyze, `meta` is the `meta` object that was sent, or `{}` if none was sent, and `all_info` is the entire payload the server received - in case you need access to clientID or something. Feel free to define `def __call__(self, segment: str, meta: dict, _)` if you don't expect to need the request.
- `QRest` can be passed a Sanic app, or be passed a dictionary which maps issue types to categories (in addition to the default behavior). This is useful for services that handle multiple categories, for which the default behavior doesn't work.
- QAI has a simpler structure, so all imports look different
- Configs, Strings, Storage, and Document are gone. The later 2 because they aren't needed anymore, the former 2 because you should manage that yourself. Whitelisting is also gone - just don't make the issues if you don't want them.
- All issues are created in the v2 format (meaning, the format we switched to after new segmentation - defined [here](https://writerai.atlassian.net/wiki/spaces/HOME/pages/2115928140/NLP+Services+API+Contract+Meta))
- By default, issue `from` and `until` keys are now based on UTF-16 indexing, to make things easier for JS. We add `_from_p` and `_until_p` keys for debugging, which are the Python string indexes. This happens as response middleware in QRest.

## Usage

You can explicitly create a REST connection like this:

```python
from app import Analyzer

from qai.server import QRest


# setting the category / service name does nothing
# we use the category passed on the request
category = 'service_name'
host = '0.0.0.0'
port = 5000


if __name__ == '__main__':
    analyzer = Analyzer()
    rest_connection = QRest(
      analyzer,
      category=category,
      host=host,
      port=port
    )
    # create a blocking connection:
    rest_connection.connect()
```

The above will create *as many workers as you have cores.* This is great, sometimes. For example, there is a known bug where AutoML crashes if you are using more than one worker. So pass `workers=1` if this happens

There is also a helper class for turning spaCy `Span`s into issues the rest of the platform can process:

```python
from spacy.tokens import Span
from qai.spacy_factor import SpacyFactor


MyFactor = SpacyFactor(
    "subject_object_verb_spacing",
    "Keep the subject, verb, and object of a sentence close together to help the reader understand the sentence."
)

Span.set_extension("score", default=0)
Span.set_extension("suggestions", default=[])

doc = nlp("Holders of the Class A and Class B-1 certificates will be entitled to receive on each Payment Date, to the extent monies are available therefor (but not more than the Class A Certificate Balance or Class B-1 Certificate Balance then outstanding), a distribution.")
score = analyze(doc)
if score is not None:
    span = Span(doc, 0, len(doc))  # or whichever tokens/spans are the issue (don't have to worry about character indexes)
    span._.score = score
    span._.suggestions = get_suggestions(doc)
    issue = MyFactor(span)
```

## Installation

`pip install qai` or `poetry add qai`

## Testing

See Confluence for docs on input format expectations.

`scripts/test_qai.sh` has some helpful testing functions.

### CI/CD

GitHub Actions will push to PyPi when you merge into the `main` branch.

### License

This software is not licensed. If you do not work at Writer, you are not legally allowed to use it. Also, it's just helper functions that really won't help you. If something in it does look interesting, and you would like access or our help, open an issue.
