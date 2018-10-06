def add(bar):
    return bar + 1

def sub(bar):
    return bar - 1

print(add)
print(add(2))
print(sub(2))
print(type(add))


def call_foo_with_arg(add, arg):
    return add(arg)


print(call_foo_with_arg(add, 3))
