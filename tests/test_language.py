import pytest

from pytuga import transpile
from transpyler import get_transpyler

tokenize = get_transpyler().lexer.tokenize


def pytg(src):
    return [repr(x) for x in tokenize(transpile(src))]


def py(src):
    return [repr(x) for x in tokenize(src)]


#
# Dictionary of translations. Each test case is separated by a line of ='s and
# where the 1st part has a Pytugues code and the second part has the
# corresponding python source
#
data = r'''
================================================================================

--------------------------------------------------------------------------------

================================================================================
verdadeiro, falso, nulo, Verdadeiro, Falso, Nulo
--------------------------------------------------------------------------------
True, False, None, True, False, None
================================================================================
a ou b, a e b, a é b
--------------------------------------------------------------------------------
a or b, a and b, a is b
================================================================================
repetir 4 vezes: prosseguir
--------------------------------------------------------------------------------
for ___ in range(4): pass
================================================================================
repetir 4 vezes:
    prosseguir
--------------------------------------------------------------------------------
for ___ in range(4):
    pass
================================================================================
    repetir 4 vezes:
        prosseguir
--------------------------------------------------------------------------------
    for ___ in range(4):
        pass
================================================================================
para x em L:
    prosseguir
--------------------------------------------------------------------------------
for x in L:
    pass
================================================================================
para x em L faça:
    prosseguir
--------------------------------------------------------------------------------
for x in L:
    pass
================================================================================
para cada x em L faça:
    prosseguir
--------------------------------------------------------------------------------
for x in L:
    pass
================================================================================
para cada x em L faca:
    prosseguir
--------------------------------------------------------------------------------
for x in L:
    pass
================================================================================
para cada x de 1 até 10:
    prosseguir
--------------------------------------------------------------------------------
for x in range(1, 10 + 1):
    pass
================================================================================
'''.split('=' * 80)

data = [x.split('-' * 80) for x in data if x.strip()]


@pytest.fixture(params=data)
def sources(request):
    return request.param


def test_pytuga_to_python_transpile(sources):
    pytuga, python = sources
    assert pytg(pytuga) == py(python)


#
# Passthru translations. Each test case is separated by a blank line.
#
data = r'''
mostre(42)

x + y, x * y
'''.split('\n\n')


@pytest.fixture(params=data)
def passtru(request):
    return request.param


def test_passthru(passtru):
    assert py(passtru) == pytg(passtru)


#
# Old tests
#
def test_para_cada_in_range():
    ptsrc = []
    pysrc = []

    ptsrc.append('para x de 1 até 10: mostre(x)')
    pysrc.append('for x in range(1, 10 + 1): mostre(x)')

    ptsrc.append('para x de 1 até 10:\n    mostre(x)')
    pysrc.append('for x in range(1, 10 + 1):\n    mostre(x)')

    ptsrc.append('para x de 1 até 10 faça: mostre(x)')
    pysrc.append('for x in range(1, 10 + 1): mostre(x)')

    ptsrc.append('para x de 1 até 10 a cada 2: mostre(x)')
    pysrc.append('for x in range(1, 10 + 1, 2): mostre(x)')

    ptsrc.append('para x de 1 até 10 a cada 2 faça: mostre(x)')
    pysrc.append('for x in range(1, 10 + 1, 2): mostre(x)')

    ptsrc.append('para x de 1 até 10 a cada 2 faça:\n    mostre(x)')
    pysrc.append('for x in range(1, 10 + 1, 2):\n    mostre(x)')

    ptsrc.append('\n\npara cada x em [1, 2, 3]: mostre(x)')
    pysrc.append('\n\nfor x in [1, 2, 3]: mostre(x)')

    ptsrc.append('para x de 10 até 20: mostre(x)')
    pysrc.append('for x in range(10, 20 + 1): mostre(x)')

    ptsrc.append('para xx de 10 até 20: mostre(x)')
    pysrc.append('for xx in range(10, 20 + 1): mostre(x)')

    test_cases = list(zip(ptsrc, pysrc))

    for pt_str, py_str in test_cases:
        assert pytg(pt_str) == py(py_str)


def test_enquanto():
    ptsrc = 'enquanto x < 1: mostre(x)'
    pysrc = 'while x < 1: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'enquanto x < 1 faça: mostre(x)'
    pysrc = 'while x < 1: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'enquanto x < 1 faça:\n    mostre(x)'
    pysrc = 'while x < 1:\n    mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'enquanto não x: mostre(x)'
    pysrc = 'while not x: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)


