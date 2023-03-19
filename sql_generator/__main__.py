import argparse
from datetime import date, timedelta

# Table data as lists of dictionaries
ALUNO = [
    {'codigo': i, 'nome': f'Aluno {i}', 'matricula': i + 100}
    for i in range(1, 51)
]
PROFESSOR = [
    {'codigo': i, 'nome': f'Professor {i}'}
    for i in range(1, 51)
]
TURMA = [
    {'codigo': i, 'nome': f'Turma {i}', 'codigo_professor': (i % 50) + 1}
    for i in range(1, 51)
]
PROVA = [
    {'codigo': i, 'titulo': f'Prova {i}', 'data_aplicacao': date.today() - timedelta(days=i), 'codigo_turma': (i % 50) + 1}
    for i in range(1, 51)
]
TURMA_ALUNO = [
    {'codigo': i, 'codigo_turma': (i % 50) + 1, 'codigo_aluno': (i % 50) + 1}
    for i in range(1, 51)
]
PROVA_ALUNO = [
    {'codigo': i, 'codigo_prova': (i % 50) + 1, 'codigo_aluno': (i % 50) + 1}
    for i in range(1, 51)
]

# SQL insert statements templates
ALUNO_SQL_TEMPLATE = "INSERT INTO aluno (`codigo`, `nome`, `matricula`) VALUES ({codigo}, '{nome}', {matricula});\n"
PROFESSOR_SQL_TEMPLATE = "INSERT INTO professor (`codigo`, `nome`) VALUES ({codigo}, '{nome}');\n"
TURMA_SQL_TEMPLATE = "INSERT INTO turma (`codigo`, `nome`, `codigo_professor`) VALUES ({codigo}, '{nome}', {codigo_professor});\n"
PROVA_SQL_TEMPLATE = "INSERT INTO prova (`codigo`, `titulo`, `data_aplicacao`, `codigo_turma`) VALUES ({codigo}, '{titulo}', '{data_aplicacao}', {codigo_turma});\n"
TURMA_ALUNO_SQL_TEMPLATE = "INSERT INTO turma_aluno (`codigo`, `codigo_turma`, `codigo_aluno`) VALUES ({codigo}, {codigo_turma}, {codigo_aluno});\n"
PROVA_ALUNO_SQL_TEMPLATE = "INSERT INTO prova_aluno (`codigo`, `codigo_prova`, `codigo_aluno`) VALUES ({codigo}, '{codigo_prova}', {codigo_aluno});\n"

def generate_insert_sql(table, sql_template):
    """
    Generates SQL insert statements for the given table data and SQL template
    """
    sql_statements = []
    for row in table:
        sql_statements.append(sql_template.format(**row))
    return sql_statements



if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=50, help='Number of rows to generate')
    args = parser.parse_args()

    # Generate SQL insert statements for each table
    sqls = {}
    sqls['aluno_sql'] = generate_insert_sql(ALUNO[:args.rows], ALUNO_SQL_TEMPLATE)
    sqls['professor_sql'] = generate_insert_sql(PROFESSOR[:args.rows], PROFESSOR_SQL_TEMPLATE)
    sqls['turma_sql'] = generate_insert_sql(TURMA[:args.rows], TURMA_SQL_TEMPLATE)
    sqls['prova_sql'] = generate_insert_sql(PROVA[:args.rows], PROVA_SQL_TEMPLATE)
    sqls['turma_aluno_sql'] = generate_insert_sql(TURMA_ALUNO[:args.rows], TURMA_ALUNO_SQL_TEMPLATE)
    sqls['prova_aluno_sql'] = generate_insert_sql(PROVA_ALUNO[:args.rows], PROVA_ALUNO_SQL_TEMPLATE)

    for filename, lines in sqls.items():
        with open(f'{filename}.sql', 'w+') as file:
            file.writelines(lines)
    
    order = [
        'professor_sql',
        'aluno_sql',
        'turma_sql',
        'prova_sql',
        'turma_aluno_sql',
        'prova_aluno_sql'
    ]

    one_file_sql = [
        ''.join(sqls[key]) + '\n'
        for key in order
    ]
    with open('onefile.sql', 'w+') as file:
        file.writelines(one_file_sql)



