# -*- coding: utf-8 -*-

import re
import requests
import warnings

from bs4 import BeautifulSoup, Comment
from optparse import make_option
from time import time

from django.core.management.base import BaseCommand
from django.db.models import Q

from helpck.customs import get_hostname
from helpck.lang_detect import classify
from helpck.models import Lead
from helpck.utils import PagedQueryset


UNKNOWN = None
OK = 'OK'
DOUBTFUL = 'DOUBTFUL'
ERROR = 'ERROR'
TOO_FEW_CHARACTERS = 'TOO_FEW_CHARACTERS'
TIMEOUT = 'TIMEOUT'
EXCEPTION = 'PYTHON_EXCEPTION'


class Command(BaseCommand):
    help = """Update Leads by guessing the language of the website.
Usage:
./manage.py lead_detect_lang
./manage.py lead_detect_lang --limit=100
./manage.py lead_detect_lang --url='http://www.example.com'
To display info in stdout use:
./manage.py lead_detect_lang -v 2
./manage.py lead_detect_lang --verbosity=2
"""

    option_list = BaseCommand.option_list + (
        make_option("--limit", action="store", dest="limit",
                    help="Max number of Leads to process."),
        make_option("--url", action="store", dest="url",
                    help="Process a single URL."),
        make_option("--include", action="store", dest="includes",
                    help="Include previuosly failed sites.\n"
                         "--include=\"TIMEOUT,TOO_FEW_CHARACTERS,ERROR\""),
        make_option("--count", action="store_true", dest="count",
                    help="Count only leads matching the options."),
    )

    log_results = False

    def handle(self, **options):
        """ Process the leads based on the options passed.
        By default it does not print anything to stdout. To do so, please set
        verbosity to greater than 1 (the default value).
        - To process a single URL use the --url=URL option.
        - When processing multiple URLs use --count to return the number of
          leads that match the query.
        - If you use --count and --limit the smallest value will be returned.
        - To include previously processed leads use --include with a list of
          comma-separated values from this list:
                TIMEOUT
                ERROR
                TOO_FEW_CHARACTERS
                DOUBTFUL
          ./manage.py lead_detect_lang --include="TIMEOUT,DOUBTFUL"
        To start processing in "a saco paco" mode just use:
            ./manage.py lead_detect_lang &
        To log results somewhere:
            ./manage.py lead_detect_lang -v 2 > /path/to/logfile &
        """
        start = time()
        total_processed = 0
        total_items = 0

        self.log_results = options.get('verbosity', 1) > 1

        if options.get('url'):
            total_items = 1
            language, status, confidence = self.process_url(options.get('url'))

            if status == OK:
                total_processed += 1

            self.log_result(options.get('url'), language, confidence, status)

        else:
            try:
                all_leads_qs = Lead.objects

                if options.get('includes'):
                    # Process not processed leads
                    stat_condition_1 = Q(zoho_web_status__isnull=True) & \
                        Q(zoho_website_language__isnull=True)
                    # OR process leads with any of the following statuses
                    stat_condition_2 = None

                    for include in [Q(zoho_web_status=x.strip().upper())
                                    for x in options.get('includes').split(',')
                                    if x.strip().upper() in (
                                        TIMEOUT,
                                        TOO_FEW_CHARACTERS,
                                        ERROR,
                                        DOUBTFUL
                                    )]:
                        if not stat_condition_2:
                            stat_condition_2 = include
                        else:
                            stat_condition_2 = stat_condition_2 | include

                    if not stat_condition_2:
                        all_leads_qs = all_leads_qs.filter(stat_condition_1)
                    else:
                        all_leads_qs = all_leads_qs\
                            .filter(stat_condition_1 | stat_condition_2)
                else:
                    # Include only non processed leads
                    all_leads_qs = all_leads_qs.filter(
                        zoho_web_status__isnull=True,
                        zoho_website_language__isnull=True
                    )

                all_leads_qs = all_leads_qs.order_by('id')

                # How many leads would be processed with the selected options?
                if options.get('count'):
                    n = all_leads_qs.count()
                    if options.get('limit'):
                        n = min(int(options.get('limit')), n)

                    print "%d leads would be processed." % n
                    return

                paged_qs = PagedQueryset(all_leads_qs)
                if options.get('limit'):
                    paged_qs.limit(int(options.get('limit')))

                total_items = paged_qs.count

                for lead_qs in paged_qs.iterator():
                    for lead in lead_qs:
                        total_processed += 1 if self.process_lead(lead) else 0

            except KeyboardInterrupt:
                raise

        if self.log_results:
            print "Procesed %d of %d in %.2f seconds." % (
                total_processed,
                total_items,
                time() - start
            )

    def process_url(self, url):
        """ Process a single URL
        The text extracted must be at least 20 characters length.
        Args:
            url, string.
        Returns:
            Tuple containing in this order:
            - language
            - status
            - confidence (float between 0 and 1)
        """
        language = UNKNOWN
        confidence = 0.0
        status = UNKNOWN

        try:
            host = get_hostname(url)

            response = requests.get(host, allow_redirects=True, timeout=5)

            warnings.filterwarnings("ignore")
            input_text = response.text.strip()

            if len(input_text) == 1 and isinstance(input_text, basestring):
                input_text += ' '

            soup = BeautifulSoup(input_text)
            [s.extract() for s in soup(['style', 'script', '[document]',
                                        'head', 'title'])]
            [c.extract() for c in soup.findAll(
                text=lambda x: isinstance(x, Comment))]

            try:
                input_text = soup.body.getText(separator=u' ')
            except AttributeError:
                # No soup.body
                pass

            input_text = re.sub("\s+", " ", input_text).strip()

            if len(input_text) < 20:
                raise ValueError("input must be at least 20 characters long")

            language, confidence = classify(input_text)
            if int(confidence) == 1:
                status = OK
            else:
                status = DOUBTFUL

        except requests.exceptions.Timeout:
            language = UNKNOWN
            status = TIMEOUT

        except requests.exceptions.RequestException:
            language = UNKNOWN
            status = ERROR

        except ValueError:
            language = UNKNOWN
            status = TOO_FEW_CHARACTERS

        except Exception as e:
            language = UNKNOWN
            status = EXCEPTION

        finally:
            return (language, status, confidence)

    def process_lead(self, lead):
        """ Process a single lead and save the results in db.
        Args:
            lead, Lead object.
        Returns:
            Boolean, True if status is OK or DOUBTFUL (confidence < 1)
        """
        language, status, confidence = self.process_url(lead.zoho_website)

        lead.zoho_website_language = language
        lead.zoho_web_status = status
        lead.save()

        self.log_result(lead.zoho_website, language, confidence, status)

        return status == OK or status == DOUBTFUL

    def log_result(self, website, language, confidence, status):
        """ If the command was configured as verbose, prints a log message """
        if self.log_results:
            print "%s - %s (%s) - %s" % (website, language, confidence, status)