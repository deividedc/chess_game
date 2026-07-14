
# Jogo de Xadrez 

Este é um jogo de xadrez jogável através do terminal, desenvolvido em Python. O projeto foi construído como critério avaliativo para a disciplina de **Engenharia de Software**, com foco prático no design de arquitetura de software orientada a objetos.

O principal objetivo deste projeto é demonstrar a aplicação rigorosa dos princípios **SOLID** e de **Padrões de Projeto (Design Patterns)** para criar um código limpo, de fácil manutenção, testável e altamente extensível.


## Estrutura do Projeto

A arquitetura do projeto segue uma divisão modular clara e desacoplada, separando a lógica das peças da gestão do tabuleiro e do fluxo principal do jogo.

```text
.
├── board/
│   ├── board.py          # Representa o tabuleiro (matriz, colisões, xeque, roque, etc.)
│   └── __init__.py
├── pieces/
│   ├── piece.py          # Classe abstrata/base para todas as peças
│   ├── pawn.py           # Comportamento específico do Peão (inclui En Passant)
│   ├── rook.py           # Comportamento específico da Torre
│   ├── knight.py         # Comportamento específico do Cavalo
│   ├── bishop.py         # Comportamento específico do Bispo
│   ├── queen.py          # Comportamento específico da Rainha
│   ├── king.py           # Comportamento específico do Rei (inclui Roque e salvaguardas de xeque)
│   └── __init__.py
├── main.py               # Fluxo de execução (Game Loop), controle de turnos e inputs
└── README.md

```


---

## Como o Projeto foi Estruturado e Construído

O projeto foi arquitetado sob a filosofia de **atribuição estrita de responsabilidades**.

### 1. Aplicação dos Princípios SOLID

* **S - Single Responsibility Principle (Princípio da Responsabilidade Única):**
* Cada classe de peça (`Pawn`, `Rook`, etc.) é responsável única e exclusivamente por validar se um movimento é geometricamente compatível com suas regras de movimento originais.
* A classe `Board` cuida apenas da estrutura matricial de 8x8, colisões de caminho (`is_path_blocked`), mapeamento físico de xeques (`is_square_under_attack`) e simulações de jogadas.
* O arquivo `main.py` é o orquestrador do jogo, lidando apenas com a interação do usuário, input/output e transição de turnos.


* **O - Open/Closed Principle (Princípio Aberto/Fechado):**
* Se decidirmos criar uma nova peça não convencional para o xadrez (como uma peça customizada de variantes do xadrez), não precisamos modificar o tabuleiro (`Board`) ou o fluxo do jogo (`main.py`). Basta herdar da classe base `Piece` e implementar o método `is_valid_move()`. O sistema está fechado para modificações, mas aberto para extensões.


* **L - Liskov Substitution Principle (Princípio da Substituição de Liskov):**
* Todas as peças concretas estendem a classe abstrata `Piece`. No tabuleiro, qualquer chamada de validação ou captura trata os objetos de forma polimórfica através do tipo genérico `Piece` (ex: `isinstance(piece, Piece)`), garantindo que qualquer subclasse possa substituir sua classe pai sem quebrar o comportamento do sistema.


* **I - Interface Segregation Principle (Princípio da Segregação de Interfaces):**
* Embora Python não use interfaces nativas estritas como Java, o princípio é respeitado ao mantermos as classes base leves. A classe `Piece` expõe apenas o contrato essencial de que todas as peças precisam (ex: cor, posição, se já se moveu e validação de movimento), sem forçar implementações de comportamentos desnecessários em subclasses.


* **D - Dependency Inversion Principle (Princípio da Inversão de Dependência):**
* A classe `Board` não depende de implementações de baixo nível para realizar certas tarefas complexas; em vez disso, o fluxo de jogo injeta e utiliza abstrações. As validações de jogadas de cada peça recebem o próprio tabuleiro (`board`) como parâmetro, invertendo o controle e permitindo que as peças verifiquem o estado geral do jogo sem criar dependências circulares rígidas.



### 2. Padrões de Projeto (Design Patterns) Utilizados

* **Template Method:**
* Utilizado na relação entre a classe abstrata `Piece` e as suas subclasses. A classe pai estabelece a estrutura base das peças e inicializa propriedades comuns, enquanto delega os detalhes do algoritmo de validação de movimento (`is_valid_move`) para ser implementado individualmente em cada subclasse concreta.


* **Polimorfismo e Encapsulamento:**
* O tabuleiro gerencia os movimentos sem precisar saber se a peça selecionada é um Bispo ou um Cavalo. Ao disparar `piece.is_valid_move(...)`, o interpretador resolve dinamicamente qual regra executar.


* **Prevenção de Recursão Infinita (Algoritmo de Salvaguarda):**
* Para evitar loops infinitos onde o Rei A pergunta se o Rei B o está atacando (gerando estouro de pilha na chamada do `is_square_under_attack`), foi aplicada uma verificação matemática local de proximidade radial para ataques originados de Reis inimigos, protegendo o ciclo recursivo do motor.




---

##  Como Executar o Jogo

Certifique-se de possuir o Python 3.10 ou superior instalado em sua máquina.

1. Clone o repositório:
```bash
git clone [https://github.com/seu-usuario/chess_game.git](https://github.com/seu-usuario/chess_game.git)

```


2. Navegue até a pasta do projeto:
```bash
cd chess_game

```


3. Execute o arquivo principal:
```bash
python3 main.py

```
