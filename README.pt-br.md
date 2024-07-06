# Exemplo de Cifra de César

Este repositório contém um exemplo de Cifra de César, uma técnica antiga de criptografia. A Cifra de César desloca letras por um número fixo de passos no alfabeto. Este projeto foi criado para demonstrar técnicas básicas de criptografia usando Python, Flask e Docker, juntamente com práticas de integração e entrega contínuas usando GitHub Actions. Além disso, o aspecto de implantação abrange uma configuração simples de Kubernetes usando K3S na AWS.

### Requisitos

* Ambiente de desenvolvimento Python3 funcional.
* Ambiente Docker funcional para construção e uso de imagem (opcional).
* Conta no GitHub para execução de workflow (opcional).
  * Este repositório e um [repositório de manifestos](https://github.com/cicerowordb/caesar-cipher-manifests) equivalente.
  * Incluir secrets: `secrets.DOCKER_USERNAME`, `secrets.DOCKER_PASSWORD` e `secrets.MANIFESTS_REPOSITORY_AUTH_URL`.
  * Para `secrets.MANIFESTS_REPOSITORY_AUTH_URL` use o formato: `https://USER:TOKENT@github.com/cicerowordb/caesar-cipher-pipeline.git`.
* Cluster Kubernetes. Utilizando K3S operando na AWS (opcional).

### Executando localmente sem Docker

Para testar e desenvolver localmente sem a necessidade de Docker, você pode configurar e rodar a aplicação diretamente no seu ambiente de desenvolvimento Python. Isso é especialmente útil para desenvolvedores que querem rapidamente fazer alterações e testar funcionalidades sem passar pelo processo de construção de imagens Docker. Siga os passos abaixo para configurar e executar a aplicação:

```bash
# criar ambiente virtual
python3 -m venv development
source development/bin/activate

# instalar requisitos da aplicação
pip install -r requirements.txt

# executar aplicação
gunicorn --bind 0.0.0.0:5000 --workers 4 index:app

# acessar e fazer seus testes manuais
# verifique as imagens nas próximas seções

# parar com control+c

# desativar ambiente virtual
deactivate
```

### Construindo e executando com Docker

Construa uma imagem Docker da aplicação Cifra de César usando a base de código mais recente e execute localmente para garantir que tudo esteja empacotado corretamente.

```bash
# construir imagem docker
docker build -t caesar-cipher:$(head -n1 CHANGELOG.md|tr -d "# ") .

# executar imagem docker
docker run -d --name caesar-cipher -p 5000:5000 caesar-cipher:$(head -n1 CHANGELOG.md|tr -d "# ")

# executar um shell dentro de um contêiner
docker exec -it caesar-cipher bash

# remover contêiner docker
docker rm caesar-cipher --force
```

### Resultados dos testes manuais

Aqui estão os resultados dos testes manuais para demonstrar a funcionalidade da Cifra de César. Os testes confirmam que os processos de criptografia e descriptografia são tratados corretamente pela aplicação. Abaixo estão capturas de tela mostrando a UI da aplicação antes e após uma operação de cifra.

* Antes de enviar:

  ![before-send](img/doc001.png)

* Após enviar:

  ![after-send](img/doc002.png)

### Testes manuais com cURL

Abaixo estão vários comandos de teste manual usando curl para demonstrar a resposta da aplicação a diferentes entradas e deslocamentos. Esses comandos testam a lógica de criptografia com várias entradas de string e valores de deslocamento, verificando tanto a funcionalidade da aplicação quanto seu tratamento de erros.

```bash
curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=123abcABC&shift=1' \
    | grep -E '(Encrypted Text:|HTTP/)'
# esperado: 234bcdBCD

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=234bcdBCD&shift=-1' \
    | grep -E '(Encrypted Text:|HTTP/)'
# esperado: 123abcABC

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=HELLO&shift=2' \
    | grep -E '(Encrypted Text:|HTTP/)'
# esperado: JGNNQ

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=staySafe&shift=0' \
    | grep -E '(Encrypted Text:|HTTP/)'
# esperado: staySafe

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=abc123!@#&shift=1' \
    | grep -E '(Encrypted Text:|HTTP/)'
# esperado: bcd234!@#

curl -isS -X POST http://localhost:5000/ \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'text=&shift=1' \
    | grep -E '(Encrypted Text:|HTTP/)'
# esperado: 
```

### Executando testes unitários

Execute os seguintes comandos para executar testes unitários para a aplicação Cifra de César. Estes testes garantem que a funcionalidade de criptografia e descriptografia funcione como esperado.

```bash
# instalar bibliotecas de teste
pip install -r requirements-test.txt

# executar testes unitários da pasta raiz do repositório
export PYTHONPATH=$PWD
pytest -s
```

### Executando verificações estáticas

Realize análise estática para garantir a qualidade do código, segurança e segurança das dependências usando as ferramentas Pylint, Safety e Bandit.

#### Lint com Pylint

Verifique o código Python por erros estilísticos e padrões de programação. Isso ajuda a manter a qualidade e consistência do código em todo o projeto.

```bash
pylint --fail-under=9 *.py
```

#### Verificar dependências com Safety

Garanta que não há vulnerabilidades conhecidas nas dependências especificadas no arquivo `requirements.txt`.

```bash
safety check -r requirements.txt
```

#### Verificar segurança com Bandit

Realize uma análise de segurança para encontrar problemas de segurança comuns no código Python. Isso é importante para manter uma aplicação segura.

```bash
bandit *.py
```