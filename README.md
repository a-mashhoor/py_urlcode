# Py URL Encoder/Decoder
Very simple URL encoder/decoder that works both with
command line argument input, input file, and with linux pipe line
(reading from stdin)

## Installing:
No additional libraries so you can use it out of the box
with just python3 installed on your system
```shell
git clone https://github.com/a-mashhoor/py_urlcode

```

## Usage:

for encoding
```shell
echo "data,and, more, data" | py py_urlcode.py -ue
py py_urlcode.py -ue -d "data,and, more, data"
```
for double encoding
```shell
py py_urlcode.py -ue -d data%2Cand%2C%20more%2C%20data%20
```
for decoding
```shell
py py_urlcode.py -ud -d data%2Cand%2C%20more%2C%20data%20
echo data%2Cand%2C%20more%2C%20data%20 | py py_urlcode.py -ud
```
enjoy :)
