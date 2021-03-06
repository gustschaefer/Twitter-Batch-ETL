# Twitter Batch ETL

ETL que encontra os trending topics do Twitter em cinco países (Inglaterra, Brasil, Alemanha, Canadá, EUA e Suécia), coleta tweets (dez por padrão) relacionados a cada tópico, realiza transformações para capturar os principais dados de cada tweet, salva os dados em formato json e os converte para parquet. Após isso, os arquivos (json e parquet) são enviados para um bucket no Amazon S3.


<p align="center">
 <img src="./assets/etl-diagram.png">
</p>


Confira os gráficos do Airflow (Grapth View e Tree View) que representam o pipeline:

<div align="center">
 <img src="./assets/airflow-graphView.png">
 <p>Graph View</p>
</div>

<div align="center">
 <img src="./assets/airflow-tree-view.png">
 <p>Tree View</p>
</div>

Com os dados salvos, você pode conferir os arquivos json e parquet em seu bucket.

<div align="center">
 <img src="./assets/s3-json-folder.png">
 <p>Arquivos json: TweetsData-COUNTRY-yyyy-mm-dd.json</p>
</div>

Os arquivos **parquet** são salvos na estrutura *TweetsData-COUNTRY-yyyy-mm-dd/file.parquet*

<div align="center">
 <img src="./assets/s3-parquet-folder.png">
 <p>Pastas parquet: TweetsData-COUNTRY-yyyy-mm-dd/</p>
</div>

<div align="center">
 <img src="./assets/parquet-crc.png">
 <p>Arquivos parquet: file.parquet e file.crc</p>
</div>

## Dependências e Executar o projeto

- Uma conta configurada no [twitter para desenvolvedores](https://developer.twitter.com/en)
- Adicione suas credenciais do Tweepy no arquivo de configuração *(DAG/ETL_scripts/config.py)*. As credenciais são fornecidas após a criação da conta (passo acima): *consumer_key, consumer_secret, access_token e access_token_secret*
- Instale o [Docker](https://docs.docker.com/engine/install/ubuntu/) e [docker-compose](https://docs.docker.com/compose/install/)
- Crie uma conta na [AWS](https://aws.amazon.com/pt/free/) se ainda não possui (pode ser free tier)
- Instale o [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)
- Crie e configure o seu [Bucket S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html)
- Modifique o *bucket_name* no arquivo de configuração *(DAG/ETL_scripts/config.py)* para o seu (criado no passo acima)

Após isso, execute o seguinte comando para criar o arquivo de configuração das suas credenciais da AWS, que serão salvas no caminho *~/.aws* e posteriormente usadas no container (ver volumes em *docker-compose.yml*):

```bash
$ aws configure
```

Finalmente, use os seguintes comandos:

```bash
$ git clone https://github.com/gustschaefer/Twitter-Batch-ETL
$ cd Twitter-Batch-ETL/
$ docker-compose up -d
```

Após o proceso terminar, acesse [http://localhost:8080/](http://localhost:8080/) para entrar na interface gráfica do Airflow.

O comando **docker-compose up -d** cria os containers necessários para o projeto, com seus volumes e variávies. Se desejar **instalar mais algum pacote**, adicione-o no arquivo *requirements.txt* e utilize o seguinte comando para reconstruir seus containers:

```bash
$ docker-compose up --build
```


