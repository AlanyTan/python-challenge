#### Do not change this section ##### 
a = 0b10011010
b = 0b00110111
c = 13
d = 105
##### End do-not-change section #####

# given the below values of variable a to d, complete the following code: 

# print the value of a and bitwise NOT a:
print(a,~a)

# manually calculate bitwise NOT of b, and NOT c, and add answer to the 
#  right side of = of the following assignment statement 
# (hint, for b, you can flip each bit, but 0b format are unsigned, you will 
#  need to manually convert the result as a signed integer, since it has 8 bits,
#  the highest bit is used as sign, so you need to subtract the result by 256, 
#  this is needed because integers are signed internally, but 0b format is 
#  unsigned ;
#  for c, you actually don't need to do it bit by bit, although it is 
#  perfectly legit to convert it to binary and do it as b.):
answer_bitwise_not_b = -56
answer_bitwise_not_c = -14
print(answer_bitwise_not_b, answer_bitwise_not_c)

# consider a and c, with bitwise AND, XOR, OR, which operation of these
#  two values will produce the largest amount, what is the result value of this
#  operation? (use an expression to answer, but you need to know which
#  operation produce the largest result):
answer_largest_bitwise_operation_of_a_and_c = a | c
print(answer_largest_bitwise_operation_of_a_and_c)

# The following code tries to multiply d by c using bitwise operations.
# To simplify the solution, we will use add operation +, but we have
# shown using bitwise operation to realize addition, so it's possible to
# completely realize multiplication using bitwise operations only.
# Your task is to complete the missing parts of the code below (note, we 
# intentionally break down the steps to step_0 to step_4, so we can check the
# intermediate results and make sure you did everything correctly.  With 4 
# steps, we will only be able to handle c<=15, that is ok for now.)

# step0
multiplier = c
result = 0
multiplicand = d

# step1
print(result)
if multiplier & 1: 
    result += multiplicand
multiplicand = multiplicand << 1

# step2
print(result)
if multiplier & 2:
    result += multiplicand
multiplicand <<= 1


# based on the above lines, use same logic, please finish ...step_3 
# and ...ste_4, so that final result equals d * c
# (please print intermediate result like above.)
# step2
print(result)
if multiplier & 4:
    result += multiplicand
multiplicand <<= 1
# step4
print(result)
if multiplier & 8:
    result += multiplicand
multiplicand <<= 1

# final result
print(result)
