import krpc
import time
import csv
import matplotlib.pyplot as plt
def main():
    # Подключение к серверу kRPC
    conn = krpc.connect(name='Space M')

    # Получение информации об активном "судне"
    vessel = conn.space_center.active_vessel
  
    #получение информации о небесном теле - Луне
    body = vessel.orbit.body 

    #Открытие csv файла
    w_file = open("KSP change orbit data.csv", mode="w", encoding="UTF-8")
    fieldnames = ['Time since maneuver start', 'Ingame Time', 'Velocity']
    writer = csv.DictWriter(w_file, fieldnames=fieldnames)
    writer.writeheader()   
    # Инициализация списков для хранения данных
    velocity_data = []
    time_data = [] 

    try:
        # Ждем, пока не зарабоатет двигатель Луны-25 
        while vessel.control.throttle == 0:
          print(conn.space_center.ut, vessel.control.throttle)
          time.sleep(0.5)
        # Маневр начался. Считываем данные, пока работает двигатель
        k = 0      
        while vessel.control.throttle > 0:  
          # Получение текущего  времени
          cur_time = round(conn.space_center.ut, 2)
          # Получение текущей скорости
          velocity = round(vessel.flight(body.orbital_reference_frame).speed, 5)
          # Запись данных
          velocity_data.append(velocity)
          time_data.append(round(cur_time, 2))
          print(k, cur_time,velocity, vessel.orbit.time_to_apoapsis, vessel.control.throttle)
          k += 1
          # Задержка перед следующим измерением
          time.sleep(1) 


    except KeyboardInterrupt:
        print('Программа завершена пользователем.')

    finally:
        # Закрытие соединения с сервером kRPC
        conn.close()
        #Запись полученных данных в csv файл, закрытие файла
        for n in range(len(time_data)):
            writer.writerow({'Time since maneuver start': n, 'Ingame Time': time_data[n], 'Velocity': velocity_data[n]})
        w_file.close()
        # Построение графика зависимости скорости от времени 
        plt.plot(time_data, velocity_data)
        plt.xlabel('Время (секунды)')
        plt.ylabel('Скорость (м/с)')
        plt.title('График зависимости скорости от времени')
        plt.show()
        

if __name__ == '__main__':
   main()
