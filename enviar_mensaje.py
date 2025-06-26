
from twilio.rest import Client

# 🔐 Tus credenciales desde Twilio Dashboard
account_sid = 'XXXXX'
auth_token = 'XXXXX'
client = Client(account_sid, auth_token)

# 📤 Envío del mensaje de prueba
message = client.messages.create(
    from_='whatsapp:+numerotwilio',  # Este es el número del sandbox de Twilio (NO cambiar)
    body='¡Hola mi proveedor guapetón! Este es un mensaje de prueba desde ArtisanBurger SAS. Confirmame si te llegó 😎🍔',
    to='whatsapp:+57numeroartisan'  # Reemplaza con tu número real en formato internacional
)

print("✅ Mensaje enviado. SID:", message.sid)