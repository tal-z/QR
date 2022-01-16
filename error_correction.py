''' Early Attempts
"""
const LOG = new Uint8Array(256);
const EXP = new Uint8Array(256);
for (let exponent = 1, value = 1; exponent < 256; exponent++) {
  value = value > 127 ? ((value << 1) ^ 285) : value << 1;
  LOG[value] = exponent % 255;
  EXP[exponent % 255] = value;
}
"""

log = {}
exp = {}
value = 1
for exponent in range(1, 256):
    value = ((value << 1) ^ 285) if value > 127 else value << 1
    log[value] = exponent % 255
    exp[log[value]] = value


"""
function mul(a, b) {
  return a && b ? EXP[(LOG[a] + LOG[b]) % 255] : 0;
}
function div(a, b) {
  return EXP[(LOG[a] + LOG[b] * 254) % 255];
}
"""


def mul(a, b):
    return exp[(log[a] + log[b]) % 255] if (a and b) else 0


def div(a, b):
    return exp[(log[a] + log[b] * 254 % 255)]

print(div(128,2))
'''
# With modules
import galois

GF256 = galois.GF(2**8)


GF256.