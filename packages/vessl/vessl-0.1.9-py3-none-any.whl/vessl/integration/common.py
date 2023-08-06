import os
from collections import defaultdict
from datetime import datetime
from numbers import Number
import typing
from typing import Dict, List, Optional, SupportsFloat, Union

from openapi_client.models import (
    InfluxdbExperimentPlotFile,
    InfluxdbExperimentPlotMetric,
    ResponseExperimentInfo,
)
from vessl import vessl_api
from vessl.experiment import (
    read_experiment_by_id,
    update_experiment_plots_files,
    update_experiment_plots_metrics,
)
from vessl.util import logger
from vessl.util.constant import VESSL_IMAGE_PATH, VESSL_PLOTS_FILETYPE_IMAGE
from vessl.util.exception import VesslApiException
from vessl.util.image import Image
from vessl.volume import copy_volume_file

ImageRowType = Dict[str, List[Image]]
MetricRowType = Dict[str, SupportsFloat]
RowType = Union[ImageRowType, MetricRowType]

current_experiment: Optional[ResponseExperimentInfo] = None


def _update_current_experiment():
    global current_experiment
    experiment_id = os.environ.get("VESSL_EXPERIMENT_ID", None)
    access_token = os.environ.get("VESSL_ACCESS_TOKEN", None)

    if experiment_id is None or access_token is None:
        return

    vessl_api.update_access_token(access_token)
    current_experiment = read_experiment_by_id(int(experiment_id))


def get_current_experiment() -> Optional[ResponseExperimentInfo]:
    global current_experiment
    if current_experiment != None:
        return current_experiment

    _update_current_experiment()
    return current_experiment

def get_current_experiment_id() -> int:
    assert current_experiment
    assert current_experiment.id
    return current_experiment.id

def _update_images(row: ImageRowType):
    if not current_experiment:
        return

    path_to_caption = {}
    for images in row.values():
        for image in images:
            path_to_caption[image.path] = image.caption

    source_path = os.path.join(VESSL_IMAGE_PATH, "")
    dest_volume_id = current_experiment.experiment_plot_volume
    dest_path = "/"

    files = copy_volume_file(
        source_volume_id=None,
        source_path=source_path,
        dest_volume_id=dest_volume_id,
        dest_path=dest_path,
        recursive=True,
    )

    for images in row.values():
        for image in images:
            image.flush()

    if files:
        plot_files = [
            InfluxdbExperimentPlotFile(
                step=None,
                path=file.path,
                caption=path_to_caption[file.path],
                timestamp=datetime.utcnow().timestamp(),
            )
            for file in files
            if file.path in path_to_caption
        ]
    else:
        plot_files = []

    workload_id = os.environ.get("VESSL_WORKLOAD_ID", None)
    assert workload_id

    id = get_current_experiment_id()

    update_experiment_plots_files(
        experiment_id=id,
        workload_id=int(workload_id),
        files=plot_files,
        type=VESSL_PLOTS_FILETYPE_IMAGE,
    )


def _update_metrics(row: MetricRowType, step: int):
    if not current_experiment:
        return

    plot_metrics: Dict[str, List[InfluxdbExperimentPlotMetric]] = defaultdict(list)

    for key, val in row.items():
        plot_metrics[key].append(
            InfluxdbExperimentPlotMetric(
                step=step,
                timestamp=datetime.utcnow().timestamp(),
                value=float(val),
            )
        )

    workload_id = os.environ.get("VESSL_WORKLOAD_ID", None)
    assert workload_id

    update_experiment_plots_metrics(
        experiment_id=get_current_experiment_id(),
        workload_id=int(workload_id),
        metrics=plot_metrics,
    )


def _log(row: RowType, step: int = None):
    # TODO: type validation? (ref: legacy client)
    # row, step = _refine(row, step)

    for val in row.values():
        if isinstance(val, list) and all(isinstance(i, Image) for i in val):
            _update_images(typing.cast(ImageRowType, row))
        else:
            assert step
            _update_metrics(typing.cast(MetricRowType, row), step)
        break


def log(row: RowType, step: int = None):
    """Log a metric during a Vessl experiment.

    This function must be called on the Vessl infrastructure to log the metric.
    If not executed on Vessl's infrastructure, this function has no effect.

    :param row: a dictionary to log (required)
    :param step: a step(positive integer) for each iteration
    """

    _update_current_experiment()

    try:
        _log(row, step)

    except VesslApiException as e:
        logger.warn(f"Cannot send metrics {row} for step {step}: {e.message}")
