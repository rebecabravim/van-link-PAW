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
    ```
    git checkout main
    git branch -d back-end(front-end)/[nome-da-funcao]
    ```


# Comandos para rodar o app web atraves de um ambiente virtual:


## 1. Iniciar ambiente virtual
```
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

## Instalar dependências
Podemos instalar todas as dependências com o pyproject.toml:
```
pip install -e .
```

## Nos computadores do lab
Instalar a extensão do PowerShell e criar um Script .ps1 contendo:
```
if ( -Not (Test-Path "venv")) {
    py -m venv venv
}
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

. .\venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -e .
```

## Rodar
```
set FLASK_APP=van-link-paw.py
$env:FLASK_DEBUG = 1
flask run
```

## Inicio BD (só na primeira vez)
```
flask db init 
```

## Atualizar o banco de dados
```
flask db migrate -m "initial tables"
flask db upgrade
```

## Segurança:
```
pip install werkzeug
pip install flask-login
```
