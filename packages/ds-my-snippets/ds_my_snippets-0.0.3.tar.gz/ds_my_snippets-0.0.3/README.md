# DS Snippets

Trechso de código úteis sobre DataScience

Autor: Rafael Morais de Assis

## Como criar nova versão

Instalar aqui e testar
pip install -e .

## Como atualizar o pacote

=> (mandar para o test-py)
twine upload --repository-url https://test.pypi.org/legacy/ dist/* 
=> mandar para Pypi (pip
python -m twine upload dist/*


## Como usar

Instalar com pip
+ Use `!` se estiver no colba/kaggle
````
!pip install ds-my-snippets
````

Chamando
````
import ds_my_snippets as ds
````

Trecho que funciona

````
import pandas as pd
import seaborn as sns
import ds_my_snippets as ds

iris = sns.load_dataset('iris')
iris = ds.reduce_mem_usage(iris)
````

Chamando todas as funções
````
dir(ds) # lista todas as funçôes do módulo
````
