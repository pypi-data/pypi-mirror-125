from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, TypeAlias, Union


class Form:
    """ Базовая форма для PyQt6-input-виджетов """
    def __init__(self, form_name: str,
                 default_value='',
                 converter: Callable = str,
                 error_handler: Callable = print,
                 form_manager: FormManager = None) -> None:

        self._form_name = form_name
        self._default_value = default_value
        self._converter = converter
        self._error_handler = error_handler
        self._form_manager = form_manager

        self.append_form_manager(form_manager)

    def get_value(self):
        """ Возвращает текущее значение поля """
        raise NotImplementedError('Невозможно получить значение, '
                                  'т.к. метод не переопределён')

    def set_value(self, value: FormValueType):
        """ Устанавливает текущее значение поля """
        raise NotImplementedError('Невозможно задать значение, '
                                  'т.к. метод не переопределён')

    def restore_value(self):
        """ Устанавливает значение по умолчанию """
        raise NotImplementedError('Невозможно установить '
                                  'значение по-умолчанию, '
                                  'т.к. метод не переопределён')

    def clear_value(self):
        """ Удаляет значение из формы """
        raise NotImplementedError('Невозможно задать значение, '
                                  'т.к. метод не переопределён')

    def form_name(self):
        return self._form_name

    def form_manager(self):
        return self._form_manager

    def default_value(self):
        return self._default_value

    def append_form_manager(self, form_manager: FormManager):
        """ Добавляет форму в FormManager """
        if isinstance(form_manager, FormManager):
            form_manager.append_form(self)

    def remove_form_manager(self):
        """ Удаляет форму из FormManager """
        self._form_manager.remove_form(self)


class FormManager:
    def __init__(self) -> None:
        self.__forms_dict: dict[str, Form] = {}
        self.__forms_list: list[str] = []

    def __getitem__(self, form_name: str) -> Form:
        return self.__forms_dict[form_name]

    def __getattribute__(self, name: str) -> Any | Form:
        return super().__getattribute__(name)

    def append_form(self, form: Form):
        """ Добавляет форму в FormManager """
        if isinstance(form, Form):
            self.__forms_dict[form.form_name()] = form
            self.__dict__[form.form_name()] = form
            self.__forms_list.append(form.form_name())
            form._form_manager = self
        else:
            raise TypeError(f'Must be {Form}, not {type(form)} | '
                            f'{form.form_name()}: {form}')

    def append_forms(self, forms: list[Form]):
        """ Добавляет """
        for form in forms:
            self.append_form(form)

    def remove_form(self, form_or_name: str | Form) -> Form | None:
        """ Удаляет форму из FormManager """

        # Если была передана форма, то получаем сами ее имя
        if isinstance(form_or_name, Form):
            form_name = form_or_name.form_name()
        else:
            form_name = form_or_name

        removed_form: Form = self.__forms_dict.pop(form_name, None)
        if removed_form:
            self.__dict__.pop(form_name)
            self.__forms_list.remove(removed_form.form_name())
            removed_form.remove_form_manager()
        return removed_form

    def forms_to_dict(self) -> dict[str, Form]:
        """ Возвращаем словарь `{form_name: Form}`"""
        return self.__forms_dict.copy()

    def update_form_value(self, form_or_name: FormOrNameType,
                          value: FormValueType):
        """ Обновляет значение указанной формы """
        try:
            if isinstance(form_or_name, Form):
                form_name = form_or_name.form_name()
            else:
                form_name = form_or_name
            self.__forms_dict[form_name].set_value(value)
        except KeyError as e:
            # !!!
            # Добавить свой Exception
            # !!!
            raise e

    def update_form_values(self, form_value_dict: dict[str, FormValueType]):
        """ Обновляет значение указанных в словаре форм """
        for form_name, value in form_value_dict.items():
            self.update_form_value(form_name, value)


FormValueType: TypeAlias = str | int | float | bool | object
FormOrNameType: TypeAlias = str | Form
FormsOrNamesType: TypeAlias = list[str | Form] | list[str] | list[Form]
