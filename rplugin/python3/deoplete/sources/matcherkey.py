try:
    from .base import Base
except:
    class Base:
        pass

import re


HG_PATTERN = r'HG:?\w*$'


def get_branch_names():
    return sorted([
        'HGfeature/RT123456_implement_proxy_support',
        'HGfeature/RT123450_add_rate_limiting',
        'HGfeature/RT123451_add_role_processing',
        'HGdefault',
        'HGstable',
    ])


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.debug_enabled = False
        self.name = 'MK'
        self.mark = '[MK]'

        self.is_volatile = False
        self.matchers = ['matcher_cpsm']
        # self.sorters = []

        # self.matchers = ['matcher_fuzzy', 'matcher_full_fuzzy']
        # self.sorters = ['sorter_rank']
        # self.converters = []

        self.max_menu_width = 120
        self.max_abbr_width = 120
        self.input_pattern = HG_PATTERN

        self.matcher_key = 'abbr'

    def get_complete_position(self, context):
        m = re.search(self.input_pattern, context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        context['is_async'] = False

        return [{'word': 'word%s' % i, 'abbr': name, }
                for i, name in enumerate(get_branch_names())]
