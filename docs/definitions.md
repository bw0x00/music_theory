# Supported musical definitions

The musical definitions are done specificaly for a defined chromatic scale.
By default (and this is currently the only supported chromatic scale), 
`12 equal temperament` is used.

Additional chromaticscales can be supported by

1. adding the required definitions to the config files below
2. defining a compatible temperament class for the usage in an
    chromatic scale object

## Intervals
Defined in `trallala/config_intervals.py`
```python
--8<-- "trallala/config_intervals.py"
```

## Scales
Defined in `trallala/config_scales.py`
```python
--8<-- "trallala/config_scales.py"
```

## Chords
Defined in `trallala/config_chords.py`
```python
--8<-- "trallala/config_chords.py"
```

