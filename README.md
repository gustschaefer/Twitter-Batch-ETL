# Twitter Batch ETL

**ESTE É UM PROJETO EM ANDAMENTO/WORK IN PROGRESS...**

Atualmente é possível extrair os dados em formato json, envialos para o S3 na estrutura: *trending_tweets/TweetsData-COUNTRY-yyyy-mm-dd.json* e remover os arquivos locais. Apenas a conversão para parquet não foi feita, pois esse processo é executado pelo PySpark no container do Airflow, o que está gerando alguns erros de compatibilidade e timeout.

Para rodar o projeto:

- Instale o Docker e docker-compose
- Crie uma conta na AWS se ainda não possui
- Instale o aws cli
- Crie e configure o seu Bucket S3
- Modifique o *bucket_name* do arquivo de configuração *(DAG/ETL_scripts/config.py)* para o seu (criado no passo acima)

Após isso, execute o seguinte comando para criar o arquivo de configuração das suas credenciais da AWS:

```bash
$ aws configure
```

Finalmente, use os seguintes comandos:

```bash
$ git clone https://github.com/gustschaefer/Twitter-Batch-ETL
$ cd Twitter-Batch-ETL/
$ docker-compose up -d
```

O comando **docker-compose up -d** cria os containers necessários para o projeto, com seus volumes e variávies. Se desejar instalar mais algum pacote, adicione-o no arquivo *requirements.txt* e utilize o seguinte comando para reconstruir seus containers:

```bash
$ docker-compose up --build
```


