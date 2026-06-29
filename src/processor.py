import cv2
import os
import numpy as np

def carregar_imagem(caminho):
    """Carrega a imagem e valida se o arquivo existe."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Imagem não encontrada em: {caminho}")
    
    imagem = cv2.imread(caminho)
    print(f"[PDI - INFO] Imagem carregada. Resolução: {imagem.shape[1]}x{imagem.shape[0]} | Canais: {imagem.shape[2]}")
    return imagem

def processar_pipeline(caminho_imagem):
    """Executa o pipeline completo de PDI: HSV -> Threshold -> Morfologia -> Recorte."""
    # 1. Leitura
    img_original = carregar_imagem(caminho_imagem)
    
    # 2. Conversão para HSV
    img_hsv = cv2.cvtColor(img_original, cv2.COLOR_BGR2HSV)
    
    # 3. Limiarização (Valores calibrados para o fundo Rosa)
    # Apertando o intervalo: aumentamos o S mínimo (150) e o V mínimo (150)
    # Agora, tons de rosa mais escuros, pastéis ou queimados (do vestido) devem ser ignorados pelo filtro do fundo
    limite_inferior = np.array([140, 150, 150])
    limite_superior = np.array([170, 255, 255])
    mascara_fundo = cv2.inRange(img_hsv, limite_inferior, limite_superior)
    mascara_sprites = cv2.bitwise_not(mascara_fundo)
    
    
    # 4. Operações Morfológicas para limpar imperfeições nas bordas
    kernel = np.ones((3, 3), np.uint8)
    mascara_limpa = cv2.morphologyEx(mascara_sprites, cv2.MORPH_OPEN, kernel)
    mascara_final = cv2.morphologyEx(mascara_limpa, cv2.MORPH_CLOSE, kernel)
    print("[PDI] Filtros morfológicos aplicados com sucesso.")
    # === PARA CONSERTAR PIXEL SOBRANDO ===
    kernel_borda = np.ones((2, 2), np.uint8)
    mascara_final = cv2.erode(mascara_final, kernel_borda, iterations=1)
    print("[PDI] Filtros morfológicos e ajuste de borda (Erosão) aplicados com sucesso.")
    
    # 5. Detecção de Contornos (Análise de Componentes Conectados)
    # Encontra as fronteiras de cada ilha branca na máscara
    contornos, _ = cv2.findContours(mascara_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"[PDI] Total de sprites detectados pelo algoritmo: {len(contornos)}")
    
    # Configuração da pasta de saída
    pasta_output = os.path.join(os.path.dirname(os.path.dirname(caminho_imagem)), "dataset", "output")
    os.makedirs(pasta_output, exist_ok=True)
    
    # Salva a máscara para o relatório
    cv2.imwrite(os.path.join(pasta_output, "1_mascara_binaria.png"), mascara_final)
    
    # 6. Laço de Recorte e Salvamento com Transparência (Canal Alfa)
    contador = 0
    for i, contorno in enumerate(contornos):
        if cv2.contourArea(contorno) < 50:
            continue
            
        x, y, largura, altura = cv2.boundingRect(contorno)
        
        # 1. Recorta o sprite colorido e a sua respectiva máscara binária
        sprite_recortado = img_original[y:y+altura, x:x+largura]
        mascara_recortada = mascara_final[y:y+altura, x:x+largura]
        
        # 2. Converte o sprite de BGR (3 canais) para BGRA (4 canais)
        sprite_bgra = cv2.cvtColor(sprite_recortado, cv2.COLOR_BGR2BGRA)
        
        # 3. Onde a máscara for 0 (fundo preto), definimos o canal Alfa como 0 (transparente)
        # Onde for 255 (personagem branco), o canal Alfa fica em 255 (opaco/visível)
        sprite_bgra[:, :, 3] = mascara_recortada
        
        # Salva o sprite individual (o formato .png suporta o canal alfa)
        nome_saida = f"sprite_{contador:03d}.png"
        cv2.imwrite(os.path.join(pasta_output, nome_saida), sprite_bgra)
        contador += 1
        
    print(f"[SUCESSO] Processo concluído! {contador} sprites foram salvos em dataset/output/")
    return img_original