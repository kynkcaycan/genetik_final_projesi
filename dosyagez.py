import random

def dosyadan_deger_al(file_path, target_variables):
    with open(file_path, 'r') as dosya:
        değişken_isimleri = dosya.readline().split()
        satırlar = dosya.readlines()

    rs_satır = random.choice(satırlar)
    degisken_degerleri = rs_satır.split()

    selected_values = {}
    for target_variable in target_variables:
        variable_index = değişken_isimleri.index(target_variable)
        selected_values[target_variable] = degisken_degerleri[variable_index]

    return selected_values

def dosyadan_deger_al_teacher_can_less(file_path, target_variables, lesson_id_groups):
    with open(file_path, 'r') as dosya:
        değişken_isimleri = dosya.readline().split()
        satırlar = dosya.readlines()

    # Belirli lesson_id ile eşleşen değerleri filtrele
    uygun_satırlar = []
    for satır in satırlar:
        satır_split = satır.split()
        if "lesson_id" in değişken_isimleri and len(satır_split) > değişken_isimleri.index("lesson_id") and satır_split[değişken_isimleri.index("lesson_id")] == lesson_id_groups:
            uygun_satırlar.append(satır_split)

    if not uygun_satırlar:
        # Eşleşen değer bulunamazsa boş bir sözlük döndür
        return {}

    # Ardından rasgele bir değeri seç
    selected_values = {}
    rs_satır = random.choice(uygun_satırlar)
    for target_variable in target_variables:
        variable_index = değişken_isimleri.index(target_variable)
        selected_values[target_variable] = rs_satır[variable_index]

    return selected_values

# Kullanım örneği
groups_path = "txt_dosyalari/groups.txt"
teacher_can_less_path = "txt_dosyalari/teacher_can_less.txt"
class_path = "txt_dosyalari/class.txt"

target_variables_groups = ["lesson_id", "time_id"]
target_variables_teacher_can_less = ["lesson_id", "teacher_id"]
target_variables_class = ["class_id", "student_capacity"]

# İki tablodan rastgele değerleri al
selected_values_groups = dosyadan_deger_al(groups_path, target_variables_groups)
selected_values_class = dosyadan_deger_al(class_path, target_variables_class)
lesson_id_groups = selected_values_groups["lesson_id"]

selected_values_teacher_can_less = dosyadan_deger_al_teacher_can_less(teacher_can_less_path, target_variables_teacher_can_less, lesson_id_groups)

# Kromozom oluşturma
chromosome = {
    "groups": selected_values_groups,
    "teacher_can_less": selected_values_teacher_can_less,
    "class": selected_values_class
}

# Kromozomu yazdır
print("Oluşturulan Kromozom:", chromosome)
