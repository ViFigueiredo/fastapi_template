# Configurar ambiente e instalar as bibliotecas

...

# Executar e iniciar as migrações

export FLASK_APP=./configs/migrate.py
flask db init
flask db migrate -m "mensagem de commit"
flask db upgrade

# Atualizar e criar novas migrações

export FLASK_APP=./configs/migrate.py
flask db stamp head
flask db migrate -m "msg:"
flask db upgrade

# Reverter as migrações

flask db downgrade -1 (quantidade de reversões)

# Em casos de erros de upgrade ou downgrade, verificar dependências e removê-las se necessário

ALTER TABLE [nome_tabela] DROP CONSTRAINT [nome_contraint]; (remover para aplicar a migração e depois recriar com o sql abaixo)
ALTER TABLE [nome_tabela] ALTER COLUMN [nome_coluna] VARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AI NOT NULL; (recria de acordo com o tipo e colação de cada uma)

