## senaite.timeseries

**Time Series Results Add-on for Senaite / Ingwe Bika LIMS**

This add-on extends **Senaite** (the modern core of Bika LIMS) with powerful time-series functionality for laboratory results that evolve over time.

### What is senaite.timeseries?

`senaite.timeseries` allows labs to capture, view, and analyse results that are measured repeatedly on the same sample or object at different time points.

It is particularly useful for:

- Concrete compressive strength testing (7, 28, 56, 90-day breaks)
- Stability studies and shelf-life testing
- Environmental monitoring (e.g. water quality trends)
- Long-term product or material testing
- Trend analysis and graphical reporting

### Key Features

- Capture multiple results for the same analysis at different time intervals
- Beautiful tabular and graphical (chart) presentation of time-series data
- Trend visualisation directly in the LIMS interface
- Time-series data and charts on COAs
- Full integration with Bika/Senaite workflows, calculations, and reporting
- Audit trail and ISO-compliant data integrity

### Requirements

- **Senaite** (latest recommended) or **Ingwe Bika LIMS 4**

### Installation

#### For Ingwe Bika LIMS 4 (Docker – Recommended)

Add `senaite.timeseries` to your custom add-ons list in the Ingwe Bika Docker configuration.

##### Classic Buildout

Add the package to your `buildout.cfg`:

cfg
[buildout]
eggs =
    ...
    senaite.timeseries

##### For Docker

### Documentation
[Time Series in the Bika User Manual](https://www.bikalims.org/new-manual/analysis-services/time-series-analyses)

### License
This project is licensed under the GNU General Public License v2.0 (GPL-2.0).

### Support & Professional Services
[Bika Lab Systems](www.bikalabs.com) provides professional implementation, training, custom development, and ongoing support for senaite.timeseries and the full Ingwe Bika LIMS suite.

Website: [https://www.bikalims.org](https://www.bikalims.org)

Made with ❤️ in Cape Town, South Africa
