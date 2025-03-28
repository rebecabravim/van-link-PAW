# Manual de Gerenciamento de Branches e Commits

## Introdução

Para manter a organização e o controle sobre o desenvolvimento do projeto, utilizaremos um fluxo de trabalho específico para o gerenciamento de branches e commits no Git. 
Este manual descreve o processo que cada membro da equipe deve seguir ao trabalhar em novas funcionalidades ou correções de bugs e ao preparar código para a produção.

## Fluxo de Trabalho

### 1. Criando uma Nova Branch

Antes de começar a trabalhar em qualquer alteração no código, é necessário criar uma nova branch baseada na branch develop. 
Dependendo do tipo de trabalho, as branches seguirão um padrão de nomenclatura específico:

- *Para uma Nova Funcionalidade:*
  - Crie uma branch do tipo back-end(front-end)/[nome-da-funcao].
  - Exemplo de comando:
    ```
    git checkout main
    git pull origin main
    git checkout -b back-end(front-end)/[nome-da-funcao]
    ```

### 2. Instale as novas dependências do projeto

Antes de começar a trabalha, troque para o powershell. Após isso, ative o ambiente virtual e instale as novas bibliotecas.

```
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Finalizando fluxo de trabalho
- *Não se esqueça das novas bibliotecas:*

  Lembre-se sempre de manter o arquivo das dependências do projeto atualizado, com as novas bibliotecas que você instalou.
  ```
  pip freeze > requirements.txt
  ```

- *Comite as Alterações:*
  ```
  git add .
  git commit -m "Descrição das alterações realizadas no imperativo. Ex: Cria funções de CRUD de Usuários"
  git checkout main
  git pull origin main
  git checkout back-end(front-end)/[nome-da-funcao]
  git merge main
  ```
     
- *Finalizando nossa funcionalidade:*
  - Vamos fazer um Pull Request
    ```
    git push origin back-end(front-end)/[nome-da-funcao]
    ```

    - Após fazer isso você vai notar uma notificação no seu repositório sugerindo um Pull Request
    

    - Basta clicar em "compare & pull request" e fazer o merge da sua branch
      

    - depois do merge o Github te pergunta se você deseja deletar a branch, clique para deletar a branch
    
  - Deletando a branch local:
    ´´´
    git checkout develop
    git pull origin develop
    git branch -d back-end(front-end)/[nome-da-funcao]
    ´´´


# Comandos para rodar o app web atraves de um ambiente virtual:


## 1. Iniciar ambiente virtual
```
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

## Instalar bibliotecas
Podemos instalar todas de uma vez com o comando:
```
pip install -r requirements.txt
```

Sempre que instalarmos uma biblioteca nova, devemos rodar o seguinte comando:
```
pip freeze > requirements.txt
```
O comando acima sobrescreve o arquivo requirements.txt com todas as novas biblioteca instaladas.

Se preferir, pode instalar as bibliotecas uma por uma. Segue abaixo a lista de algumas bibliotecas instaladas até o momento:
```
py -m pip install --upgrade pip
pip install flask
pip install ipython
pip install flask-wtf
pip install werkzeug
pip install flask-login
pip install flask-sqlalchemy flask-migrate
```

## Rodar
```
set FLASK_APP=van-link-paw.py
$env:FLASK_DEBUG = 1
flask run
```
## Inicio BD
```
pip install flask-sqlalchemy flask-migrate
flask db init
```
Segurança:
```
pip install werkzeug
pip install flask-login

