import gzip
import io
import timeit
from contextlib import contextmanager
from datetime import datetime

from typing_extensions import List, TypeVar


def zulu_time_now_str():
    return datetime.utcnow().isoformat()


@contextmanager
def timeit_context(name=""):
    start_time = timeit.default_timer()
    yield
    end_time = timeit.default_timer()
    print(f"{name} Execution time: {end_time - start_time} seconds")


T = TypeVar("T")


def split_list(lst: List[T], n: int) -> List[List[T]]:
    "split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3) -> [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]"
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)]


def ungzip_bytes_to_text(gzip_bytes):
    with gzip.GzipFile(fileobj=io.BytesIO(gzip_bytes)) as gz:
        text_content = gz.read().decode("utf-8")

    return text_content
