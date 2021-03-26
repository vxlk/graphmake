# here will be a collection of asserts for use with gmake

def assert_eq(left, right) -> None:
    assert(left == right)

def assert_eq_epsilon(left, right, epsilon : float) -> None:
    assert(abs(left - right) < epsilon)