import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
EMAIL_TO = os.environ.get("EMAIL_TO")


class NotificationManager:
    def __init__(self):
        self.weather_alert_msgs = []
        self.msg_subject = "Today's Weather"
        self.alert_email_msg = ""
        self.message = ""
        self.forecast = ""

    def create_alert_message(self, alert_event):
        if "wind" and "rain" in alert_event:
            self.weather_alert_msgs.append("Batten down the hatches, a storm is coming")
        elif "wind" in alert_event:
            self.weather_alert_msgs.append("Buckle up, it's going to get windy")
        elif "rain" in alert_event:
            self.weather_alert_msgs.append("Best to build an ark, rain is coming")
        if "snow" in alert_event:
            self.weather_alert_msgs.append("Time to curl up in front of the fire, looks like snow")
        if "ice" in alert_event:
            self.weather_alert_msgs.append("Be careful out there, it's going to be slippy")
        if "thunderstorm" in alert_event:
            self.weather_alert_msgs.append("Time to curl up with a good book, there's a storm brewing")
        if "lightning" in alert_event:
            self.weather_alert_msgs.append("Can you feel the electricity in the air?")
        if "heat" in alert_event:
            self.weather_alert_msgs.append("I'm melting...")
        if "fog" in alert_event:
            self.weather_alert_msgs.append("Good luck seeing your hand in front of your face today")

        if len(self.weather_alert_msgs) == 1:
            self.alert_email_msg = f"{self.weather_alert_msgs[0]}!"
        elif len(self.weather_alert_msgs) == 2:
            self.alert_email_msg = f"{self.weather_alert_msgs[0]}. By the way, {self.weather_alert_msgs[1].lower()}!"
        elif len(self.weather_alert_msgs) > 2:
            self.alert_email_msg = "TOO MUCH WEATHER!!!!!"

        return self.alert_email_msg

    def create_weather_forecast(self, weather_forecast):
        weather_description = weather_forecast["weather"]
        day_temp = weather_forecast["day_temp"]
        day_temp_feels_like = weather_forecast["day_temp_feels_like"]
        uv = weather_forecast["uv"]
        wind_speed = weather_forecast["wind_speed"]
        wind_gusts = weather_forecast["wind_gusts"]
        night_temp = weather_forecast["night_temp"]

        self.forecast = f"Today, the weather will be mostly {weather_description}, with an average day-time temperature" \
                        f" of {day_temp}°c, although this will feel much more like {day_temp_feels_like}°c.\n\n" \
                        f"The UV index is {uv}.\n\n" \
                        f"You can expect wind speeds averaging around {wind_speed}mph, with gusts of {wind_gusts}mph." \
                        f" Tonight will have an average temperature of {night_temp}°c."
        return self.forecast

    def create_1_weather_warning_msg(self, alert_event, alert_description):
        self.create_alert_message(alert_event=alert_event)
        self.msg_subject = "Time for a Weather Warning!"
        self.message = f"{self.alert_email_msg}\n\nA weather alert has been issued by the Met Office: " \
                       f"{alert_event}\n\n{alert_description}\n\n\n\n"
        return self.msg_subject, self.message

    def create_2_weather_warning_msg(self, alert_event_1, alert_event_2, alert_description_1, alert_description_2):
        self.create_alert_message(alert_event=alert_event_1)
        self.msg_subject = "It's about to get grim out there - Weather Warning Alert!"
        self.message = f"Hold up, there have been two weather alerts issued by the Met Office:\n\n" \
                       f"{alert_event_1} today and {alert_event_2} tomorrow!" \
                       f"\n\nSo...{self.alert_email_msg}\n\n" \
                       f"Today: {alert_event_1}\n" \
                       f"{alert_description_1}\n\n" \
                       f"Tomorrow: {alert_event_2}\n" \
                       f"{alert_description_2}\n\n" \
                       f"Stay safe out there!\n\n\n\n"
        return self.msg_subject, self.message

    def create_thunder_email_msg(self):
        self.msg_subject = "Potential Thunder Alert"
        self.message = "Hold on to your hats, there is potential for a thunderstorm today!\n\n"
        return self.msg_subject, self.message

    def create_snow_email_msg(self):
        self.msg_subject = "Potential Snow Alert"
        self.message = "Stoke up the fire and pour yourself a hot chocolate, there may be snow today!\n\n"
        return self.msg_subject, self.message

    def send_email(self):
        body = f"{self.message}Today's Forecast:\n\n{self.forecast}"
        message = EmailMessage()
        message.add_header("From", MY_EMAIL)
        message.add_header("To", EMAIL_TO)
        message.add_header("Subject", self.msg_subject)
        message.set_payload(body, "utf-8")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.send_message(message)
