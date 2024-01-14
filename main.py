import random
import tkinter as tk
from tkinter import ttk
import sys

def run_genetic_algorithm():
    global num_iterations, mutation_rate, crossover_rate
    num_iterations = int(iteration_entry.get())
    mutation_rate = float(mutation_entry.get())
    crossover_rate = float(crossover_entry.get())

    result_label.config(text="Genetik algoritma başarıyla çalıştırıldı!")

# Tkinter penceresini oluştur
window = tk.Tk()
window.title("Genetik Algoritma Parametreleri")

# Etiketler
iteration_label = tk.Label(window, text="Iterasyon Sayısı:")
mutation_label = tk.Label(window, text="Mutasyon Oranı:")
crossover_label = tk.Label(window, text="Çaprazlama Oranı:")

# Giriş kutuları
iteration_entry = ttk.Entry(window)
mutation_entry = ttk.Entry(window)
crossover_entry = ttk.Entry(window)

# Çalıştır butonu
run_button = ttk.Button(window, text="Genetik Algoritma Çalıştır", command=run_genetic_algorithm)

# Sonuç etiketi
result_label = ttk.Label(window, text="")

# Pencere elemanlarını düzenle
iteration_label.grid(row=0, column=0, padx=10, pady=5, sticky="E")
iteration_entry.grid(row=0, column=1, padx=10, pady=5)

mutation_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
mutation_entry.grid(row=1, column=1, padx=10, pady=5)

crossover_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
crossover_entry.grid(row=2, column=1, padx=10, pady=5)

run_button.grid(row=3, columnspan=2, pady=10)

result_label.grid(row=4, columnspan=2, pady=5)

# Tkinter ana döngüsünü başlat
window.mainloop()

# Başlangıç değerleri
population_size=50


# Dosya yollarını tanımla
groups_path = "txt_dosyalari/groups.txt"
teacher_can_less_path = "txt_dosyalari/teacher_can_less.txt"
class_path = "txt_dosyalari/class.txt"

target_variables_groups = ["lesson_id", "time_id", "teacher_id"]
target_variables_teacher_can_less = ["lesson_id", "teacher_id"]
target_variables_class = ["class_id", "student_capacity"]

def dosyadan_deger_al(file_path, target_variables):
    with open(file_path, 'r') as dosya:
        değişken_isimleri = dosya.readline().split()
        satırlar = dosya.readlines()

    rs_satır = random.choice(satırlar)
    degisken_degerleri = rs_satır.split()

    selected_values = {}
    for target_variable in target_variables:
        if target_variable in değişken_isimleri:
            variable_index = değişken_isimleri.index(target_variable)
            selected_values[target_variable] = degisken_degerleri[variable_index]

    return selected_values

def dosyadan_deger_al_teacher_can_less(file_path, target_variables, lesson_id_groups):
    with open(file_path, 'r') as dosya:
        değişken_isimleri = dosya.readline().split()
        satırlar = dosya.readlines()

    uygun_satırlar = []
    for satır in satırlar:
        satır_split = satır.split()
        if "lesson_id" in değişken_isimleri and len(satır_split) > değişken_isimleri.index("lesson_id") and satır_split[
            değişken_isimleri.index("lesson_id")] == lesson_id_groups:
            uygun_satırlar.append(satır_split)

    if not uygun_satırlar:
        return {}

    selected_values = {}
    rs_satır = random.choice(uygun_satırlar)
    for target_variable in target_variables:
        if target_variable in değişken_isimleri:
            variable_index = değişken_isimleri.index(target_variable)
            selected_values[target_variable] = rs_satır[variable_index]

    return selected_values

def print_population(population):
    for idx, individual in enumerate(population):
        teacher_id_value = individual["teacher_can_less"].get("teacher_id")
        lesson_id = individual["groups"].get("lesson_id")
        time_id = individual["groups"].get("time_id")
        class_id = individual["class"].get("class_id")

        print(f"Group ID:{lesson_id} Time ID:{time_id} Teacher ID: {teacher_id_value}  Class ID:{class_id}")

