def user_group_is_exist(user:object, group_name:str)->bool:
    return user.groups.filter(name=group_name).exists()