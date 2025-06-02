import logging # loggingモジュールをインポート
import dateutil
import numpy
import matplotlib.pyplot
import matplotlib.dates
import matplotlib.ticker
import astropy.time
import astropy.coordinates
from astropy.coordinates import name_resolve # 追加
from typing import List, Dict, Tuple, Any

import io

from components.get_site import get_site
from components.get_localtime import get_localtime

from astropy.utils.iers import conf as iers_conf
iers_conf.remote_timeout = 30.0

# ロガーの設定 (モジュールのトップレベルで行う)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # INFOレベル以上のログを出力 (ERRORも含む)
# Vercelの環境では通常、標準出力や標準エラー出力へのログは自動的に収集されるため、
# 特定のハンドラ設定は不要な場合が多い。

# 現在のAstropy名前解決サービスリストをログに出力 # 追加
logger.info(f"Default Astropy name resolve services: {name_resolve.NAME_RESOLVE_SERVICES}")
print(f"DEBUG_PRINT: Default Astropy name resolve services: {name_resolve.NAME_RESOLVE_SERVICES}")

# Sesame ('cds') 以外のサービスを優先する試み # 追加
current_services = name_resolve.NAME_RESOLVE_SERVICES.copy()
preferred_order = []
other_services = []

if 'simbad' in current_services:
    preferred_order.append('simbad')
    current_services.pop(current_services.index('simbad'))
if 'ned' in current_services:
    preferred_order.append('ned')
    current_services.pop(current_services.index('ned'))

other_services = current_services

if preferred_order:
    name_resolve.NAME_RESOLVE_SERVICES = preferred_order + other_services
    logger.info(f"Updated Astropy name resolve services to: {name_resolve.NAME_RESOLVE_SERVICES}")
    print(f"DEBUG_PRINT: Updated Astropy name resolve services to: {name_resolve.NAME_RESOLVE_SERVICES}")
else:
    logger.info("Could not change preferred name resolve services (simbad or ned not found in list).")
    print("DEBUG_PRINT: Could not change preferred name resolve services (simbad or ned not found in list).")

# 定数は大文字で定義
FIG_SIZE = (10, 8)
PLOT_DPI = 200


def setup_plot_style(timezone: str) -> Tuple[
    matplotlib.dates.DateFormatter, 
    matplotlib.dates.HourLocator, 
    matplotlib.ticker.MultipleLocator, 
    matplotlib.ticker.MultipleLocator, 
    matplotlib.ticker.MultipleLocator, 
    matplotlib.ticker.MultipleLocator
]:
    matplotlib.rcParams["font.family"] = "serif"
    matplotlib.rcParams["xtick.top"] = True
    matplotlib.rcParams["xtick.bottom"] = True
    matplotlib.rcParams["xtick.direction"] = "in"
    matplotlib.rcParams["ytick.left"] = True
    matplotlib.rcParams["ytick.right"] = True
    matplotlib.rcParams["ytick.direction"] = "in"

    date_locator = matplotlib.dates.HourLocator()
    date_formatter = matplotlib.dates.DateFormatter(
        "%k", tz=dateutil.tz.gettz(timezone)
    )

    el_locator = matplotlib.ticker.MultipleLocator(20)
    el_locator_min = matplotlib.ticker.MultipleLocator(10)
    az_locator = matplotlib.ticker.MultipleLocator(90)
    az_locator_min = matplotlib.ticker.MultipleLocator(45)
    return (
        date_formatter, 
        date_locator, 
        el_locator, 
        el_locator_min, 
        az_locator, 
        az_locator_min
    )


def create_figure_axes() -> Tuple[
    matplotlib.pyplot.Figure, 
    matplotlib.pyplot.Axes, 
    matplotlib.pyplot.Axes
]:
    fig = matplotlib.pyplot.figure(figsize=FIG_SIZE)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    return fig, ax1, ax2