def crossover(population, crossover_rate,previous_teacher_id_olmayan_count):
    new_population = []  # Yeni popülasyonu tutacak liste

    for _ in range(len(population)):

        parent1_index = random.randint(0, len(population) - 1)
        parent2_index = random.randint(0, len(population) - 1)


        if random.random() < crossover_rate:

            child1, child2 = single_point_crossover(population[parent1_index], population[parent2_index])


            new_population.append(child1)
            new_population.append(child2)
        else:
            # Çaprazlama yapılmadıysa, ebeveynleri yeni popülasyona ekle
            new_population.append(population[parent1_index])
            new_population.append(population[parent2_index])
    teacher_id_olmayan_kromozomlar = len([ind for ind, pop in enumerate(population) if
                                          not pop["teacher_can_less"].get("teacher_id")])


    print("Mevcut sayı:", teacher_id_olmayan_kromozomlar)

    # Karşılaştır ve önceki sayıyı güncelle
    if teacher_id_olmayan_kromozomlar < previous_teacher_id_olmayan_count:
        if teacher_id_olmayan_kromozomlar==0:
            def write_population_to_file(population, file_path):

                with open(file_path, 'w') as file:
                    for individual in population:
                        teacher_id_value = individual["teacher_can_less"].get("teacher_id")
                        lesson_id = individual["groups"].get("lesson_id")
                        time_id = individual["groups"].get("time_id")
                        class_id = individual["class"].get("class_id")

                        print(
                            f"Group ID:{lesson_id} Time ID:{time_id} Teacher ID: {teacher_id_value}  Class ID:{class_id}")
                        print("\n")
                        file.write(
                            f"Group ID:{lesson_id}" + '\n' + f" Time ID:{time_id}" + '\n' + f"Teacher ID: {teacher_id_value}" + '\n' + f" Class ID:{class_id}" + '\n' + f"Uygunluk Değeri:{previous_teacher_id_olmayan_count}"+ '\n')



            file_path = 'population.txt'
            write_population_to_file(population, file_path)
            sys.exit()


        previous_teacher_id_olmayan_count = teacher_id_olmayan_kromozomlar

        def write_population_to_file(population, file_path):

            with open(file_path, 'w') as file:
                for individual in population:
                    teacher_id_value = individual["teacher_can_less"].get("teacher_id")
                    lesson_id = individual["groups"].get("lesson_id")
                    time_id = individual["groups"].get("time_id")
                    class_id = individual["class"].get("class_id")

                    print(
                        f"Group ID:{lesson_id} Time ID:{time_id} Teacher ID: {teacher_id_value}  Class ID:{class_id}")
                    print("\n")
                    file.write(
                        f"Group ID:{lesson_id}" + '\n' + f" Time ID:{time_id}" + '\n' + f"Teacher ID: {teacher_id_value}" + '\n' + f" Class ID:{class_id}" + '\n' + f"Uygunluk Değeri:{previous_teacher_id_olmayan_count}"+ '\n')


        file_path = 'population.txt'
        write_population_to_file(population, file_path)


    population=new_population

    return population
def single_point_crossover(parent1, parent2):

    child1 = parent1.copy()
    child2 = parent2.copy()



    crossover_point = 3


    child1["groups"]["lesson_id"] = parent2["groups"]["lesson_id"][:crossover_point] + parent1["groups"]["lesson_id"][crossover_point:]
    child2["groups"]["lesson_id"] = parent1["groups"]["lesson_id"][:crossover_point] + parent2["groups"]["lesson_id"][crossover_point:]




    return child1, child2

previous_teacher_id_olmayan_count = 50  # Initialize with a large value

