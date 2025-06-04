
# Projeto - Detecção e Resposta a Queimadas com Visão Computacional

Este projeto simula um sistema de resposta a queimadas utilizando **YOLOv8**, **OpenCV** e **Python**. A solução identifica fogo em tempo real via webcam e aciona um bot do Telegram com alertas automáticos. 

---

## Estruturas de Programação Usadas

O projeto utiliza **conceitos do Conjunto 3** de Programação Dinâmica, como:

-  **Busca binária (bisect.insort)**: para manter a lista de ocorrências ordenada por severidade e tempo.
-  **Dicionários**: usados para gerar relatórios agregados por região.
-  **Análise de algoritmos**: as estruturas foram escolhidas visando eficiência, principalmente para ordenação e registro.

---

## Funcionalidades

- Detectar fogo em tempo real com YOLOv8
- Calcular a área do fogo para definir **severidade**
- Registrar ocorrências com base em região
- Atender a ocorrência mais severa
- Enviar alerta e foto via **Telegram Bot**
- Exibir foto com detecção ao vivo

---

## Comentários no Código

O código contém comentários onde os conceitos do Conjunto 3 são aplicados. Trechos como:

```python
relatorio_regioes = {}  # <-- USO DE DICIONÁRIO
bisect.insort(ocorrencias, ...)  # <-- USO DE BUSCA BINÁRIA
```

---

## Execução

1. Treine seu modelo YOLO e coloque o `.pt` em `runs/detect/train4/weights/best.pt`
2. Instale dependências:
```bash
pip install ultralytics opencv-python pyTelegramBotAPI
```
3. Execute o script.
4. Interaja com o bot via Telegram e observe a detecção ao vivo.