def _calculate_and_plot_target(
    ax1: matplotlib.pyplot.Axes, 
    ax2: matplotlib.pyplot.Axes, 
    target_details: Dict[str, Any],
    astropy_localtime: astropy.time.Time,
    datetime_list_for_plot: List[Any],
    telescope_location: astropy.coordinates.EarthLocation
):
    alt: astropy.units.degree.Degree
    az: astropy.units.degree.Degree
    common_altaz_frame = astropy.coordinates.AltAz(
        obstime=astropy_localtime, location=telescope_location
    )

    if target_details.get("is_sun", False):
        sun_positions_at_obstime = target_details["coord"] 
        sun_altaz_coords = sun_positions_at_obstime.transform_to(
            astropy.coordinates.AltAz(location=telescope_location)
        )
        alt = sun_altaz_coords.alt
        az = sun_altaz_coords.az
    else:
        coord = target_details["coord"]
        coord_altaz = coord.transform_to(common_altaz_frame) 
        alt = coord_altaz.alt
        az = coord_altaz.az

    ax1.plot(
        datetime_list_for_plot,
        alt,
        target_details["style"],
        color=target_details["color"],
        label=target_details["label"],
    )

    visible_mask = alt > 0
    ax2.plot(
        [dt for i, dt in enumerate(datetime_list_for_plot) if visible_mask[i]],
        az[visible_mask],
        ".",
        mfc=target_details["color"],
        mec="none",
        ms=6,
    )


def _finalize_axes(
    fig: matplotlib.pyplot.Figure,
    ax1: matplotlib.pyplot.Axes, 
    ax2: matplotlib.pyplot.Axes, 
    datetime_list_for_plot: List[Any], 
    lst: astropy.time.Time,
    timezone: str, 
    date_formatter: matplotlib.dates.DateFormatter, 
    date_locator: matplotlib.dates.HourLocator, 
    el_locator: matplotlib.ticker.MultipleLocator, 
    el_locator_min: matplotlib.ticker.MultipleLocator, 
    az_locator: matplotlib.ticker.MultipleLocator, 
    az_locator_min: matplotlib.ticker.MultipleLocator,
    obs_date_str: str,
    telescope_name: str
):
    axes_list = [ax1, ax2]
    [a.xaxis.set_major_locator(date_locator) for a in axes_list]
    [a.xaxis.set_major_formatter(date_formatter) for a in axes_list]
    ax1.yaxis.set_major_locator(el_locator)
    ax1.yaxis.set_minor_locator(el_locator_min)
    ax2.yaxis.set_major_locator(az_locator)
    ax2.yaxis.set_minor_locator(az_locator_min)
    [a.grid(True, which="both", linestyle=":") for a in axes_list]
    ax1.set_ylabel("El (deg)")
    ax2.set_ylabel("Az (deg)")
    [a.set_xlabel(f"Local Time (hour, tz={timezone})") for a in axes_list]
    ax1.legend(loc="upper right")
    ax1.set_ylim(0, 90)
    ax2.set_ylim(0, 360)
    if datetime_list_for_plot is not None and len(datetime_list_for_plot) > 0:
        xlim_start = datetime_list_for_plot[0]
        xlim_end = datetime_list_for_plot[-1]
        for a in axes_list:
            a.set_xlim(xlim_start, xlim_end)

    if lst.value.size > 0:
        lst_val_0 = int(lst.value[0])
        lst_ticks = numpy.arange(lst_val_0, lst_val_0 + 25, 1)
        lst_ticklabels = lst_ticks.copy()
        lst_ticklabels[lst_ticklabels > 23] -= 24
        ax1lst = ax1.twiny()
        ax1lst.set_xticks(lst_ticks)
        ax1lst.set_xticklabels(lst_ticklabels)
        ax1lst.set_xlim(lst.value[0], lst.value[-1] + 24)
        # ax1lst.set_xlabel("LST")

    ax1.set_title(f"{obs_date_str} / {telescope_name}", y=1.1, fontsize=12)


