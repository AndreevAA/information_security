import intaller
import math

def dist_points():
	print ("Программа нахождения расстония между двумя точками...")
	p1 = list(map(float, input("Введите координаты первой точки через пробел: ").split()))
	p2 = list(map(float, input("Введите координаты второй точки через пробел: ").split()))
	distance = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
	print ("Итоговая дистация между двумя точками: " + str(distance))

if __name__ == "__main__":
	license = intaller.License("license.key")

	if license.check_CPUsum():
		print("Cool! You have a license!")
		dist_points()
	else:
		print("Sorry, access is denied!")

