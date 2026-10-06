"""Capítulo 27: Atributos e métodos.

Parte: Intermediário.
Execute com: python cap27_atributos_metodos.py
"""


# === Atributos de instância e de classe ===

class Contador:
    total_criados = 0

    def __init__(self, nome):
        self.nome = nome
        Contador.total_criados += 1


a = Contador("a")
b = Contador("b")
print(Contador.total_criados, a.total_criados)

class Config:
    nivel = "padrão"


c = Config()
print(c.nivel)
c.nivel = "personalizado"
print(c.nivel, Config.nivel)


# === A armadilha do atributo de classe mutável ===

class Turma:
    alunos = []

    def adicionar(self, nome):
        self.alunos.append(nome)


t1, t2 = Turma(), Turma()
t1.adicionar("Ana")
print(t2.alunos)

class TurmaCorreta:
    def __init__(self):
        self.alunos = []

    def adicionar(self, nome):
        self.alunos.append(nome)


t1, t2 = TurmaCorreta(), TurmaCorreta()
t1.adicionar("Ana")
print(t2.alunos)


# === Métodos de instância, de classe e estáticos ===

class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    @classmethod
    def de_texto(cls, texto):
        nome, idade = texto.split(",")
        return cls(nome.strip(), int(idade))

    @staticmethod
    def eh_maior_de_idade(idade):
        return idade >= 18

    def __repr__(self):
        return f"Pessoa({self.nome!r}, {self.idade})"


p = Pessoa.de_texto("Ana, 30")
print(p, Pessoa.eh_maior_de_idade(p.idade))


# === Exercício: Produto a partir de um dicionário ===

class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    @classmethod
    def de_dict(cls, dados):
        return cls(dados["nome"], dados["preco"])


p = Produto.de_dict({"nome": "caneta", "preco": 3.5})
assert (p.nome, p.preco) == ("caneta", 3.5)
print("ok")
