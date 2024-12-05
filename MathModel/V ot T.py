import matplotlib.pyplot as plt

def V(t,m,V2,F):
    return (m * V2 - F * t) / m
time = []
V1 = []
F = 375
m = 1750
V2 = 1633
t_engine = 84
for t in range(t_engine + 1):
    time.append(t)
    V1.append(V(t,m,V2,F))

plt.plot(time, V1)
plt.xlabel('Время (секунды)')
plt.ylabel('Скорость (м/с)')
plt.title('График зависимости скорости от времени')
plt.show()
