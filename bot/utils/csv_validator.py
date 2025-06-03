import csv
import re
from typing import Dict, List


class CSVValidator:
    PRODUCT_SCHEMA = {
        'артикул': str,
        'название': str,
        'описание': str,
        'фото1': str,
        'фото2': str,
        'фото3': str,
        'цена': float,
        'категория': str
    }

    @classmethod
    def validate_product_csv(cls, file_path: str) -> Dict:
        result = {
            'is_valid': True,
            'errors': [],
            'headers': [],
            'sample_row': {}
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                result['headers'] = reader.fieldnames

                required_columns = {'артикул', 'название', 'цена', 'категория'}
                missing_columns = required_columns - set(reader.fieldnames)
                if missing_columns:
                    result['is_valid'] = False
                    result['errors'].append(f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}")
                    return result

                try:
                    first_row = next(reader)
                    result['sample_row'] = first_row

                    if not re.match(r'^[a-zA-Z0-9]+$', first_row['артикул']):
                        result['is_valid'] = False
                        result['errors'].append("Артикул должен содержать только буквы и цифры")

                    try:
                        price = float(first_row['цена'])
                        if price <= 0:
                            result['is_valid'] = False
                            result['errors'].append("Цена должна быть больше 0")
                    except ValueError:
                        result['is_valid'] = False
                        result['errors'].append("Неверный формат цены")

                    for i in range(1, 4):
                        photo_key = f'фото{i}'
                        if photo_key in first_row and first_row[photo_key]:
                            if not first_row[photo_key].startswith(('http://', 'https://')):
                                result['is_valid'] = False
                                result['errors'].append(f"Фото{i} должно быть URL")

                except StopIteration:
                    result['errors'].append("CSV файл не содержит данных")
                    result['is_valid'] = False

        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Ошибка чтения файла: {str(e)}")

        return result