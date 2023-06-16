import json

# Función para cargar los datos del archivo JSON
def load_data():
    try:
        with open('movies.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []

# Función para guardar los datos en el archivo JSON
def save_data(data):
    with open('movies.json', 'w') as file:
        json.dump(data, file)

# Función para agregar una película y su calificación
def add_movie():
    title = input("Ingrese el título de la película: ")
    rating = float(input("Ingrese la calificación de la película (0-5): "))

    movie = {
        'title': title,
        'rating': rating
    }

    data = load_data()
    data.append(movie)
    save_data(data)

    print("Película agregada con éxito.")

# Función para mostrar el ranking de películas
def show_ranking():
    data = load_data()

    if not data:
        print("No hay películas en el ranking.")
        return

    print("Ranking de películas:")
    for i, movie in enumerate(data):
        print(f"{i+1}. {movie['title']}: {movie['rating']}")

# Función principal del programa
def main():
    while True:
        print("\nSistema de Ranking de Películas")
        print("1. Agregar película y calificación")
        print("2. Mostrar ranking de películas")
        print("3. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            add_movie()
        elif choice == "2":
            show_ranking()
        elif choice == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
