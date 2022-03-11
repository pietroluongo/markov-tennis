# markov-tennis
Trabalho da disciplina de Processos Estocásticos que modela jogos de tênis usando cadeias de Markov

## Instalação

É recomendado usar um **virtual env** para organização de dependências do projeto. Um tutorial simples para a instalação do *pip* e do *virtual env* está disponível [neste link](http://timsherratt.org/digital-heritage-handbook/docs/python-pip-virtualenv/).

Com o ambiente criado e ativado, basta executar o comando `pip install -r requirements.txt`, que instala as bibliotecas e dependências necessárias para a execução do projeto.

## Execução
Para executar uma simulação, basta executar o comando

```
make
```
ou

```
python tennis/main.py
```


para executar uma simulação usando as definições padrão.

A execução do comando

```
python tennis/main.py -h
```

permite analisar as possíveis _flags_ de execução do projeto.

Por fim, a execução do comando

```
python tennis/main.py --analyze --path caminho/para/datasets
```

Onde a pasta `caminho/para/datasets` contém uma quantidade de arquivos `.JSON` dentro, gerados pelo próprio programa, faz a análise dos resultados simulados.


## Documentação
O projeto conta com documentação embutida gerada a partir do código. Para acessar, basta executar

```
make docs-live
```

para iniciar um servidor local na porta 8080 com a documentação do projeto, ou

```
make docs
```

para gerar arquivos .html estáticos com a documentação.

Alternativamente, a documentação pré-compilada está disponível na pasta `docs`.
