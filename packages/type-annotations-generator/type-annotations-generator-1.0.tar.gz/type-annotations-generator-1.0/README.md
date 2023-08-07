# type-annotations-generator

type-annotations-generator provides a function for generating type annotations. That can be useful if you work with a API which has a complex data structure.
It supports [PEP 585](https://www.python.org/dev/peps/pep-0585) and [PEP 604](https://www.python.org/dev/peps/pep-0604).

```python
import type_annotations_generator

data = {
    "elements": [
        {
            "name": "foo",
            "age": 42
        }
    ],
    "count": 1
}

print(type_annotations_generator.generate_annotations(data))
# Dict[str, Union[List[Dict[str, Union[str, int]]], int]]

print(type_annotations_generator.generate_annotations(data, pep_585=True))
# dict[str, Union[list[dict[str, Union[str, int]]], int]]

print(type_annotations_generator.generate_annotations(data, pep_585=True, pep_604=True))
# dict[str, list[dict[str, str | int]] | int]
```
