import pytest
import math as _math
import random as _random

import pytuga.lib.tuga_math as math

pi = _math.pi
neperiano = _math.exp(1)

def test_raiz():

	assert(math.raiz(4) == 2.0)
	assert(math.raiz(16) == 4.0)

def test_seno():

	assert(math.seno(0) == 0.0)
	

def test_cosseno():

	assert(math.cosseno(0) == 1.0)
	

def test_tangente():

	assert(math.tangente(0) == 0.0)

def test_exponencial():

	assert(math.exponencial(1) == 2.718281828459045)

def test_logaritimo():

	assert(math.logarítimo(1) == 0.0)

def test_log10():

	assert(math.log10(10) == 1.0)

def test_modulo():

	assert(math.módulo(-1) == 1)

def test_sinal():

	assert(math.sinal(-32.0) == -1)

def test_arredondar():

	assert(math.arredondar(1.6) == 2)

def test_truncar():

	assert(math.truncar(1.6) == 1 and math.truncar(1.8) == 1 and math.truncar(1.806) == 1)
	assert(math.truncar(5.3) == 5 and math.truncar(3.14) == 3 and math.truncar(9.7) == 9)

def test_maximo():

	assert(math.máximo([1, 5, 42, 0]) == 42)

def test_minimo():

	assert(math.mínimo([1, 5, 42, 0]) == 0)

def test_soma():

	assert(math.soma([1, 2, 3, 4]) == 10)

def test_produto():

	assert(math.produto([1, 2, 3, 4, 5]) == 120)

def test_todos():

	assert(math.todos([True, True, True]) == True)
	assert(math.todos([True, False, True]) == False)

def test_algum():

	assert(math.algum([True, False, False]) == True)
	assert(math.algum([False, False, False]) == False)


def test_aleatorio():

	for i in range(5):
		resultado = math.aleatório()
		assert(resultado >= 0 and resultado <= 1)

def test_inteiro_aleatório():
	
	resultado = math.inteiro_aleatório(1, 20)
	assert(resultado >= 1 and resultado <= 20)

def test_lancar_dado():

	for i in range(5):
		resultado = math.lançar_dado()
		assert(resultado >= 1 and resultado <= 6)
