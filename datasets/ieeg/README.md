# IEEG Datasets

https://ieeg.org (requires making an account)

```
cd ieegpy
python setup.py build
python setup.py install
```


## Scripts
See [ieegpy/README.md](https://github.com/ieeg-portal/ieegpy/blob/080bfa42a8503380ef164b5e7b116613f75073bb/README.md)

```
python get_data_by_annotation.py -u ${USER} -p ${PWD} ${DATASET} ${ANNOTATION_TYPE}
```

## Dataset Names

* `I001_P013_D01`
    * 72 channels, 5000 Hz sampling rate
    * Referenced in the SCALO paper

## Examples
```
python get_data_by_annotation.py -u meugur -p password123 I001_P013_D01 Seizure
```
