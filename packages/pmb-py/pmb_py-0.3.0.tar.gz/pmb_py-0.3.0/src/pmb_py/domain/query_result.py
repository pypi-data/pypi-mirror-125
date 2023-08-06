import os
from typing import Iterable
import re


PMBAPI_URL = os.environ['PMB_API_URL']


class QueryResult:
    def __init__(self,
                 limit: int = 1000,
                 next: str = '',
                 previous: str = '',
                 results: Iterable = list(),
                 start: int = 0,
                 total_count: int = 0,
                 ):
        self.limit = limit
        self.next = next
        self.previous = previous
        self.results = results
        self.start = start
        self.total_count = total_count

    def first(self):
        if not self.results:
            return None
        for item in self.results:
            return item

    def next_start(self):
        '''下一個起始數'''
        re_str = r'start=([0-9]+)'
        return int(re.search( re_str, self.next).group(1))

        # '/blocks?project_id=937&start=1001&limit=1000'
    # def __next__(self):
    #     if self._iter_count+1 < self.total_count:
    #         if self._next_count+1 < self.limit:
    #         return _next(self)
    #     elif self._object:
        
    #     else:
    #         raise StopIteration

    # def _next(re_obj):
    #     if re_obj._next_count+1 < re_obj.limit:
    #         # print(re_obj.start + re_obj._next_count)
    #         item = re_obj._to_list[re_obj._next_count]
    #         re_obj._next_count += 1
    #         return self._to_obj(item)
    #     elif re_obj.next:
    #         re = core._session.get(self.next)
    #         return _next(re)
    #     else:
    #         raise StopIteration


# class QueryResult2:
#     def __init__(self, pmb_pagenation_query_result):
#         self._re = pmb_pagenation_query_result

#     @property
#     def results(self):
#         return self._re.results
    
#     @property
#     def next(self):
#         return self._re.next
    
#     @property
#     def previous(self):
#         return self._re.previous

#     @property
#     def start(self):
#         return self._re.start
    
#     @property
#     def limit(self):
#         return self._re.limit

#     @property
#     def total_count(self):
#         return self._re.total_count

#     def first(self):
#         if not self._re.results:
#             return None
#         for item in self._re.results:
#             return item

#     def next_start(self):
#         re_str = r'start=([0-9]+)'
#         return int(re.search( re_str, self._re.next).group(1))