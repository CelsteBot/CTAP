from ctypes import *

MyLev = cdll.LoadLibrary('./C_Tests/my_lib.so').MyLev

str1 = 'setting'
str2 = 'sittmg'

b_str1 = str1.encode('utf8')
b_str2 = str2.encode('utf8')

MyLev.argtypes = [c_char_p, c_char_p, c_uint]
res = MyLev(b_str1, b_str2, 2)

print(res)
