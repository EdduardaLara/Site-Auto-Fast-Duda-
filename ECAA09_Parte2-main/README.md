# ECAA09 Parte2
Segunda parte do projeto Django para a disciplina ECAA09

# Proposta da Atividade (deixar mais claro a avaliação)

- Criar tela de cadastro/registro personalizada indicando se é cliente ou oficina
- No dashboard de cliente cadastrar de problema com upload de imagem
- No dashboard de cliente listar os cadastros de problemas e se tem oficina interessada
- No dashboard de oficina selecionar um problema cadastrado pelo cliente
- No dashboard de oficina listar problemas selecionados

## Resultados do Gemini 3 
[Chat de Geração do Projeto no Gemini 3 Pro](https://gemini.google.com/share/689d84d7820e)

## Primeiro Uso

Criar ambiente virtual e ativá-lo:

```bash
python -m venv .venv

# Ativar no Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

Criar banco de dados com modelos:
```bash
# Criar tabelas do core
python manage.py makemigrations core
# Criar tabelas de atenticação do django
python manage.py migrate
# criar super usuário
python manage.py createsuperuser
```

Rodar servidor de debug:
```bash
python manage.py runserver
```
