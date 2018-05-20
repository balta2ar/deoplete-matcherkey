try:
    from .base import Base
except:
    class Base:
        pass

import re


def log(msg):
    with open('/tmp/deoplete-matcherkey.log', 'a') as file_:
        file_.write('%s\n' % msg)


PREFIX_PATTERN = r'HG:?\w*$'

JIRA_CANDIDATES = """
OFFICE_IT-1257	Fix hg hook in cs/rnd-tests repo	Resolved	user1	2018-02-27
IT_SUPPORT-236	Configure certificates on https://someurl.company.net	Resolved	user2	2018-03-02
IT_DEV-319	Hypertext links to Crucible reviews in RT comments	On Hold	<NA>	2018-03-12
GENERAL-1874	Re: changes for 2018 (high level summary)	New	<NA>	2018-03-10
DEMO-56 my test	Open	user3	2018-03-06
ACCESS-6092	Please create bot user for SecretProject <-> TopSecretProject interaction	Resolved	user4	2018-03-05
ACCESS-2432	wrong permissions in test project. user1	Resolved	user1	2018-02-27
"""


def get_jira_candidates(current_prefix):
    # current_prefix == context['complete_str']
    candidates = [line.split('\t')[:2]
                  for line in JIRA_CANDIDATES.strip().splitlines()]
    return [{'word': ticket,
             'abbr': ticket + ' ' + title,
             'custom_key': current_prefix + title, }
            for ticket, title in candidates]


def get_branch_name_candidates(current_prefix):
    branch_names = sorted([
        'feature/RT123456_implement_proxy_support',
        'feature/RT123450_add_rate_limiting',
        'feature/RT123451_add_role_processing',
        'default',
        'stable',
    ])
    return [{'word': 'word%s' % i,
             'abbr': current_prefix + name, }
            for i, name in enumerate(branch_names)]


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
        self.input_pattern = PREFIX_PATTERN

        self.matcher_key = 'custom_key'

    def get_complete_position(self, context):
        m = re.search(self.input_pattern, context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        context['is_async'] = False
        from pprint import pformat
        log('CONTEXT: %s' % pformat(context))

        # return get_jira_candidates('')
        return get_jira_candidates(context['complete_str'])
        # return get_branch_name_candidates(context['complete_str'])
