# Banco de Dados de Uva, Vinho e Derivados API
## Descrição
Esta API foi desenvolvida para retornar dados sobre a vitivinicultura disponíveis no site 
[Embrapa Uva e Vinho](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01). 
A API facilita o acesso a informações sobre produção, processamento, comercialização, importação e exportação de uvas e seus derivados.
O Objetivo da API é apenas de exibição dos dados.


## Estrutura do Projeto

O projeto está estruturado da seguinte forma:

- main.py: Arquivo principal para configurar e iniciar o aplicativo FastAPI.
- routes.py: Define as rotas da API e a lógica de obtenção de dados.
- auth.py: Arquivo para autenticação e acessos de rotas para usuários
- utils/Scraper/: Diretório contendo as classes de Web Scraping específicas para cada seção do site.
- utils/constants.py: Contém as constantes utilizadas para as opções de botões no scraping.
- utils/csv/: Diretório contendo alternativa de download dos dados, via csv, caso o site esteja fora do ar.


O projeto é uma API para retornar dados de um site. O retorno desses dados primeiramente é realizado a tentativa da busca via Web Scraping de dados, caso o site apresente inconsistência ou esteja sem acesso, irá realizar a busca dos dados via alguns sites de download de csv destes mesmos dados. 
Das duas formas, os dados são transformados para melhor padronização, organização e filtragem.

## Dependências
- FastAPI
- Uvicorn
- python-jose
- bcrypt
- Pydantic
- Pandas
- Requests
- BeautifulSoup4

## Instalação

1. Clone o repositório:

```
git clone https://github.com/PabloPicinini/WebScraping-Embrapa-API.git
cd repositorio
```
2. Crie um ambiente virtual:
```
python -m venv venv
venv\Scripts\activate  # No Windows 
```
3. Instale as dependências:
```
pip install -r requirements.txt
```
4. Execute o aplicativo:
```
uvicorn main:app --reload
```


## Endpoints

### Autorização
- POST /token

    Gera um token JWT para autenticação

    ***Parâmetros de Query:***

    username: username - Required
    password: username - Required

- Exemplo de Uso
    - Requisição
    ```
    curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=admin&password=admin&scope=&client_id=&client_secret='
    ```

    - Resposta
    ```json
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxNjM4ODg4Mn0.q0jBWHl_RTkapJejlLsbqhWxduv_VFxZkSMYB5gp4sg",
  "token_type": "bearer"
  ```

  
- GET /users/me

    Retorna as informações do usuário baseado no token JWT

    ***Parâmetros de Query:***

    No parameters

- Exemplo de Uso
    - Requisição
    ```
    curl -X 'GET' \
  'http://127.0.0.1:8000/users/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxNjM4ODQyNH0.WxUgGKWvL15wxFo95LQI9PuP4leZKaQZ0-1MDN4plJk'
    ```

    - Resposta
    ```json
    {
  "username": "admin",
  "full_name": "Admin Usuário",
  "email": "admin@usuario.com",
  "hashed_password": "$2b$12$XgwIpUItTlcdxFHpZMu.nO2IONkab7xt2Y0Tg4GeFv6ZjKK0a1WB6",
  "disabled": false,
  "permissions": [],
  "is_admin": true
  }
    ```

### Produção
- GET /producao-data

    Retorna dados de produção de uvas.

    ***Parâmetros de Query:***

    start_year: Ano inicial (default: 2020) - Opcional
    end_year: Ano final (default: 2024) - Opcional

- Exemplo de Uso
    - Requisição
    ```
    curl -X 'GET' \
  'http://127.0.0.1:8000/producao-data?start_year=1995&end_year=1997' \
  -H 'accept: application/json'
    ```

    - Resposta
    ```json
    [
    {
    "Produto": "VINHO DE MESA",
    "Classificação": "VINHO DE MESA",
    "Ano": 1970,
    "Quantidade": 217208604
  },
    ...
    ]
    ```
 

### Processamento
- GET /processamento-data

    Retorna dados de processamento de uvas.

    ***Parâmetros de Query:***
    - start_year: Ano inicial (default: 2020) - Opcional
    - end_year: Ano final (default: 2024) - Opcional
    - botao_opcao: Opção do botão (VINIFERA, AMERICANAS_E_HIBRIDA, UVA_DE_MESA, SEM_CLASSIFICACAO) - Opcional e caso seja nulo traz todas as opções

- Exemplo de Uso
    - Requisição com todas as opções
    ```
    curl -X 'GET' \
  'http://127.0.0.1:8000/processamento-data?start_year=2015&end_year=2018' \
  -H 'accept: application/json'
    ```

    - Requisição com uma opção selecionada
    ```
    curl -X 'GET' \
  'http://127.0.0.1:8000/processamento-data?start_year=2015&end_year=2018&botao_opcao=SEM_CLASSIFICACAO' \
  -H 'accept: application/json'
    ```

    - Resposta
    ```json
    [
    {
    "Cultivar": "TINTAS",
    "Classificação": "TINTAS",
    "Ano": 1970,
    "Quantidade": 10448228,
    "Botao": "VINIFERAS"
  },
    ...
    ]
    ```

### Comercialização
- GET /comercializacao-data
    
    Retorna dados de comercialização de uvas.

    ***Parâmetros de Query:***
    - start_year: Ano inicial (default: 2020) - Opcional
    - end_year: Ano final (default: 2024) - Opcional