def test_se():
    ptsrc = []
    pysrc = []

    ptsrc.append('se x < 1 então: mostre(x)')
    pysrc.append('if x < 1: mostre(x)')

    ptsrc.append('se x < 1: mostre(x)')
    pysrc.append('if x < 1: mostre(x)')

    ptsrc.append('se x < 1 então:\n    mostre(x)')
    pysrc.append('if x < 1:\n    mostre(x)')

    ptsrc.append('se não x: mostre(x)')
    pysrc.append('if not x: mostre(x)')

    ptsrc.append('\n\n\nse não x: mostre(x)')
    pysrc.append('\n\n\nif not x: mostre(x)')

    test_cases = zip(ptsrc, pysrc)

    for pt_str, py_str in test_cases:
        assert pytg(pt_str) == py(py_str)


def test_se_senao():
    ptsrc = '''
se x < 1 então:
    mostre(x)
senão:
    mostre(-x)
'''
    pysrc = '''
if x < 1:
    mostre(x)
else:
    mostre(-x)
'''
    assert pytg(ptsrc) == py(pysrc)


def test_se__ou_entao_se__senao():
    ptsrc = '''
se x < 1 então:
    mostre(x)
ou então se x > 3:
    mostre(0)
senão:
    mostre(-x)
'''
    pysrc = '''
if x < 1:
    mostre(x)
elif x > 3:
    mostre(0)
else:
    mostre(-x)
'''
    assert pytg(ptsrc) == py(pysrc)


def test_function_definition():

    ptsrc = []
    pysrc = []

    ptsrc.append('função foo(x): retorne x')
    pysrc.append('def foo(x): return x')

    ptsrc.append('definir foo(x): retorne x')
    pysrc.append('def foo(x): return x')

    ptsrc.append('definir função foo(x): retorne x')
    pysrc.append('def foo(x): return x')

    ptsrc.append('definir função foo(x):\n    retorne x')
    pysrc.append('def foo(x):\n    return x')

    # Integração
    ptsrc.append('para cada x em [1, 2, 3]:\n    mostre(x ou z)')
    pysrc.append('for x in [1, 2, 3]:\n    mostre(x or z)')

    for pt_str, py_str in zip(ptsrc, pysrc):
        assert pytg(pt_str) == py(py_str)


#
# Simple binary operators
#
def test_logical_and():
    ptsrc = 'x e y'
    pysrc = 'x and y'
    assert pytg(ptsrc) == py(pysrc)


def test_is_operator():
    ptsrc = 'x é verdadeiro'
    pysrc = 'x is True'
    assert pytg(ptsrc) == py(pysrc)


def test_nested_loops():
    ptsrc = '''
repetir 2 vezes:
    repetir 2 vezes:
        mostre(1)
'''

    pysrc = '''
for ___ in range(2):
    for ___ in range(2):
        mostre(1)
'''
    assert pytg(ptsrc) == py(pysrc)


def test_prefixed_nested_repetir_loops():
    ptsrc = '''
repetir 2 vezes:
    1
    repetir 2 vezes:
        1
'''

    pysrc = '''
for ___ in range(2):
    1
    for ___ in range(2):
        1
'''
    print(pytg(ptsrc))
    print(py(pysrc))
    assert pytg(ptsrc) == py(pysrc)


def test_prefixed_nested_para_cada_loops():
    ptsrc = '''
para cada x de 1 até 2:
    1
    para cada y de 1 até 2:
        1
'''

    pysrc = '''
for x in range(1, 2 + 1):
    1
    for y  in range(1, 2 + 1):
        1
'''
    print(pytg(ptsrc))
    print(py(pysrc))
    assert pytg(ptsrc) == py(pysrc)


#
# Bug tracker: these are all examples that have failed in some point and do not
# belong to any category in special
#
def test_separate_command_blocks_regression():
    ptsrc = 'mostre(1)\n\n\n\npara cada x em [1, 2, 3]: mostre(x)'
    pysrc = 'mostre(1)\n\n\n\nfor x in [1, 2, 3]: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = 'mostre(1)\n\n\n\npara x de 1 até 3: mostre(x)'
    pysrc = 'mostre(1)\n\n\n\nfor x in range(1, 3 + 1): mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = '\n\n\nsenão: mostre(x)'
    pysrc = '\n\n\nelse: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

    ptsrc = '\n\n\nsenão faça: mostre(x)'
    pysrc = '\n\n\nelse: mostre(x)'
    assert pytg(ptsrc) == py(pysrc)

def test_function_with_long_docstring():
    ptsrc = '''
função foo():
    """
    x
    """
    x
'''
    pysrc = '''
def foo():
    """
    x
    """
    x
'''
    assert pytg(ptsrc) == py(pysrc)


def test_full_conditional_command():
    ptsrc = 'se x então faça:\n    pass'
    pysrc = 'if x:\n   pass'
    assert pytg(ptsrc) == py(pysrc)
