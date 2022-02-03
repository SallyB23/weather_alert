from weather_search import WeatherSearch
from notification_manager import NotificatationManager

ws = WeatherSearch()
nm = NotificatationManager()

ws.get_weather_data()
nm.create_weather_forecast(ws.forecast_data)
ws.check_alerts()

if len(ws.alert_event_list) == 1:
    nm.create_1_weather_warning_msg(alert_event=ws.alert_event_list[0],
                                    alert_description=ws.alert_description_list[0])

elif len(ws.alert_event_list) == 2:
    if ws.alert_event_list[0] == ws.alert_event_list[1]:
        nm.create_1_weather_warning_msg(alert_event=ws.alert_event_list[0],
                                        alert_description=ws.alert_description_list[0])

    else:
        nm.create_2_weather_warning_msg(alert_event_1=ws.alert_event_list[0],
                                        alert_event_2=ws.alert_event_list[1],
                                        alert_description_1=ws.alert_description_list[0],
                                        alert_description_2=ws.alert_description_list[1])

else:
    if ws.check_thunder() > 0:
        nm.create_thunder_email_msg()
    if ws.check_snow() > 0:
        nm.create_snow_email_msg()
    else:
        nm.create_weather_forecast(ws.forecast_data)

nm.send_email()

