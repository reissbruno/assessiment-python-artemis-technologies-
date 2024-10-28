import unittest

from desafio_3 import cached_property 

class TestCachedProperty(unittest.TestCase):
    def setUp(self):
        # Definir uma classe de teste que utiliza o decorador
        class TesteClasse:
            def __init__(self, a, b):
                self.a = a
                self.b = b
                self.contador = 0

            @cached_property('a', 'b')
            def propriedade_computada(self):
                self.contador += 1
                return self.a + self.b

        self.TesteClasse = TesteClasse

    def test_computacao_inicial(self):
        obj = self.TesteClasse(1, 2)
        resultado = obj.propriedade_computada
        self.assertEqual(resultado, 3)
        self.assertEqual(obj.contador, 1)

    def test_uso_do_cache(self):
        obj = self.TesteClasse(1, 2)
        _ = obj.propriedade_computada  # Primeira computação
        resultado = obj.propriedade_computada  # Deve usar o cache
        self.assertEqual(resultado, 3)
        self.assertEqual(obj.contador, 1)  # A função não deve ter sido chamada novamente

    def test_alteracao_de_dependencia(self):
        obj = self.TesteClasse(1, 2)
        _ = obj.propriedade_computada  # Primeira computação
        obj.a = 5  # Alterar uma dependência
        resultado = obj.propriedade_computada  # Deve recomputar
        self.assertEqual(resultado, 7)
        self.assertEqual(obj.contador, 2)  # A função deve ter sido chamada novamente

    def test_alteracao_nao_dependente(self):
        obj = self.TesteClasse(1, 2)
        _ = obj.propriedade_computada  # Primeira computação

        # Adicionar um atributo que não é dependência
        obj.c = 10
        resultado = obj.propriedade_computada  # Deve usar o cache
        self.assertEqual(resultado, 3)
        self.assertEqual(obj.contador, 1)

    def test_multiplas_instancias(self):
        obj1 = self.TesteClasse(1, 2)
        obj2 = self.TesteClasse(3, 4)

        resultado1 = obj1.propriedade_computada
        resultado2 = obj2.propriedade_computada

        self.assertEqual(resultado1, 3)
        self.assertEqual(resultado2, 7)
        self.assertEqual(obj1.contador, 1)
        self.assertEqual(obj2.contador, 1)

    def test_exclusao_de_atributo(self):
        obj = self.TesteClasse(1, 2)
        _ = obj.propriedade_computada  # Primeira computação
        del obj.a  # Exclui uma dependência

        with self.assertRaises(AttributeError):
            _ = obj.propriedade_computada

    def test_dependencia_mutavel(self):
        class TesteDependenciaMutavel:
            def __init__(self, dados):
                self.dados = dados
                self.contador = 0

            @cached_property('dados')
            def propriedade_computada(self):
                self.contador += 1
                return sum(self.dados)

        obj = TesteDependenciaMutavel([1, 2, 3])
        resultado = obj.propriedade_computada
        self.assertEqual(resultado, 6)
        self.assertEqual(obj.contador, 1)

        # Modificar o conteúdo da lista
        obj.dados.append(4)
        resultado = obj.propriedade_computada  # Como a referência é a mesma, o cache não é invalidado
        self.assertEqual(resultado, 6)
        self.assertEqual(obj.contador, 1)

        # Para lidar com isso, precisaríamos implementar uma comparação profunda ou usar tipos imutáveis

    def test_sem_dependencias(self):
        class TesteSemDependencias:
            def __init__(self):
                self.contador = 0

            @cached_property()
            def propriedade_computada(self):
                self.contador += 1
                return 42

        obj = TesteSemDependencias()
        resultado = obj.propriedade_computada
        self.assertEqual(resultado, 42)
        self.assertEqual(obj.contador, 1)

        resultado = obj.propriedade_computada  # Deve usar o cache
        self.assertEqual(obj.contador, 1)

    def test_invalida_cache_manual(self):
        obj = self.TesteClasse(1, 2)
        _ = obj.propriedade_computada  # Primeira computação

        # Limpar o cache manualmente
        delattr(obj, '_cached_propriedade_computada')

        resultado = obj.propriedade_computada  # Deve recomputar
        self.assertEqual(resultado, 3)
        self.assertEqual(obj.contador, 2)

if __name__ == '__main__':
    unittest.main()
