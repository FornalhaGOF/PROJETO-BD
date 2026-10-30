"""Projeto 01: CRUD de alunos por matricula."""
from pymongo.errors import DuplicateKeyError
from conexao import banco

alunos = banco['alunos_p01']
alunos.create_index('matricula', unique=True)

while True:
    print('\n[1] Cadastrar [2] Listar [3] Alterar [4] Excluir [0] Sair')
    opcao = input('Opcao: ').strip()
    if opcao == '1':
        matricula = input('Matricula: ').strip()
        nome = input('Nome: ').strip()
        curso = input('Curso: ').strip()
        if not all([matricula, nome, curso]):
            print('Preencha todos os campos.')
            continue
        try:
            alunos.insert_one({'matricula': matricula, 'nome': nome, 'curso': curso})
            print('Aluno cadastrado!')
        except DuplicateKeyError:
            print('Matricula ja cadastrada.')
    elif opcao == '2':
        for aluno in alunos.find({}, {'_id': 0}).sort('nome', 1):
            print(aluno)
    elif opcao == '3':
        matricula = input('Matricula: ').strip()
        novo_curso = input('Novo curso: ').strip()
        if novo_curso:
            r = alunos.update_one({'matricula': matricula}, {'$set': {'curso': novo_curso}})
            print('Atualizado!' if r.matched_count else 'Aluno nao encontrado.')
    elif opcao == '4':
        matricula = input('Matricula: ').strip()
        r = alunos.delete_one({'matricula': matricula})
        print('Excluido!' if r.deleted_count else 'Aluno nao encontrado.')
    elif opcao == '0':
        break
    else:
        print('Opcao invalida.')
