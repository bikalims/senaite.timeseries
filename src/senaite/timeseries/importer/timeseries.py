import json
import traceback
from os.path import abspath

from bika.lims import api
from bika.lims.api.analysisservice import get_by_keyword as get_as_by_keyword
from bika.lims import bikaMessageFactory as _
from senaite.core.exportimport.instruments import IInstrumentAutoImportInterface
from senaite.core.exportimport.instruments import IInstrumentImportInterface
from senaite.core.exportimport.instruments.importer import AnalysisResultsImporter
from bika.lims.utils import t
from senaite.instruments.instrument import InstrumentXLSResultsFileParser
from zope.interface import implements


class TimeSeriesParser(InstrumentXLSResultsFileParser):
    """Parser"""

    def __init__(self, infile, worksheet=2, encoding=None, instrument_uid=None):
        InstrumentXLSResultsFileParser.__init__(
            self, infile, worksheet=worksheet, encoding=encoding, data_only=True
        )
        self._end_header = False
        self._ar_id = None
        # self._instrument = api.get_object(instrument_uid, None)
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

        if splitted[0] == "Analysis":
            keyword = splitted[1].strip()
            if not keyword:
                return 0
            brains = get_as_by_keyword(keyword)
            if len(brains) != 1:
                return 0
            AS = api.get_object(brains[0])
            if not AS:
                return 0
            self._analysis_service = AS
            if AS.TimeSeriesColumns:
                self._column_headers = [
                    col["ColumnTitle"] for col in AS.TimeSeriesColumns
                ]

        if splitted[0] == "Start Date":
            self._start_date = splitted[1].strip()

        return 0

    def format_values(self, result):
        precision = self._analysis_service.Precision
        float_fmt = "{:0." + str(precision) + "f}"
        formatted = []
        for value in result:
            try:
                value = int(value)
                value = "%d" % value
                formatted.append(value)
                continue
            except Exception:
                pass
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

    def Import(self, context, request):
        """Import Form"""
        infile = request.form["instrument_results_file"]
        fileformat = request.form.get("instrument_results_file_format", "xlsx")
        artoapply = request.form.get("artoapply")
        override = request.form.get("results_override")
        instrument_uid = request.form.get("instrument")
        worksheet = int(request.form.get("worksheet", "2"))
        errors = []
        logs = []
        warns = []

        # Load the most suitable parser according to file extension/options/etc...
        parser = None
        if not hasattr(infile, "filename"):
            errors.append(_("No file selected"))
        if fileformat in ("xls", "xlsx"):
            parser = TimeSeriesParser(
                infile, worksheet, encoding=fileformat, instrument_uid=instrument_uid
            )
        else:
            errors.append(
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
                status = ["sample_received", "attachment_due", "to_be_verified"]

            over = [False, False]
            if override == "nooverride":
                over = [False, False]
            elif override == "override":
                over = [True, False]
            elif override == "overrideempty":
                over = [True, True]

            importer = AnalysisResultsImporter(
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
                errors = importer.errors
                logs = importer.logs
                warns = importer.warns
            except Exception:
                tbex = traceback.format_exc()
                errors.append(tbex)

        results = {"errors": errors, "log": logs, "warns": warns}

        return json.dumps(results)
