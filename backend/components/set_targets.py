import astropy.coordinates
import astropy.coordinates as coord


def set_targets(target_list, localtime_ap):
    targets = []
    for t in target_list:
        try:
            sky_coord = coord.get_body(t["label"], time=localtime_ap)
        except KeyError:
            sky_coord = coord.SkyCoord.from_name(t["label"])
        targets.append({
            "label": t["label"],
            "color": t["color"],
            "style": "-",
            "coord": sky_coord
            })
    return targets