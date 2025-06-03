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

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    results = model(frame)
    fogo_detectado = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            label = r.names[cls]

            if label == classe_fogo:
                fogo_detectado = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "FOGO DETECTADO", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.imwrite("alerta.jpg", frame)

    agora = time.time()
    if fogo_detectado and (agora - ultimo_alerta > 10):
        bot.send_message(CHAT_ID, "🔥 Tá pegando fogo, bixo!")
        ultimo_alerta = agora 
        with open("alerta.jpg", "rb") as foto:
            bot.send_photo(CHAT_ID, foto)

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
