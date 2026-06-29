# Smart Spritesheet Processor 🎮🤖

Repositório dedicado ao desenvolvimento de um pipeline automatizado para segmentação, extração e preparação de assets de jogos 2D (pixel art) utilizando técnicas de Processamento Digital de Imagens (PDI).

O projeto foi desenvolvido como parte de atividades acadêmicas na Universidade Federal de Santa Maria (UFSM).

## 🚀 O Problema e a Solução
Processar folhas de sprites (spritesheets) manualmente para o desenvolvimento de jogos pode levar horas. Este software automatiza o mapeamento físico e o fatiamento de cada frame individual através de matrizes matemáticas, devolvendo arquivos `.png` isolados com transparência real (canal alfa).

## 🛠️ O Pipeline de PDI Implementado
O algoritmo processa a imagem original através das seguintes etapas de visão computacional:
1. **Conversão de Espaço de Cores:** Transição do modelo BGR original para o espaço **HSV**, otimizando a segmentação cromática.
2. **Limiarização (Thresholding):** Criação de uma máscara binária isolando o fundo por meio de intervalos de matiz, saturação e brilho.
3. **Morfologia Matemática:** Aplicação de filtros de *Abertura* (remoção de ruídos isolados) e *Fechamento* (preenchimento de lacunas internas).
4. **Ajuste de Borda (Erosão):** Aplicação de uma erosão milimétrica para mitigar artefatos de borda (*fringe pixels*) residuais.
5. **Análise de Componentes Conectados:** Extração de contornos e mapeamento de coordenadas via *Bounding Boxes* para fatiamento físico da matriz colorida.

## 📦 Tecnologias Utilizadas
- Python 3.12
- OpenCV (Open Source Computer Vision Library)
- NumPy (Computação Científica)

## 🔧 Como Executar o Projeto
1. Clone o repositório:
   ```bash
   git clone [https://github.com/RicardoFerreiraDaSilva/smart-spritesheet-processor.git](https://github.com/RicardoFerreiraDaSilva/smart-spritesheet-processor.git)
1.2 Após clonar o repositório crie a ative seu ambiente virtual (venv)
1.3 Instale as dependências atráves de: pip install opencv-python numpy
1.4 Insira a sua folha de sprites na pasta dataset/ e execute: python src/main.py
