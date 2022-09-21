import intaller


if __name__ == "__main__":
	license = intaller.License("license.key")

	if license.check_CPUsum():
		print("Cool! You have a license!")
	else:
		print("Sorry, access is denied!")

