import krpc
import time
import matplotlib.pyplot as plt
def main():
    # Подключение к серверу kRPC
    conn = krpc.connect(name='Space M')

    # Получение информации об активном "судне"
    vessel = conn.space_center.active_vessel
  
    #получение информации о небесном теле - Луне
    body = vessel.orbit.body 

    # Инициализация списков для хранения данных
    velocity_data = []
    time_data = [] 

    try:
        # Ждем, пока Луна-25 не приблизится к апоцентру
        while vessel.orbit.time_to_apoapsis > 1.5:
          print(vessel.orbit.time_to_apoapsis)
          time.sleep(0.5)
        # Маневр начался. Т.к измерения каждые 0.5 сек (двигатель работает около 84 сек), считываем данные, пока k < 169 
        k = 0      
        while k < (84 * 2 + 1):  
          # Получение текущего  времени
          cur_time = conn.space_center.ut
          # Получение текущей скорости
          velocity = vessel.flight(body.orbital_reference_frame).speed
          # Запись данных
          velocity_data.append(velocity)
          time_data.append(cur_time)
          print(k, cur_time,velocity, vessel.orbit.time_to_apoapsis)
          k += 1
          # Задержка перед следующим измерением
          time.sleep(0.5) 


    except KeyboardInterrupt:
        print('Программа завершена пользователем.')

    finally:
        # Закрытие соединения с сервером kRPC
        conn.close()
        # Построение графика зависимости скорости от времени 
        plt.plot(time_data, velocity_data)
        plt.xlabel('Время (секунды)')
        plt.ylabel('Скорость (м/с)')
        plt.title('График зависимости скорости от времени')
        plt.show()
        

if __name__ == '__main__':
   main()
