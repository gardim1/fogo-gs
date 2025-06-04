from ultralytics import YOLO
import cv2
import telebot
import threading
import time

TOKEN = "7744307403:AAHydF9ilHCy3gQp_R4iwHpc2r-OwTI7s7A"
CHAT_ID = "5872025823"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(msg):
    bot.reply_to(msg, "Olá! Estou monitorando o vídeo em busca de fogo. Se detectar, enviarei uma imagem de alerta.")

def rodar_bot():
    bot.infinity_polling()

threading.Thread(target=rodar_bot, daemon=True).start()

model = YOLO("runs/detect/train4/weights/best.pt")
cap = cv2.VideoCapture(0)
classe_fogo = list(model.names.values())[0]
ultimo_alerta = 0

ocorrencias = []
historico = []
relatorio_regioes = {} # Dicionário usado para armazenar contagem de atendimentos por região

def registrar_ocorrencia(severidade, local):
    timestamp = time.time()
    nova_ocorrencia = (severidade, timestamp, local)

    # Implementação da busca binária para encontrar o índice de inserção
    low = 0
    high = len(ocorrencias)
    while low < high:
        mid = (low + high) // 2
        if ocorrencias[mid][0] < severidade:
            low = mid + 1
        elif ocorrencias[mid][0] > severidade:
            high = mid
        else:
            # empata em severidade, desempata por timestamp 
            if ocorrencias[mid][1] < timestamp:
                low = mid + 1
            else:
                high = mid
    ocorrencias.insert(low, nova_ocorrencia)  

def atender_ocorrencia():
    if ocorrencias:
        ocorrencia = ocorrencias.pop() # Análise de eficiência: como a lista está ordenada, último item é o mais urgente
        historico.append(ocorrencia)
        regiao = ocorrencia[2]
        relatorio_regioes[regiao] = relatorio_regioes.get(regiao, 0) + 1 # Uso de dicionário com contagem acumulada
        return ocorrencia
    return None

def calcular_area_total(boxes):
    total = 0
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        area = (x2 - x1) * (y2 - y1)
        total += area
    return total

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    results = model(frame)
    fogo_detectado = False
    boxes_detectadas = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            label = r.names[cls]

            if label == classe_fogo:
                fogo_detectado = True
                boxes_detectadas.append(box)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "FOGO DETECTADO", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.imwrite("alerta.jpg", frame)

    agora = time.time()
    if fogo_detectado and (agora - ultimo_alerta > 10):
        area_total = calcular_area_total(boxes_detectadas)
        severidade = min(10, area_total // 5000) or 1 
        regiao = "Zona " + ["Norte", "Sul", "Leste", "Oeste"][int(time.time()) % 4]
        registrar_ocorrencia(severidade, regiao)

        bot.send_message(CHAT_ID, "🔥 Tá pegando fogo, bixo!")
        with open("alerta.jpg", "rb") as foto:
            bot.send_photo(CHAT_ID, foto)

        ocorrencia = atender_ocorrencia()
        if ocorrencia:
            msg = f"Ocorrência atendida:\nRegião: {ocorrencia[2]}\nSeveridade: {ocorrencia[0]}"
            bot.send_message(CHAT_ID, msg)

        ultimo_alerta = agora

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
