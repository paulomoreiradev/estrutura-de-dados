# 📦 Sistema de Controle de Estoque Avançado — Estrutura de Dados 2025.1

## 🌟 Visão Geral

Este projeto representa um sistema completo de gerenciamento de estoque desenvolvido em **Python** como trabalho final da disciplina de **Estrutura de Dados (2025.1)**. O sistema implementa operações complexas de estoque utilizando **estruturas de dados customizadas**, com foco especial em **eficiência e robustez**.

---

## 🚀 Funcionalidades Principais

### 📋 Gestão de Produtos

- Cadastro completo de produtos (código, nome, quantidade, preço, validade)
- Atualização dinâmica de estoque
- Controle de lotes com diferentes datas de validade
- Validação rigorosa de dados de entrada

### 💰 Operações Comerciais

- Sistema de vendas inteligente:
  - Prioriza produtos não vencidos
  - Utiliza múltiplos lotes quando necessário
- Gera relatórios detalhados
- Cálculo automático de faturamento total

### 🔍 Ferramentas de Análise

- Identificação e remoção de produtos vencidos
- Consultas flexíveis por:
  - Código do produto
  - Nome (busca parcial)
  - Status de validade
- Relatórios consolidados de vendas

---

## 🛠️ Funcionalidades Técnicas

- Persistência de dados em **JSON**
- Sistema de tratamento de erros robusto
- Interface intuitiva com menus hierárquicos

---

## 🧠 Arquitetura e Estruturas de Dados

### ⛓️ Lista Encadeada Customizada (LinkedList)

Implementação completa com:

- Inserção/remoção em O(1) no início e fim
- Busca e navegação eficiente
- Controle automático de tamanho
- Métodos especiais para representação

### 📊 Sistema de Armazenamento

- Dicionário otimizado com **LinkedList como valor**
- Controle de múltiplos lotes por produto
- Serialização/deserialização para JSON

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.9+
- **Estruturas de Dados**:
  - Lista Encadeada Simples (implementação manual)
  - Dicionários para indexação rápida
- **Persistência**: JSON para armazenamento
- **Testes**: `unittest` (em desenvolvimento)

---

## 👨‍💻 Equipe de Desenvolvimento

| Integrante                              | Matrícula | Responsabilidades                                           |
|----------------------------------------|-----------|-------------------------------------------------------------|
| Paulo Roberto Nunes Moreira Filho      | 555020    | Arquitetura de dados, implementação das estruturas, lógica de negócios |
| Paulo Vitor Angelo Silveira            | 387388    | Interface do usuário, sistema de menus, integração          |

---

## 📥 Instalação e Execução

### Pré-requisitos

- Python 3.9 ou superior

### 🖥️ Execução Local

```bash
# Execute o sistema
python main.py
