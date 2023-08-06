import sys
import numpy as np
from numpy.typing import ArrayLike, NDArray


def check_two_array(
        a: ArrayLike, b: ArrayLike,
        *,
        is_same_size: bool = False,
        is_same_shape: bool = False,
        is_clean_same_time: bool = False,
        is_nan_warning: bool = False,
        nan_warning_criterion=0.3
) -> (NDArray, NDArray):
    """
    检查并转换两个数组
    :param a: ArrayLike
    :param b: ArrayLike
    :param is_same_size: 是否检查相同 size
    :param is_same_shape: 是否检查相同 shape
    :param is_clean_same_time: 是否由两个数组的 nan 值共同决定清洗
    :param is_nan_warning: nan 值过多时是否提出 warning
    :param nan_warning_criterion: nan 值超过 size 的百分率 warning（仅在 is_nan_warning=True 时生效）
    :return:
    """
    a = np.asarray(a)
    b = np.asarray(b)

    if is_same_size:
        if a.size != b.size:
            raise ValueError(f'Expect two array have then same size, but got {a.size} and {b.size}')

    if is_same_shape:
        if a.shape != b.shape:
            raise ValueError(f'Expect two array have then same shape, but got {a.shape} and {b.shape}')

    if is_clean_same_time:
        not_nan = np.logical_not(np.logical_or(np.isnan(a), np.isnan(b)))
        a = a[not_nan]
        b = b[not_nan]

    if is_nan_warning:
        for _arr in [a, b]:
            nan_warning_criterion = check_int(
                nan_warning_criterion,
                is_lower_closed=True,
                is_upper_closed=True,
                minimum=0, maximum=1
            )
            if np.count_nonzero(np.isnan(_arr)) >= _arr.size * nan_warning_criterion:
                raise RuntimeWarning('Input array nan value have too much')

    return a, b


def check_int(
        a: int,
        *,
        is_upper_closed: bool = False,
        is_lower_closed: bool = False,
        minimum: int = -sys.maxsize,
        maximum: int = sys.maxsize
) -> int:
    """
    检查整数是否在范围中
    :param a: 整数
    :param is_upper_closed: 上限是否为闭区间
    :param is_lower_closed: 下限是否为闭区间
    :param minimum: 区间最小值
    :param maximum: 区间最大值
    :return:
    """
    a = int(a)
    if not minimum <= a <= maximum:
        raise ValueError
    if not is_lower_closed and a == minimum:
        raise ValueError
    if not is_upper_closed and a == maximum:
        raise ValueError

    return a
