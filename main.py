import random
import numpy as np

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

def kontrol_ve_duzelt(chromosome, population):
    teacher_id_groups = chromosome["groups"].get("teacher_id")
    time_id_groups = chromosome["groups"].get("time_id")
    class_id_groups = chromosome["groups"].get("class_id")

    for ind, pop in enumerate(population):
        if teacher_id_groups and pop["groups"].get("teacher_id") == teacher_id_groups:
            new_teacher_id = dosyadan_deger_al_teacher_can_less(teacher_can_less_path,
                                                                target_variables_teacher_can_less,
                                                                pop["groups"]["lesson_id"])["teacher_id"]
            print("aynı ogretmen atanmıs")

            if new_teacher_id != teacher_id_groups:
                pop["groups"]["teacher_id"] = new_teacher_id
                print("Yeni öğretmen atandı:", new_teacher_id)
            else:
                print("Aynı öğretmene yeni bir atama yapılması gerekiyor ama aynı öğretmen ID'si seçildi. Başka bir öğretmen ID'si alınmalı.")

        if time_id_groups and class_id_groups and pop["groups"].get("time_id") == time_id_groups and pop["groups"].get(
                "class_id") == class_id_groups:
            new_class_id = dosyadan_deger_al(groups_path, target_variables_groups)["class_id"]

            if new_class_id != class_id_groups:
                pop["groups"]["class_id"] = new_class_id
                print("Yeni sınıf atandı:", new_class_id)
            else:
                print("Aynı sınıfa yeni bir atama yapılması gerekiyor ama aynı sınıf ID'si seçildi. Başka bir sınıf ID'si alınmalı.")

def print_population(population):
    for idx, individual in enumerate(population):
        teacher_id_value = individual["teacher_can_less"].get("teacher_id")
        lesson_id = individual["groups"].get("lesson_id")
        time_id = individual["groups"].get("time_id")
        class_id = individual["class"].get("class_id")
        print(f"Group ID:{lesson_id} Time ID:{time_id} Teacher ID: {teacher_id_value}  Class ID:{class_id}")

def crossover(parent1, parent2):
    # Çaprazlama işlemi
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(solution, pm):
    print(solution)  # Eklediğimiz satır
    if not isinstance(solution, list):
        raise ValueError("Solution must be a list.")

    y = np.array(solution, dtype='float64')  # Tüm öğeleri float64 türüne dönüştür
    flag = np.random.rand(y.shape[0]) <= pm
    indices = np.argwhere(flag == True).ravel()

    y[indices] += np.random.randn(len(indices))
    return y.tolist()

def mutation_population(population, mutation_rate=0.1):
    mutated_population = []
    for individual in population:
        # Her birey için mutasyon olasılığı kontrolü
        if np.random.rand() <= mutation_rate:
            mutated_individual = mutation(individual, mutation_rate)
            mutated_population.append(mutated_individual)
        else:
            mutated_population.append(individual)
    return mutated_population

def genetic_algorithm(initial_population, num_iterations, mutation_rate, crossover_rate):
    current_population = initial_population.copy()

    for iteration in range(num_iterations):
        print(f"Iteration {iteration + 1}")

        # Çaprazlama
        for i in range(0, len(current_population), 2):
            parent1 = current_population[i]
            parent2 = current_population[i + 1]
            child1, child2 = crossover(parent1, parent2)
            current_population[i] = child1
            current_population[i + 1] = child2

        # Mutasyon
        current_population = mutation_population(current_population, mutation_rate)

        # Popülasyonu yazdır
        print_population(current_population)

    return current_population

# Popülasyon büyüklüğü
population_size = 50

# Mutasyon oranı
mutation_rate = 0.5

# Çaprazlama oranı
crossover_rate = 0.5

# Iterasyon sayısı
num_iterations = 10

# Dosya yollarını tanımla
groups_path = "txt_dosyalari/groups.txt"
teacher_can_less_path = "txt_dosyalari/teacher_can_less.txt"
class_path = "txt_dosyalari/class.txt"

target_variables_groups = ["lesson_id", "time_id", "teacher_id"]
target_variables_teacher_can_less = ["lesson_id", "teacher_id"]
target_variables_class = ["class_id", "student_capacity"]

# Başlangıç popülasyonunu oluştur
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

# İlk popülasyonu yazdır
print("Initial Population:")
print_population(population)

teacher_id_olmayan_kromozomlar = [ind for ind, pop in enumerate(population) if not pop["teacher_can_less"].get("teacher_id")]
print(f"Teacher ID'si olmayan kromozom sayısı: {len(teacher_id_olmayan_kromozomlar)}")

# Genetik algoritma iterasyonları
for iteration in range(num_iterations):
    print(f"\nIteration {iteration + 1}:")

    # Çaprazlama işlemi
    for _ in range(population_size // 2):
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        # Çaprazlama işlemi burada gerçekleştirilebilir
        # Örneğin, tek noktalı çaprazlama fonksiyonunu çağırabilirsiniz
        # crossover(parent1, parent2)

    # Mutasyon işlemi
    mutated_population = mutation_population(population, mutation_rate)

    # Popülasyonu güncelle
    population = mutated_population

    # Kontrol ve düzeltmeleri yap
    for ind, pop in enumerate(population):
        kontrol_ve_duzelt(pop, population)

    # Popülasyonu yazdır
    print_population(population)

# Son popülasyonu yazdır
print("\nFinal Population:")
print_population(population)

teacher_id_olmayan_kromozomlar = [ind for ind, pop in enumerate(population) if not pop["teacher_can_less"].get("teacher_id")]
print(f"Teacher ID'si olmayan kromozom sayısı: {len(teacher_id_olmayan_kromozomlar)}")