def set_targets_with_error_handling(
    targets: List[Dict[str, Any]], 
    obs_time: astropy.time.Time
) -> Tuple[
    List[Dict[str, Any]], 
    List[Dict[str, str]]
]:
    processed_targets = []
    target_errors = []
    for i, target_info in enumerate(targets):
        try:
            target_name = target_info["label"]
            
            coord_for_plot: Any 
            is_sun = False
            if target_name.lower() == "sun":
                temp_sun_coord = astropy.coordinates.get_sun(obs_time)
                coord_for_plot = temp_sun_coord
                is_sun = True
            else:
                coord_obj = astropy.coordinates.SkyCoord.from_name(
                    target_name
                )
                coord_for_plot = coord_obj
            
            line_style = "-" if i % 2 == 0 else "--"
            processed_targets.append(
                {
                    "label": target_name,
                    "coord": coord_for_plot, 
                    "style": line_style, 
                    "color": target_info["color"],
                    "is_sun": is_sun
                }
            )
        except astropy.coordinates.name_resolve.NameResolveError as e:
            log_message = f"NameResolveError for '{target_info.get('label', 'N/A')}': {type(e).__name__} - {str(e)}"
            logger.error(log_message) # logging を使用
            print(f"DEBUG_PRINT: {log_message}") # 念のためprintも残す
            error_msg = f"Could not find coordinates for '{target_info.get('label', 'N/A')}'."
            target_errors.append({"name": target_info.get('label', 'N/A'), "error": error_msg})
        except Exception as e:
            log_message = f"Unexpected error for '{target_info.get('label', 'N/A')}': {type(e).__name__} - {str(e)}"
            logger.error(log_message) # logging を使用
            print(f"DEBUG_PRINT: {log_message}") # 念のためprintも残す
            error_msg = (
                f"Unexpected error for '{target_info.get('label', 'N/A')}': {type(e).__name__} - {str(e)}"
            )
            target_errors.append({"name": target_info.get('label', 'N/A'), "error": error_msg})
    return processed_targets, target_errors


def generate_azel_plot(
    obsdate: str, 
    timezone: str, 
    site: str, 
    targets_input: List[Dict]
) -> Dict[str, Any]:
    telescope, obsdate_processed = get_site(site, obsdate, timezone)
    # loc_raw は datetime の numpy 配列、loc_ap が astropy.time.Time オブジェクト
    loc_raw, loc_ap, lst_raw = get_localtime(obsdate_processed, telescope)

    # set_targets_with_error_handling には loc_ap (Timeオブジェクト) を渡す
    targets_proc, target_resolution_errors = set_targets_with_error_handling(
        targets_input, loc_ap
    )

    plot_stylers = setup_plot_style(timezone)
    fig, ax1, ax2 = create_figure_axes()

    dt_list_plot: List[Any] = []
    if loc_raw is not None and loc_raw.size > 0:
        dt_list_plot = loc_raw.tolist()
    
    for target_info in targets_proc:
        _calculate_and_plot_target(
            ax1, ax2, 
            target_info, 
            loc_ap,
            dt_list_plot, 
            telescope
        )

    _finalize_axes(
        fig, ax1, ax2, 
        dt_list_plot, 
        lst_raw, 
        timezone, 
        plot_stylers[0],  # date_formatter
        plot_stylers[1],  # date_locator
        plot_stylers[2],  # el_locator
        plot_stylers[3],  # el_locator_min
        plot_stylers[4],  # az_locator
        plot_stylers[5],  # az_locator_min
        obsdate,          # obs_date_str
        site              # telescope_name
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=PLOT_DPI, bbox_inches="tight")
    buf.seek(0)
    matplotlib.pyplot.close(fig)
    return {"image_data": buf, "errors": target_resolution_errors}
