# Open Data Platform

- [Problema](#problema)
- [Motivação](#motivação)
- [Arquitetura](#arquitetura)
- [Solução](#solução)
- [Documentação](./doc/readme.md)

## Problema

- Não há ferramentas open source no mercado que provê plataformas de dados de ponta-a-ponta
- Há diversas ferramentas no mercado com propósitos específicos em cada área da engenharia de dados
- As ferramentas existentes não permitem a personalização e
- Integram apenas com ferramentas dos próprios provedores

## Motivação

- Plataforma de dados centralizada
- Solução com tecnologias open-source
- Liberdade de personalização de ferramentas

## Solução

Criar uma plataforma de dados centralizada utilizando ferramentas open-source, capaz de prover a criação de pipelines ETL em batch e em tempo real e também ferramentas para análise dos dados armazenados no Data Lake.

## Arquitetura

![Initial archtecture](./doc/images/architecture.jpeg)

## Como executar este projeto

Primeiramente construa todas imagens docker, executando

```bash
./build_images.sh
```

Suba todos os containers

```bash
docker-compose -f docker-compose.yml -f kafka/docker-compose.yml -f ingestion/docker-compose.yml up
```
