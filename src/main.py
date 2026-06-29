import os
from processor import processar_pipeline

def main():
    # Caminho dinâmico para evitar problemas de diretório
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # TODO: Baixe uma spritesheet, salve na pasta dataset e mude o nome do arquivo aqui
    nome_arquivo = "Nintendo 64 - Paper Mario - Non-Playable Characters - Toad (Red).png"
    caminho_input = os.path.join(BASE_DIR, "dataset", nome_arquivo)
    
    print("=== Iniciando Smart Tileset Processor ===")
    try:
        processar_pipeline(caminho_input)
    except Exception as e:
        print(f"[ERRO] Falha no processamento: {e}")

if __name__ == "__main__":
    main()