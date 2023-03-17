# developersandgames_withelasticsearch

```terminal

$ docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.0

```

Eğer memory az geliyor ise

--memory=1Gb

parametresini ekleyebilirsiniz.
