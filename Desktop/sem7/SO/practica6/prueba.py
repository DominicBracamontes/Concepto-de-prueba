import time
import json
from datetime import datetime, timedelta
from pathlib import Path


# Simulacion de autenticacion (OAuth con Google)
class AuthModule:
    def authenticate_user(self, username, password):
        print(f"\nAutenticando al usuario '{username}'...")
        time.sleep(1)
        
        # Simulamos un fallo de autenticacion si la contrasena es incorrecta
        if password != "correct_password":
            print(f"Error de autenticacion: Contrasena incorrecta para '{username}'")
            return None
        print(f"Autenticacion exitosa para '{username}'.")
        return {"username": username, "token": "mock_token"}


# Simulacion de base de datos para alarmas
class AlarmDatabase:
    def __init__(self, db_file="alarms.json"):
        self.db_file = Path(db_file)
        if not self.db_file.exists():
            self._initialize_db()
        self.alarms = self._load_alarms()

    def _initialize_db(self):
        with open(self.db_file, 'w') as f:
            json.dump([], f)

    def _load_alarms(self):
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def _save_alarms(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.alarms, f, default=str)

    def add_alarm(self, username, alarm):
        self.alarms.append({"username": username, **alarm})
        self._save_alarms()
        print(f"Alarma configurada para el usuario '{username}': {alarm}")

    def get_active_alarms(self):
        now = datetime.now()
        active_alarms = [alarm for alarm in self.alarms if datetime.fromisoformat(alarm["time"]) <= now and not alarm["notified"]]
        return active_alarms

    def mark_alarm_notified(self, alarm):
        alarm["notified"] = True
        self._save_alarms()

    def delete_alarm(self, username, alarm_index):
        user_alarms = [alarm for alarm in self.alarms if alarm["username"] == username]
        if 0 <= alarm_index < len(user_alarms):
            alarm_to_remove = user_alarms[alarm_index]
            self.alarms.remove(alarm_to_remove)
            self._save_alarms()
            print(f"Alarma eliminada: {alarm_to_remove}")
        else:
            print("Indice de alarma invalido.")


# Simulacion de notificaciones
class NotificationModule:
    def send_notification(self, username, message, channel):
        print(f"Enviando notificacion a {username} via {channel}: '{message}'")


# Modulo principal para gestionar alarmas
class AlarmSystem:
    def __init__(self):
        self.auth = AuthModule()
        self.db = AlarmDatabase()
        self.notifications = NotificationModule()

    def authenticate(self, username, password):
        user = self.auth.authenticate_user(username, password)
        if user is None:
            return None
        return user

    def configure_alarm(self, user, time_offset, channel="email"):
        alarm_time = datetime.now() + timedelta(seconds=time_offset)
        alarm = {"time": alarm_time.isoformat(), "channel": channel, "message": "¡Tu alarma ha sonado!", "notified": False}
        self.db.add_alarm(user["username"], alarm)

    def check_alarms(self):
        active_alarms = self.db.get_active_alarms()
        if not active_alarms:
            print("No hay alarmas activas para notificar.")
        for alarm in active_alarms:
            self.notifications.send_notification(
                alarm["username"], alarm["message"], alarm["channel"]
            )
            self.db.mark_alarm_notified(alarm)

    def show_user_alarms(self, username):
        user_alarms = [alarm for alarm in self.db.alarms if alarm["username"] == username]
        if not user_alarms:
            print("No hay alarmas configuradas.")
            return
        print("\n--- Alarmas configuradas ---")
        for i, alarm in enumerate(user_alarms):
            status = "Notificada" if alarm["notified"] else "Pendiente"
            print(f"[{i}] - Tiempo: {alarm['time']}, Canal: {alarm['channel']}, Estado: {status}")

    def delete_alarm(self, user, alarm_index):
        self.db.delete_alarm(user["username"], alarm_index)


# Simulacion interactiva del sistema
if __name__ == "__main__":
    system = AlarmSystem()

    # Flujo simulado con autenticacion y configuracion de alarmas
    print("\n--- Sistema de Gestion de Alarmas ---")

    # Simulamos autenticacion exitosa
    username = "nicole.dominic"
    password = "correct_password"
    user = system.authenticate(username, password)

    if user is None:
        print("Autenticacion fallida. Terminando sesion.")
        exit(1)

    # Simulamos configuracion de alarmas
    print("\n--- Configurando nuevas alarmas ---")
    system.configure_alarm(user, time_offset=5, channel="email")  # Alarma en 5 segundos
    system.configure_alarm(user, time_offset=10, channel="sms")   # Alarma en 10 segundos
    system.configure_alarm(user, time_offset=15, channel="push")  # Alarma en 15 segundos

    # Simulamos la visualizacion de las alarmas configuradas
    system.show_user_alarms(user["username"])

    # Simulamos la eliminacion de una alarma
    print("\n--- Eliminando una alarma ---")
    system.delete_alarm(user, alarm_index=1)  # Eliminamos la alarma de 10 segundos

    # Simulamos el monitoreo de las alarmas por 20 segundos
    print("\n--- Monitoreo de alarmas activas ---")
    for _ in range(20):  # Monitorear durante 20 segundos
        system.check_alarms()
        time.sleep(1)

    # Finalizando flujo
    print("\n--- Fin de la simulacion ---")
