import json
import traceback
from os.path import abspath

from bika.lims import api
from bika.lims.api.analysisservice import get_by_keyword as get_as_by_keyword
from bika.lims import bikaMessageFactory as _
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.exportimport.instruments import (
    IInstrumentAutoImportInterface,
    IInstrumentImportInterface,
)
from senaite.core.exportimport.instruments.importer import (
    ALLOWED_ANALYSIS_STATES,
    ALLOWED_SAMPLE_STATES,
    AnalysisResultsImporter,
)
from bika.lims.utils import t
from senaite.instruments.instrument import InstrumentXLSResultsFileParser
from zope.interface import implements


class TimeSeriesParser(InstrumentXLSResultsFileParser):
    """Parser"""

    def __init__(
            self, infile, worksheet=2, encoding=None, instrument_uid=None):
        InstrumentXLSResultsFileParser.__init__(
            self,
            infile,
            worksheet=worksheet,
            encoding=encoding,
            data_only=True
        )
        self._end_header = False
        self._ar_id = None
        self._instrument = api.get_object(instrument_uid, None)
        self._analysis_service = None
        self._column_headers = []
        self._result = []

    def _parseline(self, line):
        if self._end_header:
            return self.parse_resultsline(line)
        return self.parse_headerline(line)

    def parse_headerline(self, line):
        """Parses header lines"""
        if self._end_header:
            # Header already processed
            return 0

        splitted = [token.strip() for token in line.split(self._delimiter)]
        if splitted[0] == "Data":
            self._end_header = True

        if splitted[0] == "Sample ID":
            self._ar_id = splitted[1].strip()
            if self._ar_id is None or len(self._ar_id) == 0:
                self.err("Sample ID not provided")
                return -1

            query = {"portal_type": "AnalysisRequest", "id": self._ar_id}
            brains = api.search(query, SAMPLE_CATALOG)
            if len(brains) == 0:
                self.err("Sample ID {} does not exist".format(self._ar_id))
                return -1

        if splitted[0] == "Analysis":
            keyword = splitted[1].strip()
            if not keyword:
                self.err("Analysis not provided")
                return -1
            brains = get_as_by_keyword(keyword)
            if len(brains) != 1:
                self.warn("Anaysis Service {} not found".format(keyword))
                return -1
            AS = api.get_object(brains[0])
            if not AS:
                self.warn(
                    "Anaysis Service object for {} not found".format(keyword)
                )
                return -1
            try:
                kw_obj = AS.getKeyword()
            except Exception:
                self.warn(
                    "Anaysis Service object for {} not found".format(kw_obj)
                )
                return -1

            self._analysis_service = AS
            if not hasattr(AS, "TimeSeriesColumns"):
                self.warn(
                    "Anaysis Service {} is not Timeseries result type".format(
                        keyword
                    )
                )
                return -1
            self._column_headers = [
                col["ColumnTitle"] for col in AS.TimeSeriesColumns
            ]

        if splitted[0] == "Start Date":
            self._start_date = splitted[1].strip()
            if not self._start_date:
                self.warn("Start date not provided")
                return -1

        return 0

    def format_values(self, result):
        precision = self._analysis_service.Precision
        column_data = self._analysis_service.TimeSeriesColumns
        float_fmt = "{:0." + str(precision) + "f}"
        formatted = []
        for idx, value in enumerate(result):
            col_type = column_data[idx].get("ColumnDataType", "number")
            if col_type == "number":
                try:
                    value = int(value)
                    value = "%d" % value
                    formatted.append(value)
                    continue
                except Exception:
                    pass
            if col_type == "float":
                try:
                    value = float(value)
                    value = float_fmt.format(value)
                    formatted.append(value)
                    continue
                except Exception:
                    pass
            formatted.append(value)
        return formatted

    def parse_resultsline(self, line):
        """Parses result lines"""
        if len(self._column_headers) == 0:
            return 0

        splitted = [token.strip() for token in line.split(self._delimiter)]
        if len(filter(lambda x: len(x), splitted)) == 0:
            return 0

        # Header 1
        if splitted[1] == self._column_headers[0]:
            self._header = splitted
            return 0

        result = splitted[1 : len(self._column_headers) + 1]  # noqa
        result = self.format_values(result)
        self._result.append(result)

        return 0

    def getRawResults(self):
        # TODO Validatiom required
        if self._analysis_service is None:
            return {self._ar_id: {}}
        result = [
            {
                self._analysis_service.getKeyword(): {
                    "DefaultResult": "result",
                    "result": self._result,
                }
            }
        ]
        return {self._ar_id: result}


