# Round and convert decimal number to cents


## Install package
```bash
pip install redondear-dsalinas
```

## Package usage
```python
from redondear import redondear

number = redondear.round_number("2.5456756") # 2.55 
cents = redondear.to_cents(number) # 255
decimals = redondear.to_decimals(cents) # 2.55

print(number, cents, decimals) # 2.55 255 2.55
```
 
