# API de Cartão de Crédito

O objetivo desta aplicação é disponibilizar via APIs REST informações de cartões de crédito. Tal como o CRUD completo para os modelos de Cartão de Credito e Holder.

## Observações

O teste conta com a boa interpretação do leitor, entretanto tentei manter ao máximo com a estrutura apresentada, pois acredito que tudo fazia parte do desafio em si.

- Decidi fazer o Holder como um objeto à parte, e por conta disso, o input para a criação do cartão ficou um pouco mais complicada do que deveria. Em um cenário comum, eu iria sugerir que para o input devessemos utilizar o ID do Holder, e não o nome. Portanto, tomei a liberdade de adicionar uma "regra de negócio" onde sempre será levado em consideração o PRIMEIRO Holder cadastrado com aquele nome em cada de duplicidade. Não é algo que faz sentido no mundo real, mas mantive assim para nao mudar a estrutura do teste.

- Para a criptografia do cartão, decidi usar um HASH de SHA256. Como não estava especificado como deveria ser, escolhi uma criptografia bastante conhecida no mercado e que pode ser usada para quase tudo.

- Todas as APIs (com exceção da api de login) conta uma uma camada de Autenticação e Autorização. É possível criar usuários com diferentes níveis de acesso (para fins do teste, só é possível criar como ADMIN ou NON-ADMIN), sendo autorizado a visualizar/criar/deletar/atualizar somente o ADMIN. 

## Stack utilizada


- Python 3.8 (Linguagem de programação)
- Django 4.1 (Framework principal)
- DRF 3.14 (Paralelo ao Django para a criação das APIs)
- DRF SimpleJWT 5.2.2 (Autenticação)
- DRF-yasg 1.21.5 (Criação do Swagger)
- SQLite 3 (Banco de Dados)

As demais bibliotecas auxiliares podem ser encontradas em `requirements.txt`



## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/luizgtvsilva/credit_card_api.git
```

Entre no diretório do projeto

```bash
  cd credit_card_api
```

Crie um ambiente virtual e depois ative-o

```bash
  python3 -m venv env
  source env/bin/activate
```

Instale a biblioteca personalizada de validação de cartoes.

```bash
pip install git+https://github.com/maistodos/python-creditcard.git@main
```

Instale as dependências

```bash
  pip install -r requirements.txt
```

Crie e atualize o banco de dados

```bash
  python manage.py makemigrations
  python manage.py migrate --run-syncdb
```

Crie um usuário Admin

```bash
  python manage.py createsuperuser
```

Inicie o servidor

```bash
  python manage.py runserver
```

## Testes


O projeto conta com uma cobertura de 92% de testes unitários, você pode verificar no arquivo testes.py.

Rode os comandos abaixo para visualizar o relatório:
```bash
  coverage run --source='.' manage.py test credit_card
```
E logo em seguida rode o comando abaixo e abra o arquivo index.html gerado:
```bash
  coverage html
```


## Documentação da API
Aqui vou detalhar melhor somente como se utiliza os principais endpoints do projeto, as demais pode ser encontrada em `/swagger` uma vez que o projeto estiver rodando.

É aconselhável rodar os endpoints nesta ordem para que não haja nenhum problema de relacionamento entre os Modelos (por exemplo, tentar criar um CC sem um Holder pré-existente) ou problema de autenticação.

#### Login
Somente um ADMIN pode criar outros usuários, portanto é necessário fazer um login com o super user do Django. 

```http
  POST /api/token/
```

| Parâmetro   | Tipo       | Exemplo                           |
| :---------- | :--------- | :---------------------------------- |
| `body` | `json` | { "username": "admin", "password": "admin" } |


#### Criar usuário

```http
  POST /sign-up/
```

| Parâmetro   | Tipo       | Exemplo                           |
| :---------- | :--------- | :---------------------------------- |
| `body` | `json` | { "name": "worker1", "password": "1234",  "role": "NON_ADMIN" } |


#### Cria um Holder

```http
  POST /holders/
```

| Parâmetro   | Tipo       | Exemplo                           |
| :---------- | :--------- | :---------------------------------- |
| `auth` | `token` | Token adINUFB45ab84... |
| `body` | `json` | { "name": "Any Name" } |

#### Cria um cartão de crédito

```http
  POST /credit-cards/
```

| Parâmetro   | Tipo       | Exemplo                           |
| :---------- | :--------- | :---------------------------------- |
| `auth` | `token` | Token adINUFB45ab84... |
| `body` | `json` | { "exp_date": "03/2026", "holder":"Any Name", "number": "4539578763621486", "cvv": "1234" } |






## Melhorias à curto prazo

- Estrutura do projeto: separar os modelos, serializers e views em sub-pastas para cada Entidade.
- Performance: adicionar caching com Redis para os endpoints.
- Dockerizar a aplicação
