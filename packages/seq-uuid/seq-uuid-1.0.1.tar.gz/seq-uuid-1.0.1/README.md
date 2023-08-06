# seq-uuid

A Python library to generate UUID version 4 and 5, based on [RFC4122](https://datatracker.ietf.org/doc/html/rfc4122)
and version 6 based
on [RFC4122 2021 draft edition](https://datatracker.ietf.org/doc/html/draft-peabody-dispatch-new-uuid-format).

# Examples

```python
import seq_uuid

identifier = seq_uuid.uuid6()

print(identifier)
```

```python
import seq_uuid

id1 = seq_uuid.uuid6()
id2 = seq_uuid.uuid6()

print(id1)
print(id2)

assert (id1 < id2)
assert (id1.version == 6)
```
