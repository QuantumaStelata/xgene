def set_obj_in_kwargs(kwargs, obj_name, model_fixture):
    obj_name_pk = f'{obj_name}_id'

    if obj_name not in kwargs and obj_name_pk not in kwargs:
        kwargs[obj_name] = model_fixture()
