from main.submodels.account import Account


def fitness_cookie_update(account: Account, diff_value: int) -> None:
    """
    TODO test
    :param account:
    :param diff_value:
    :return:
    """
    new_value = max(account.number_fitness_cookie + diff_value, 0)
    account.number_fitness_cookie = new_value
    account.save()


def tennis_ball_update(account: Account, diff_value: int) -> None:
    """
    TODO test
    :param account:
    :param diff_value:
    :return:
    """
    new_value = max(account.number_tennis_ball + diff_value, 0)
    account.number_tennis_ball = new_value
    account.save()


def magic_bone_update(account: Account, diff_value: int) -> None:
    """
    TODO test
    :param account:
    :param diff_value:
    :return:
    """
    new_value = max(account.number_magic_bone + diff_value, 0)
    account.number_magic_bone = new_value
    account.save()
