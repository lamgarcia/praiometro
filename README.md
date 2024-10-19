# 1. Repositório de Código
O Projeto

O nome do projeto é Praiômetro, onde o cliente pode verificar quais as praias com melhores condições meteorológicas do Brasil a cada mês do ano. A ferramenta utiliza dados das estações meteorológicas do INMET como a média de temperatura, precipitação e frequência das chuvas.

O projeto foi feito por mim, no início deste ano, para facilitar os destinos a serem escolhidos nas minhas férias. É inspirado nas tabelas de melhores praias do site https://www.viajenaviagem.com/praiometro-nordeste-caribe/, mas com melhorias evidentes como dados atualizados direto das estações meteorológicas, iteração com mapas e inclusão de quantidade de dias de chuva.

O projeto até então era apenas um código feito no meu computador, sem git ou versionamento, estruturação de código. Todos os arquivos do projeto estão na raiz de uma pasta que era enviada para a hospedagem. Achei uma ótima ideia utilizá-lo para o trabalho final da disciplina ECD11 /UFRGS do professor Guilhmerme Lacerda e conseguir atualizá-lo com mais frequência.

## Repositório
Criado repositório: https://github.com/lamgarcia/praiometro

## STACK de Desenvolvimento

Streamlit - FrontEnd
Sqlite - Database
Folium - Maps
Pandas - Data Analysis

## Organização do código

Foi criado uma estrutura de pastas: assets (imagens e outros) , data (database e arquivos a serem salvos), tests (para artefato dos testes automatizados).
O código é em python e foi criado uma arquivo requirements.txt para instalar as dependências.
O código principal é o praiometro.py e é chamado a partir do framework Streamlit com o comando streamlit run praiometro.py. 

## Versionamento

Para versionamento será adotada a estrutura abaixo:

Major - Mudas muitos latentes que interferem na compatibilidade de versão  ou disruptiva se comparada com a versão anterior (v2.0.0)
Minor - Mudanças que entregam valor no código existente (v.1.1.0)
Patch - Correção de bugs e manutenções sem entrega de valor aparente.

## Convenções de commits

Utilizando o Conventional Commits (https://www.conventionalcommits.org/en/v1.0.0/)  e considerando a simplicidade do projeto, serão utilizadas as seguintes convenções de commits::

feat: para adicionar nova funcionalidade
fix: corrigir bugs
chore: para outras tarefas de manutenção 

## Estruturação de Branches

Será utilizado Trunk-Based Developement, com uma branch principal (main) e duas branch de vida curta feature para novas funcionalidades e hotfix para correções e manutenções . Essa estrutura proporciona rápida integração e entrega contínua. 

O nome da branch deve indicar a alteração que será feita, por exemplo, “feature\novo-mapa-de-temperatura” ou “hotfix\corrigindo-menu-meses”.

# 2. Build 

No GitActions foi construindo um workflow (.github\workflows\main.yml) que é acionado a cada push e pull nas branches main, feature e hotfix. A execução da build será em ubuntu. Também configurou-se a versão do python, a instalação de dependências e o teste automatizado com pytest.

# 3. Testes automatizados

No pipeline de CI foram incluídos os testes automatizados utilizando a ferramenta pytest. Na pasta tests foi criado um python (test_get_ip_visitors.py) para testar a função get_ip_visitors do código principal. Essa função salva o IP do usuário que visitou o site e o teste consiste em verificar se é trazido um IP válido.

Os testes são executados a cada mudança do repositório. 

# 4. Análise de qualidade de código

Para análise de qualidade de código no Pipeline foi utilizado o Flake8. A configuração e exceções foram colocadas no arquivo setup.cfg.

# 5. Deploy
O deploy automatizado ainda não foi realizado na estrutura de VPS  na empresa contratada.

## Demo
Mas uma demo da aplicação pode ser vista em: http://praiometro.com.br/

## Dependências para execuções locais
pip install -r requirements.txt

##  Como executar
streamlit run praiometro.py
Abra a aplicação no navegador: http://127.0.0.1:8502/
