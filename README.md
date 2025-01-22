# API para Gerenciador de Tarefas - Boilerplate 
Projeto de API em python para servir como boiler-plate com boas praticas de codigo e arquitetura. 


## Lista de tecnologias usadas:
 
- Python: FastAPI, Pydantic, SQLAlchemy, Alembic, Poetry, Pytest
- Docker
- Postgres
- Arquitetura: DDD, Clean Architecture, SOLID, UNIT OF WORK, REPOSITORY PATTERN, Event Driven Design
- Testes: Unitarios, Integração, E2E
- CI/CD: Github Actions

## TODO:

- [x] Refatorar testes unitarios
- [ ] Mudar nome do projeto no github
- [ ] Adicionar sistema de envio de email
- [ ] Adicionar evento de envio de email
- [ ] Criar Dockerfile para containirizar a aplicação  
- [ ] Criar docker-compose para subir a aplicação  
- [ ] Criar testes de integração e E2E
- [ ] Aprimorar Github Actions e conectar com a maquina teste
- [x] Mudar camada de repositorio para usar interface entre a camada de dominio e infraestrutura
- [ ] Implementar sistema de cache(Talvez muito complexo para um projeto já complexo demais até)
- [ ] Implementar sistema de logs
- [x] Mudar querys para não exibir itens desativados
- [ ] Implementar version ao realizar execuções de comandos no banco de dados
- [ ] Fazer Front

## Requisitos

- Python 3.11
- Poetry
- Docker se for usar o container

## Instalação

Clonar repositorio e instalar dependencias:

```sh
git clone https://github.com/BrunoSiqueiraEstrela/gerenciador_de_tarefas
cd gerenciador_de_tarefas
poetry install
```

## Uso

### Rodando a aplicação pelo containers

- TODO

### Rodando a aplicação localmente

Prencher o arquivo .env com as variaveis de ambiente


```sh
poetry run uvicorn app.main:app --reload

```
## Testes

```sh
poetry run pytest
```

## Inspirações:

CosmicPython: https://www.cosmicpython.com/book/chapter_01_domain_model.html

## Licença

* TODO
* mas pode forkar a vontade
