# Twitter Batch ETL

**ESTE É UM PROJETO EM ANDAMENTO / THIS IS A WORK IN PROGRESS**

Atualmente é possível extrair os dados em formato json, envialos para o S3 na estrutura: *trending_tweets/TweetsData-COUNTRY-yyyy-mm-dd.json* e remover os arquivos locais. Apenas a conversão para parquet não foi feita, pois esse processo é executado pelo PySpark no container do Airflow, o que está gerando alguns erros de compatibilidade e timeout.

Para rodar o projeto:

- Uma conta configurada no [twitter para desenvolvedores](https://developer.twitter.com/en)
- Adicione suas credenciais do Tweepy no arquivo de configuração *(DAG/ETL_scripts/config.py)*. As credenciais são fornecidas após a criação da conta (passo acima): *consumer_key, consumer_secret, access_token e access_token_secret*
- Instale o [Docker](https://docs.docker.com/engine/install/ubuntu/) e [docker-compose](https://docs.docker.com/compose/install/)
- Crie uma conta na [AWS](https://aws.amazon.com/pt/free/) se ainda não possui (pode ser free tier)
- Instale o [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)
- Crie e configure o seu [Bucket S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
- Modifique o *bucket_name* no arquivo de configuração *(DAG/ETL_scripts/config.py)* para o seu (criado no passo acima)

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


