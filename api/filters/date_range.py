from django_filters.filters import DateRangeField, DateTimeFromToRangeFilter


class DateRangeFieldNew(DateRangeField):
    """
    Поле как и DateFromToRangeFilter в django_filters только
    не переводить в datetime.datetime и стандартное решение работает
    с временем которое нам не нужно т.к аренда идет на сутки
    """

    def compress(self, data_list):
        if data_list:
            start_date, stop_date = data_list
            return [start_date, stop_date]
        return None


class CustomDateFromToRangeFilter(DateTimeFromToRangeFilter):
    """
    Кастомный фильтр для установления нормальнього суфикса и простоты фильтрации
    """

    field_class = DateRangeFieldNew