- Exemplo de Uso
    - Requisição
    ```
    curl -X 'GET' \
  'http://127.0.0.1:8000/comercializacao-data?start_year=2020&end_year=2020' \
  -H 'accept: application/json'
    ```

    - Resposta
    ```json
    [
    {
    "Produto": "VINHO DE MESA",
    "Classificação": "VINHO DE MESA",
    "Ano": 1970,
    "Quantidade": 98327606
  },
    ...
    ]
    ```


### Importação
- GET /importacao-data

    Retorna dados de importação de uvas e derivados.

    ***Parâmetros de Query:***
    - start_year: Ano inicial (default: 2020) - Opcional
    - end_year: Ano final (default: 2024) - Opcional
    - botao_opcao: Opção do botão (VINHOS_DE_MESA, ESPUMANTES, UVAS_FRESCAS, UVAS_PASSAS, SUCO_DE_UVA) - Opcional e caso seja nulo traz todas as opções

- Exemplo de Uso
    - Requisição com todas as opções
    ```
    curl -X 'GET' \
  'http://127.0.0.1:8000/importacao-data?start_year=2010&end_year=2012' \
  -H 'accept: application/json'
    ```

    - Requisição com uma opção selecionada
    ```
    curl -X 'GET' \
  'http://127.0.0.1:8000/importacao-data?start_year=2010&end_year=2012&botao_opcao=VINHOS_DE_MESA' \
  -H 'accept: application/json'
    ```

    - Resposta
    ```json
    [
    {
    "Países": "ALEMANHA",
    "Ano": 2000,
    "Quantidade": 1164724,
    "Valor (US$)": 1668539,
    "Botao": "VINHOS DE MESA"
  },
    ...
    ]
    ```


### Exportação
- GET /exportacao-data

    Retorna dados de exportação de uvas e derivados.

    ***Parâmetros de Query:***
    - start_year: Ano inicial (default: 2020) - Opcional
    - end_year: Ano final (default: 2024) - Opcional
    - botao_opcao: Opção do botão (VINHOS_DE_MESA, ESPUMANTES, UVAS_FRESCAS, SUCO_DE_UVA) - Opcional e caso seja nulo traz todas as opções


- Exemplo de Uso
    - Requisição com todas as opções
    ```
    curl -X 'GET' \
    'http://127.0.0.1:8000/exportacao-data?start_year=2020&end_year=2022&botao_opcao=UVAS_FRESCAS' \
    -H 'accept: application/json'
    ```

    - Requisição com uma opção selecionada
    ```
    curl -X 'GET' \
  'http://127.0.0.1:8000/exportacao-data?start_year=2020&end_year=2022' \
  -H 'accept: application/json'
    ```

    - Resposta
    ```json
    [
    {
        "Países": "ARGENTINA",
        "Ano": 2020,
        "Quantidade": 1015,
        "Valor (US$)": 4176,
        "Botao": "VINHOS DE MESA"
    },
    ...
    ]
    ```


## Autenticação 
A autenticação na API é feita utilizando tokens JWT (JSON Web Tokens). Ao realizar a autenticação, o usuário recebe um token JWT que deve ser incluído nos cabeçalhos das requisições subsequentes para acessar endpoints protegidos.

Para autenticar um usuário e obter um token JWT, o endpoint /login deve ser acessado, fornecendo as credenciais de usuário (nome de usuário e senha) no corpo da requisição. Se as credenciais estiverem corretas, o endpoint retorna um token JWT válido.

Na aplicação atual, foi criado no arquivo auth.py um dicionário simulando um banco de dados fictícios para usuários autenticados, e suas  respectivas permissões. 

No dicionário de usuários fictícios, está presente 3 usuários:
- exemplo_usuario
  - senha: senha
  - permissões: Produção, Processamento.
- outro_usuario
  - senha: outra_senha
  - permissões: Importação, Exportação.
- admin
  - senha: admin
  - permissões: Acesso total

Exemplo de requisição de login:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=admin_usuario&password=admin_senha&scope=&client_id=&client_secret='
```


Exemplo de resposta bem-sucedida:

```
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJleGFtcGxlX3VzZXIiLCJleHAiOjE2Mzg4OTYxMzN9.1Wzf82v9ZXvq4H92L2aO-wZsVYQjNVyFs_Kg3TNOu3Q",
    "token_type": "bearer"
}
```

O token JWT deve ser incluído no cabeçalho Authorization das requisições subsequentes no formato Bearer <token_jwt>.

Exemplo de cabeçalho de autorização:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJleGFtcGxlX3VzZXIiLCJleHAiOjE2Mzg4OTYxMzN9.1Wzf82v9ZXvq4H92L2aO-wZsVYQjNVyFs_Kg3TNOu3Q
```

## Tratamento de Erros:
É possível que o site da Embrapa esteja fora do ar, com isso há uma alternativa automática dentro do arquivo routes.py pela função get_data, que verifica se o site está disponível e realiza 3 tentativas de Web Scraping do site. Caso apresente alguma falha, irá recorrer ao download dos csv's pertinentes à rota escolhida e com seu devido tratamento. 

Alguns dos possíveis erros: 

- 404 Not Found: O recurso solicitado não existe.
- 401 Unauthorized: A autenticação falhou.
