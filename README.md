Desafio Técnico - Analista de Teste (SIA Tecnologia)

## Candidato
Nome: Antonio de Oliveira Filho
Função: Analista de Teste
Data da Entrega: 30/01/2025

Resumo Executivo da Entrega

O Plano de Testes foi executado com sucesso e revelou que a aplicação **não possui a qualidade e a estabilidade necessárias** para avançar para a próxima fase de desenvolvimento. A análise cobriu rigorosamente os requisitos funcionais, a conformidade visual e a segurança.

### Principais Achados:

1.  **Integridade de Dados Crítica:** Foram identificadas falhas de validação de campo que permitem a persistência de dados inválidos (como formatos de identificação incorretos e datas ilógicas), comprometendo a integridade do banco de dados.
2.  **Segurança Crítica:** O sistema não exige autenticação (login) para acesso total às funcionalidades, configurando uma grave falha de segurança que expõe o sistema a riscos.
3.  **Usabilidade e Design:** O layout é inconsistente com o Protótipo de Referência (divergências em cores, fontes e espaçamento) e apresenta falhas de **responsividade** que quebram a visualização em dispositivos móveis.
4.  **Funcionalidades Bloqueadas:** Componentes essenciais de navegação (como Menus e Barras Laterais) estão inoperantes, impedindo o usuário de executar funções básicas como a **edição e exclusão** de registros.

---

## 📂 Organização dos Artefatos

Todos os documentos e evidências estão organizados nas seguintes pastas:

* ### 1_DOCUMENTACAO/
    * Contém o **Plano de Testes Final** (em $\text{PDF}$), que inclui a estratégia, Casos de Teste (CTs) e o Relatório de Bugs detalhado.

* ### 2_EVIDENCIAS/
    * Contém as imagens (screenshots) que comprovam todos os Bugs Funcionais, Não Funcionais e de Segurança encontrados durante os testes.

* ### 3_AUTOMACAO/
    * Contém o script de automação desenvolvido para testes focados nas validações críticas (se o arquivo tiver sido adicionado).

---
