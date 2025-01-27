# -*- coding: utf-8 -*-

import datetime
import os
from bika.lims import api
from plone.protect.interfaces import IDisableCSRFProtection
from senaite.core.exportimport.auto_import_results import AutoImportResultsView as AIRV
from zope.interface import alsoProvides

CR = "\n"
LOGFILE = "logs.log"
INDEXFILE = "imported.csv"
IGNORE = ",".join([INDEXFILE, LOGFILE])


class AutoImportResultsView(AIRV):
    def __call__(self):
        # disable CSRF because
        alsoProvides(self.request, IDisableCSRFProtection)
        # run auto import of results
        self.auto_import_results()
        # return the concatenated logs
        logs = CR.join(self.logs)
        return logs

    def auto_import_results(self):
        """Auto import all new instrument import files"""
        for brain in self.query_active_instruments():
            interfaces = []
            instrument = api.get_object(brain)
            # instrument_title = api.get_title(instrument)

            # get a valid interface -> folder mapping
            mapping = self.get_interface_folder_mapping(instrument)

            # If Import Interface ID is specified in request, then auto-import
            # will run only that interface. Otherwise all available interfaces
            # of this instruments
            if self.request.get("interface"):
                interfaces.append(self.request.get("interface"))
            else:
                interfaces = mapping.keys()

            if not interfaces:
                # self.log("No active interfaces defined", instrument=instrument)
                continue

            if (
                "senaite.timeseries.importer.timeseries.timeseries_import"
                not in interfaces
            ):
                continue

            # self.log(
            #     "Auto import for '%s' started ..." % instrument_title,
            #     instrument=instrument,
            #     level="info",
            # )
            # import instrument results from all configured interfaces
            for interface in interfaces:
                folder = mapping.get(interface)
                # check if instrument import folder exists
                if not os.path.exists(folder):
                    self.log(
                        "Interface %s: Folder %s does not exist" % (interface, folder),
                        instrument=instrument,
                        interface=interface,
                        level="error",
                    )
                    continue

                log_file_path = os.path.join(folder, LOGFILE)
                # get all files in the instrument folder
                if os.path.exists(log_file_path):
                    log_file_mod_date = datetime.datetime.fromtimestamp(
                        os.path.getmtime(log_file_path)
                    )
                    allfiles = self.list_files(
                        folder, ignore=IGNORE, exclude_before=log_file_mod_date
                    )
                else:
                    allfiles = self.list_files(folder, ignore=IGNORE)

                if len(allfiles) == 0:
                    self.log(
                        "Interface '%s': Folder %s has no new files"
                        % (interface, folder),
                        instrument=instrument,
                        interface=interface,
                        level="info",
                    )
                    # crate auto import log object
                    logobj = self.create_autoimportlog(instrument, interface, "")
                    # write import logs
                    self.write_autologs(logobj, self.logs, "info")
                    continue

                # import results file
                for f in allfiles:
                    self.import_results(instrument, interface, folder, f)

            # self.log("Auto-Import finished")

    def list_files(self, folder, ignore="", exclude_before=None):
        """Returns all files in folder and its subfolders, excluding ignored files and files modified before a given date.

        :param folder: folder path
        :param ignore: comma-separated list of file names to ignore
        :param exclude_before: datetime object; exclude files modified before this date
        """
        files = []
        ignore_files = ignore.split(",") if ignore else []

        for root, _, filenames in os.walk(folder):
            for f in filenames:
                # skip hidden files
                if f.startswith("."):
                    continue
                # skip ignored files
                if f in ignore_files:
                    continue

                file_path = os.path.join(root, f)
                # skip files modified before the exclude_before date
                if exclude_before:
                    file_mod_time = datetime.datetime.fromtimestamp(
                        os.path.getmtime(file_path)
                    )
                    if file_mod_time < exclude_before:
                        continue

                files.append(file_path)

        return files