class timeseries_import(object):
    implements(IInstrumentImportInterface, IInstrumentAutoImportInterface)
    title = "TimeSeries Importer"
    __file__ = abspath(__file__)  # noqa

    def __init__(self, context):
        self.context = context
        self.request = None
        self.allowed_sample_states = ALLOWED_SAMPLE_STATES
        self.allowed_analysis_states = ALLOWED_ANALYSIS_STATES
        self.errors = []
        self.logs = []
        self.warns = []

    def Import(self, context, request, parser=None):
        """Import Form"""
        if request is not None:
            infile = request.form["instrument_results_file"]
            fileformat = request.form.get(
                "instrument_results_file_format", "xlsx"
            )
            artoapply = request.form.get("artoapply")
            override = request.form.get("results_override")
            instrument_uid = request.form.get("instrument")
            worksheet = int(request.form.get("worksheet", "2"))
        else:
            # Auto_importer hack
            artoapply = "received_tobeverified"
            override = "overrideempty"
            instrument_uid = None
            worksheet = 2

        if hasattr(self, "parser"):
            # Auto improt hack
            parser = self.parser
        else:
            # Load the most suitable parser according to
            # file extension/options/etc...
            parser = None
            if not hasattr(infile, "filename"):
                self.errors.append(_("No file selected"))
            if fileformat in ("xls", "xlsx"):
                parser = TimeSeriesParser(
                    infile,
                    worksheet,
                    encoding=fileformat,
                    instrument_uid=instrument_uid,
                )
            else:
                self.errors.append(
                    t(
                        _(
                            "Unrecognized file format ${fileformat}",
                            mapping={"fileformat": fileformat},
                        )
                    )
                )

        if parser:
            # Load the importer
            status = ["sample_received", "attachment_due", "to_be_verified"]
            if artoapply == "received":
                status = ["sample_received"]
            elif artoapply == "received_tobeverified":
                status = ["sample_received",
                          "attachment_due",
                          "to_be_verified",
                          ]

            over = [False, False]
            if override == "nooverride":
                over = [False, False]
            elif override == "override":
                over = [True, False]
            elif override == "overrideempty":
                over = [True, True]

            importer = TimeSeriesImporter(
                parser=parser,
                context=context,
                allowed_sample_states=status,
                allowed_analysis_states=None,
                override=over,
                instrument_uid=instrument_uid,
            )
            tbex = ""
            try:
                importer.process()
                if (
                    not importer._parser._result
                    or len(importer._parser._result) == 0
                ):
                    self.errors.append("No data found")
                self.errors.extend(importer.errors)
                self.logs.extend(importer.logs)
                self.warns.extend(importer.warns)
            except Exception:
                tbex = traceback.format_exc()
                self.errors.append(tbex)

        results = {"errors": self.errors,
                   "log": self.logs,
                   "warns": self.warns}

        return json.dumps(results)

    def get_automatic_importer(self, instrument, parser, **kw):
        """Called during automated results import"""
        # initialize the base class with the required parameters
        if parser._instrument is None:
            parser._instrument = instrument
        self.parser = parser
        return self

    def get_automatic_parser(self, infile):
        """Called during automated results import

        Returns the parser to be used by default for the file passed in when
        automatic results import for this instrument interface is enabled
        """
        return TimeSeriesParser(infile, encoding="xlsx")

    def process(self):
        results = self.Import(self.context, request=None, parser=self.parser)
        return results


class TimeSeriesImporter(AnalysisResultsImporter):
    def __init__(
        self,
        parser,
        context,
        override,
        allowed_sample_states=None,
        allowed_analysis_states=None,
        instrument_uid="",
        form=None,
    ):
        AnalysisResultsImporter.__init__(
            self,
            parser,
            context,
            override,
            allowed_sample_states,
            allowed_analysis_states,
            instrument_uid,
        )

    def parse_results(self):
        """Parse the results file and return the raw results"""
        parsed = self.parser.parse()

        self.errors = self.parser.errors
        self.warns = self.parser.warns
        self.logs = self.parser.logs

        if not parsed:
            return {}

        return self.parser.getRawResults()
