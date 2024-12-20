'''
Метод должен рассчитывать целое количество сырья, необходимого для производства определенного
количества (count) продукции, учитывая возможный брак материалов. Для упрощения расчетов будем
считать всю продукцию прямоугольного размера с известными значениями ширины (width) и длины
(length).
Количество необходимого качественного сырья на одну единицу продукции рассчитывается как площадь
продукции, умноженная на коэффициент типа продукции.
Коэффициенты типа продукции (product_type):
Тип продукции 1 - 1.1,
Тип продукции 2 - 2.5,
Тип продукции 3 - 8.43.
При этом нужно учитывать процент брака материала в зависимости от его типа (material_type):
Тип материала 1 - 0.3%,
Тип материала 2 - 0.12%.
При этом если в качестве параметров метода будут приходить несуществующие типы
продукции/материалов или другие неподходящие данные, то метод должен вернуть -1.
'''
import math

class MaterialCalculator:
    PRODUCT_TYPES = {
        1: 1.1,
        2: 2.5,
        3: 8.43,
    }
    MATERIAL_TYPES = {
        1: 0.003,  # 0.3%
        2: 0.0012,  # 0.12%
    }

    def calculate_material(count, width, length, product_type, material_type):
        # Проверка параметров на валидность
        if (
                not isinstance(count, int) or count <= 0 or
                not isinstance(width, (int, float)) or width <= 0 or
                not isinstance(length, (int, float)) or length <= 0 or
                product_type not in MaterialCalculator.PRODUCT_TYPES or
                material_type not in MaterialCalculator.MATERIAL_TYPES
        ):
            return -1

        # Расчет площади и коэффициента
        area = width * length
        product_coeff = MaterialCalculator.PRODUCT_TYPES[product_type]
        defect_coeff = MaterialCalculator.MATERIAL_TYPES[material_type]

        # Количество сырья
        required_material = count * area * product_coeff

        # Учет брака
        total_material = required_material * (1 + defect_coeff)

        # По условию ужно округлить полученное число
        return math.ceil(total_material)