def mutation(population, mutation_rate):
    global previous_teacher_id_olmayan_count  # Global değişken olarak tanımla

    for individual in population:
        # Mutasyon oranına göre mutasyon gerçekleşip gerçekleşmeyeceğini kontrol et
        if random.random() < mutation_rate:



            new_teacher_values = dosyadan_deger_al_teacher_can_less(teacher_can_less_path,
                                                                    target_variables_teacher_can_less,
                                                                    individual["groups"]["lesson_id"])


            if new_teacher_values and "teacher_id" in new_teacher_values:
                # Yeni öğretmen ID'sini new_teacher_values'tan al
                new_teacher_id = new_teacher_values["teacher_id"]

                # Bireyin kromozomunu yeni öğretmen ID'si ile güncelle
                individual["teacher_can_less"]["teacher_id"] = new_teacher_id


            else:


                new_teacher_id = dosyadan_deger_al_teacher_can_less(teacher_can_less_path,
                                                                        target_variables_teacher_can_less,
                                                                        individual["groups"]["lesson_id"]).get("teacher_id", None)

                if new_teacher_id is not None:
                    individual["teacher_can_less"]["teacher_id"] = new_teacher_id

                else:
                    new_teacher_id = dosyadan_deger_al_teacher_can_less(teacher_can_less_path,
                                                                          target_variables_teacher_can_less,
                                                                          lesson_id_groups)["teacher_id"]

                    individual["teacher_can_less"]["teacher_id"] = new_teacher_id


            # Öğretmen ID'si olmayan kromozom sayısını hesapla
            teacher_id_olmayan_kromozomlar = len([ind for ind, pop in enumerate(population) if
                                                  not pop["teacher_can_less"].get("teacher_id")])


            print("Fitness:", teacher_id_olmayan_kromozomlar)

            # Karşılaştır ve önceki sayıyı güncelle
            if teacher_id_olmayan_kromozomlar < previous_teacher_id_olmayan_count:
                if teacher_id_olmayan_kromozomlar==0:
                    def write_population_to_file(population, file_path):

                        with open(file_path, 'w') as file:
                            for individual in population:
                                teacher_id_value = individual["teacher_can_less"].get("teacher_id")
                                lesson_id = individual["groups"].get("lesson_id")
                                time_id = individual["groups"].get("time_id")
                                class_id = individual["class"].get("class_id")

                                print( f"Group ID:{lesson_id} Time ID:{time_id} Teacher ID: {teacher_id_value}  Class ID:{class_id}")
                                print("\n")
                                file.write(f"Group ID:{lesson_id}" + '\n' + f" Time ID:{time_id}" + '\n' + f"Teacher ID: {teacher_id_value}" + '\n' + f" Class ID:{class_id}" + '\n' + f"Uygunluk Değeri:{previous_teacher_id_olmayan_count}"+ '\n')



                    file_path = 'population.txt'
                    write_population_to_file(population, file_path)
                    sys.exit()

                previous_teacher_id_olmayan_count = teacher_id_olmayan_kromozomlar

                def write_population_to_file(population, file_path):

                    with open(file_path, 'w') as file:
                        for individual in population:
                            teacher_id_value = individual["teacher_can_less"].get("teacher_id")
                            lesson_id = individual["groups"].get("lesson_id")
                            time_id = individual["groups"].get("time_id")
                            class_id = individual["class"].get("class_id")

                            print(f"Group ID:{lesson_id} Time ID:{time_id} Teacher ID: {teacher_id_value}  Class ID:{class_id}")
                            print("\n")
                            file.write(f"Group ID:{lesson_id}"+ '\n'+f" Time ID:{time_id}"+ '\n'+f"Teacher ID: {teacher_id_value}"+ '\n'+f" Class ID:{class_id}"+ '\n'+f"Uygunluk Değeri:{previous_teacher_id_olmayan_count}"+ '\n')


                file_path = 'population.txt'
                write_population_to_file(population, file_path)


    return previous_teacher_id_olmayan_count


population = []
for _ in range(population_size):
    selected_values_groups = dosyadan_deger_al(groups_path, target_variables_groups)
    lesson_id_groups = selected_values_groups["lesson_id"]

    selected_values_teacher_can_less = dosyadan_deger_al_teacher_can_less(teacher_can_less_path,
                                                                          target_variables_teacher_can_less,
                                                                          lesson_id_groups)

    selected_values_class = dosyadan_deger_al(class_path, target_variables_class)

    # Kromozom oluşturma
    chromosome = {
        "groups": selected_values_groups,
        "teacher_can_less": selected_values_teacher_can_less,
        "class": selected_values_class
    }

    population.append(chromosome)


for iteration in range(num_iterations):
    if (iteration % 2 == 1):

      population=crossover(population, crossover_rate,previous_teacher_id_olmayan_count)
      print_population(population)

    else:

        mutationed = mutation(population, mutation_rate)
        print_population(population)





