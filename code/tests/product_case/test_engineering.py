"""B1, the engineering view: the network the product case sells on, read from the engineering
artifact, and every refusal of an artifact it cannot sell on.

The synthetic ``iridium-v7`` artifact of round numbers (the conftest's) carries the arithmetic
of method step 1 and each refusal; the committed artifact shows the reader takes the real file
and gives round 1's class split to the bit.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import math
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from product_case.constants import TERMINAL_CUSTOMERS_TODAY, VOICE_DATA_CUSTOMERS_TODAY
from product_case.engineering import (
    EngineeringArtifactError,
    EngineeringView,
    TerminalPool,
    class_split,
    engineering_view_from_bytes,
)

type Mutation = Callable[[dict[str, Any]], None]
"""A change made to the synthetic engineering artifact's mapping before it is read."""

COMMITTED_ARTIFACT = "communications/models/iridium/default.json"
"""The committed engineering artifact, repository-relative."""

COMMITTED_REPORTED_YEARS = (2031, 2033, 2035, 2036)
"""The shipped scenario's reported years."""

ROUND1_PEOPLE_PER_BEAM_SMALL = 320.0
"""Round 1's small terminal people a beam (the strategy's prototype at the engineering usage, the
product case's scratch exploration, local), against which the split is pinned to the bit."""

ROUND1_PEOPLE_PER_BEAM_MOUNTED = 40.0
"""Round 1's mounted terminal people a beam (as above)."""

PB3_CLASS_SPLIT = 0.757347400150716
"""The class split at full precision, as the plan's probe pB3 printed it (local)."""


def _year(artifact: dict[str, Any], year: int) -> dict[str, Any]:
    """The artifact's entry for one year."""
    return next(entry for entry in artifact["years"] if entry["year"] == year)


def _year_class(artifact: dict[str, Any], year: int, device_class: str) -> dict[str, Any]:
    """One device class's entry in one year."""
    return next(
        entry for entry in _year(artifact, year)["classes"] if entry["device_class"] == device_class
    )


def test_the_view_of_a_synthetic_artifact_follows_method_step_one(
    synthetic_engineering: dict[str, Any],
    synthetic_years: dict[int, dict[str, int | float]],
    synthetic_reported_years: tuple[int, ...],
    synthetic_stamp: str,
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
) -> None:
    """Objective: the view derives method step 1 from the engineering artifact alone: the class
    split from the two terminals' people a beam and today's mix, the unrounded seats, the
    network's scale over Iridium's 418,100 terminal customers today, each terminal's busy-hour
    data a month from its engineering usage, and L(t) and IoT's three rooms as read; and it
    records the bytes' SHA-256, the stamp and the schema.

    Sample: the synthetic artifact (the small terminal 200 people a beam, the mounted 25, so
    s = n_v / (8 - 7 n_v) with n_v = 402,000 / 418,100; FY2031 to FY2033 at 4, 8 and 12 million
    small-terminal people and 0.5, 1 and 1.5 million mounted), read for its three reported years.

    Expected outcome: s within 1e-15 of that closed form; S_small = s x P_small and
    S_mounted = (1 - s) x P_mounted exactly; k = (S_small + S_mounted) / 418,100 exactly; 2.7 and
    27.0 GB of busy-hour data a month; L, R, A, T, the fleet and its cost as written; 340-byte
    messages, 100,000-byte bursts, a 7 s airtime; the SHA-256 of the bytes read.
    """
    data = as_engineering_bytes(synthetic_engineering)
    view = engineering_view_from_bytes(
        data, path="synthetic/iridium.json", reported_years=synthetic_reported_years
    )
    personal = VOICE_DATA_CUSTOMERS_TODAY / TERMINAL_CUSTOMERS_TODAY
    s = view.small_terminal_share
    assert math.isclose(s, personal / (8 - 7 * personal), rel_tol=1e-15)
    assert view.path == "synthetic/iridium.json"
    assert view.sha256 == hashlib.sha256(data).hexdigest()
    assert (view.schema_version, view.version_stamp) == ("iridium-v7", synthetic_stamp)
    assert view.coverage_floor_reached_year == 2031
    assert view.busy_hour_gb_per_month_small == 2.7
    assert view.busy_hour_gb_per_month_mounted == 27.0
    assert (view.message_bytes, view.burst_bytes, view.airtime_high_s) == (340, 100_000, 7.0)
    assert view.small_terminal_pool == TerminalPool(10.0, 2.0, 0.025)
    assert view.mounted_terminal_pool == TerminalPool(12.5, 5.0, 0.1)
    assert [year.year for year in view.years] == list(synthetic_reported_years)
    for year in view.years:
        row = synthetic_years[year.year]
        assert year.seats_small_terminal == s * row["small"]
        assert year.seats_mounted_terminal == (1.0 - s) * row["mounted"]
        assert year.network_scale == (
            (year.seats_small_terminal + year.seats_mounted_terminal) / TERMINAL_CUSTOMERS_TODAY
        )
        assert (year.people_small_terminal, year.people_mounted_terminal) == (
            row["small"],
            row["mounted"],
        )
        assert (year.living_fleet, year.annual_cost_musd) == (
            row["living_fleet"],
            row["annual_cost_musd"],
        )
        assert year.phone_useful_beams == row["phone_beams"]
        assert (
            year.iot_payload_bits_per_second,
            year.iot_access_attempts_per_second,
            year.iot_single_tone_seconds_per_second,
        ) == (row["payload"], row["access"], row["tone"])


def _set_year_value(year: int, keys: tuple[str, ...], value: object) -> Mutation:
    """A mutation that sets one value inside one year's entry."""

    def mutate(artifact: dict[str, Any]) -> None:
        node: dict[str, Any] = _year(artifact, year)
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = value

    return mutate


def _drop_year_value(year: int, keys: tuple[str, ...]) -> Mutation:
    """A mutation that removes one key inside one year's entry."""

    def mutate(artifact: dict[str, Any]) -> None:
        node: dict[str, Any] = _year(artifact, year)
        for key in keys[:-1]:
            node = node[key]
        del node[keys[-1]]

    return mutate


def _schema(version: str) -> Mutation:
    """A mutation that states another schema."""

    def mutate(artifact: dict[str, Any]) -> None:
        artifact["provenance"]["schema_version"] = version

    return mutate


def _null_floor(artifact: dict[str, Any]) -> None:
    """A fleet that never reaches the coverage floor."""
    artifact["trajectory_summary"]["coverage_floor_reached_year"] = None


def _no_provenance(artifact: dict[str, Any]) -> None:
    """An artifact without its provenance."""
    del artifact["provenance"]


def _d_equals_one(artifact: dict[str, Any]) -> None:
    """FY2032 at a downlink share of 1: the uplink has no time, so no payload and no tone room."""
    iot = _year(artifact, 2032)["iot"]
    iot["uplink_payload_bits_per_second"] = 0.0
    iot["single_tone_seconds_per_second"] = 0.0


def _no_people(artifact: dict[str, Any]) -> None:
    """FY2032 with no small-terminal people."""
    _year_class(artifact, 2032, "small_terminal_class")["people_served"] = 0


def _no_mounted_pool(artifact: dict[str, Any]) -> None:
    """An artifact whose classes lack the mounted terminal."""
    artifact["classes"] = [
        entry for entry in artifact["classes"] if entry["device_class"] != "mounted_terminal_class"
    ]


def _zero_pool(artifact: dict[str, Any]) -> None:
    """A small terminal whose rate while active is 0 (its people a beam would divide by 0)."""
    artifact["classes"][0]["active_user_rate_mbps"] = 0.0


def _zero_message(artifact: dict[str, Any]) -> None:
    """A message of 0 bytes (an IoT device's service would divide by 0)."""
    artifact["iridium_physics"]["iot_message_bytes"] = 0


def _zero_phone_beams(artifact: dict[str, Any]) -> None:
    """FY2031 with no phone-class beams under its rooms (attempts a beam would divide by 0)."""
    _year_class(artifact, 2031, "phone_class")["useful_beams"] = 0.0


def _no_phone_beams(artifact: dict[str, Any]) -> None:
    """FY2033 without the phone class's entry, whose useful beams IoT rides."""
    year = _year(artifact, 2033)
    year["classes"] = [entry for entry in year["classes"] if entry["device_class"] != "phone_class"]


def _zero_access_room(artifact: dict[str, Any]) -> None:
    """FY2033 with no random-access room (the room is 57 attempts a second on each useful beam)."""
    _year(artifact, 2033)["iot"]["access_attempts_per_second_low"] = 0.0


def _zero_tone_room(artifact: dict[str, Any]) -> None:
    """FY2032 with no single-tone room alone (its payload room still published)."""
    _year(artifact, 2032)["iot"]["single_tone_seconds_per_second"] = 0.0


def _set_pool(index: int, **values: float) -> Mutation:
    """A mutation that sets values of one ``classes[]`` entry (0 the small terminal, 1 mounted)."""

    def mutate(artifact: dict[str, Any]) -> None:
        artifact["classes"][index].update(values)

    return mutate


def _people_beyond_a_double(artifact: dict[str, Any]) -> None:
    """FY2032 with more small-terminal people than a double holds (10^400)."""
    _year_class(artifact, 2032, "small_terminal_class")["people_served"] = 10**400


REFUSALS: list[tuple[str, Mutation, tuple[int, ...], tuple[str, ...]]] = [
    (
        "iridium-v6",
        _schema("iridium-v6"),
        (2031, 2032, 2033),
        ("provenance.schema_version is 'iridium-v6'", "reads only 'iridium-v7'"),
    ),
    (
        "no provenance",
        _no_provenance,
        (2031, 2032, 2033),
        ("needs schema iridium-v7", "provenance: Field required"),
    ),
    (
        "a room missing",
        _drop_year_value(2032, ("iot", "single_tone_seconds_per_second")),
        (2031, 2032, 2033),
        ("years.2.iot.single_tone_seconds_per_second: Field required",),
    ),
    (
        "a boolean fleet",
        _set_year_value(2031, ("living_fleet",), True),
        (2031, 2032, 2033),
        ("years.1.living_fleet", "valid integer"),
    ),
    (
        "a room that is not a number",
        _set_year_value(2031, ("iot", "uplink_payload_bits_per_second"), math.nan),
        (2031, 2032, 2033),
        ("years.1.iot.uplink_payload_bits_per_second", "finite number"),
    ),
    (
        "a null coverage floor year",
        _null_floor,
        (2031, 2032, 2033),
        ("trajectory_summary.coverage_floor_reached_year is null",),
    ),
    (
        "a reported year absent",
        lambda artifact: None,
        (2031, 2032, 2034),
        (
            "FY2034 is a reported year but not a year of the engineering artifact",
            "its years run FY2030 to FY2033",
        ),
    ),
    (
        "a reported year before the floor",
        lambda artifact: None,
        (2030, 2031, 2032),
        ("FY2030 is before the coverage floor year FY2031", "no seats"),
    ),
    (
        "a zero room at d = 1",
        _d_equals_one,
        (2031, 2032, 2033),
        (
            "FY2032: IoT's room is zero",
            "years[].iot.uplink_payload_bits_per_second is 0.0",
            "a downlink share of 1 leaves the uplink no time",
        ),
    ),
    (
        "no people for a terminal",
        _no_people,
        (2031, 2032, 2033),
        ("FY2032: small_terminal_class has no people", "no seats"),
    ),
    (
        "a terminal's pool absent",
        _no_mounted_pool,
        (2031, 2032, 2033),
        ("classes[] has no mounted_terminal_class entry",),
    ),
    (
        "a pool's rate of zero",
        _zero_pool,
        (2031, 2032, 2033),
        ("classes[].active_user_rate_mbps of small_terminal_class is 0.0", "above 0"),
    ),
    (
        "a message of zero bytes",
        _zero_message,
        (2031, 2032, 2033),
        ("iridium_physics.iot_message_bytes is 0", "above 0"),
    ),
    (
        "no phone-class beams under a room",
        _zero_phone_beams,
        (2031, 2032, 2033),
        (
            "FY2031: IoT's room is zero",
            "useful_beams of phone_class is 0.0",
            "the phone class has no useful beams for IoT to ride",
        ),
    ),
    (
        "a zero access room",
        _zero_access_room,
        (2031, 2032, 2033),
        (
            "FY2033: IoT's room is zero",
            "years[].iot.access_attempts_per_second_low is 0.0",
            "the phone class has no useful beams for IoT to ride",
        ),
    ),
    (
        "a zero tone room",
        _zero_tone_room,
        (2031, 2032, 2033),
        (
            "FY2032: IoT's room is zero",
            "years[].iot.single_tone_seconds_per_second is 0.0",
            "a downlink share of 1 leaves the uplink no time",
        ),
    ),
    (
        "a pool whose split leaves the doubles",
        _set_pool(0, beam_pool_mbps=1e-300, active_user_rate_mbps=1e10, concurrency_peak=1e10),
        (2031, 2032, 2033),
        (
            "the class split s is nan",
            "beam_pool_mbps, active_user_rate_mbps and concurrency_peak of small_terminal_class "
            "and mounted_terminal_class",
        ),
    ),
    (
        "a pool whose people a beam underflows to 0",
        _set_pool(0, beam_pool_mbps=1e-300, active_user_rate_mbps=1e100, concurrency_peak=1e100),
        (2031, 2032, 2033),
        (
            "small_terminal_class's people a beam is 0.0",
            "its classes[].beam_pool_mbps, active_user_rate_mbps and concurrency_peak",
        ),
    ),
    (
        "a rate whose busy-hour data leaves the doubles",
        _set_pool(1, active_user_rate_mbps=1e300),
        (2031, 2032, 2033),
        (
            "mounted_terminal_class's busy-hour data a month is inf",
            "its classes[].active_user_rate_mbps and concurrency_peak",
        ),
    ),
    (
        "people beyond a double",
        _people_beyond_a_double,
        (2031, 2032, 2033),
        (
            "FY2032: years[].classes[].people_served of small_terminal_class is beyond the range "
            "of a double",
        ),
    ),
    (
        "the phone class's beams absent",
        _no_phone_beams,
        (2031, 2032, 2033),
        ("FY2033: years[].classes[] has no phone_class entry",),
    ),
]
"""Each refusal: what it is, the change to the synthetic artifact, the reported years asked for
and the phrases its one-line message must hold."""


@pytest.mark.parametrize(
    ("mutation", "reported_years", "phrases"),
    [pytest.param(m, y, p, id=name) for name, m, y, p in REFUSALS],
)
def test_every_refusal_of_an_engineering_artifact_names_the_field_or_the_year(
    synthetic_engineering: dict[str, Any],
    as_engineering_bytes: Callable[[dict[str, Any]], bytes],
    mutation: Mutation,
    reported_years: tuple[int, ...],
    phrases: tuple[str, ...],
) -> None:
    """Objective: the view refuses an engineering artifact the product case cannot sell on, in
    one line naming the artifact and the field or the year: another schema (naming
    ``iridium-v7``); a field it reads missing, of the wrong type or not finite; a null coverage
    floor year; a reported year absent from the artifact or before its floor year; a reported
    year whose payload or tone room is zero (d = 1) or whose access room or phone-class beams
    are zero (no useful beams), each with its own cause; a terminal class with no people in a
    reported year; a pool, a size or the airtime not above 0; a value derived from the pools
    (people a beam, busy-hour data, the class split) that leaves the finite numbers above 0;
    people beyond a double; a class the reader needs absent.

    Sample: the synthetic artifact with one change, read for the reported years shown.

    Expected outcome: an ``EngineeringArtifactError`` whose message names the artifact's path
    and holds each phrase.
    """
    mutation(synthetic_engineering)
    with pytest.raises(EngineeringArtifactError) as caught:
        engineering_view_from_bytes(
            as_engineering_bytes(synthetic_engineering),
            path="synthetic/iridium.json",
            reported_years=reported_years,
        )
    message = str(caught.value)
    assert message.startswith("synthetic/iridium.json: "), message
    assert "\n" not in message, message
    for phrase in phrases:
        assert phrase in message, message


def test_bytes_that_are_not_json_are_refused() -> None:
    """Objective: bytes that are not JSON are refused in one line naming the artifact.

    Sample: a truncated JSON object.

    Expected outcome: an ``EngineeringArtifactError`` saying the file is not JSON.
    """
    with pytest.raises(EngineeringArtifactError, match=r"^synthetic/iridium\.json: not JSON \("):
        engineering_view_from_bytes(
            b'{"provenance": {', path="synthetic/iridium.json", reported_years=(2031, 2032)
        )


def test_the_committed_artifact_reads_to_round_one_class_split_to_the_bit(
    repo_dir: Path,
) -> None:
    """Objective: the narrow reader takes the committed engineering artifact whole (every field
    it does not read ignored), and the class split it derives from the artifact's beam pools
    equals round 1's from its 320 and 40 people a beam to the bit (the plan's probe pB3); each
    reported year's seats, network scale, L(t) and rooms follow from the artifact's own
    published values, so nothing here moves with a re-promotion that keeps the engineering
    usage.

    Sample: ``communications/models/iridium/default.json`` as committed, read for FY2031,
    FY2033, FY2035 and FY2036.

    Expected outcome: s equals round 1's split and pB3's printed 0.757347400150716 exactly; the
    busy-hour data 2.7 and 27.0 GB a month; each year's seats and scale by their formulas from
    the artifact's people; L, R, A and T equal to the artifact's published phone beams and rooms;
    the schema ``iridium-v7`` and the SHA-256 of the file's bytes.
    """
    path = repo_dir / COMMITTED_ARTIFACT
    data = path.read_bytes()
    view = engineering_view_from_bytes(
        data, path=COMMITTED_ARTIFACT, reported_years=COMMITTED_REPORTED_YEARS
    )
    round1 = class_split(
        TerminalPool(ROUND1_PEOPLE_PER_BEAM_SMALL, 1.0, 1.0),
        TerminalPool(ROUND1_PEOPLE_PER_BEAM_MOUNTED, 1.0, 1.0),
    )
    assert view.small_terminal_share == round1 == PB3_CLASS_SPLIT
    assert view.schema_version == "iridium-v7"
    assert view.sha256 == hashlib.sha256(data).hexdigest()
    assert view.busy_hour_gb_per_month_small == 2.7
    assert view.busy_hour_gb_per_month_mounted == 27.0
    published = json.loads(data)
    s = view.small_terminal_share
    for year in view.years:
        small = _year_class(published, year.year, "small_terminal_class")["people_served"]
        mounted = _year_class(published, year.year, "mounted_terminal_class")["people_served"]
        assert year.seats_small_terminal == s * small
        assert year.seats_mounted_terminal == (1.0 - s) * mounted
        assert year.network_scale == (
            (year.seats_small_terminal + year.seats_mounted_terminal) / TERMINAL_CUSTOMERS_TODAY
        )
        phone = _year_class(published, year.year, "phone_class")
        iot = _year(published, year.year)["iot"]
        assert year.phone_useful_beams == phone["useful_beams"]
        assert year.iot_payload_bits_per_second == iot["uplink_payload_bits_per_second"]
        assert year.iot_access_attempts_per_second == iot["access_attempts_per_second_low"]
        assert year.iot_single_tone_seconds_per_second == iot["single_tone_seconds_per_second"]


def test_a_view_built_directly_holds_the_split_and_busy_data_its_pools_give() -> None:
    """Objective: a view built from plain numbers (as the reproduction of round 3 builds one
    from pinned floats) must hold the class split and the busy-hour data its pools give, checked
    at its construction within the invariants' tolerance (the spec lens's m6), so the pool cells
    the artifact publishes cannot contradict s; round 3's pinned split passes.

    Sample: round 3's split at full precision (0.757347400150716, the plan's probe pB3) with 2.7
    and 27 GB of busy-hour data, once with the committed artifact's pools (10.72 Mbps a beam at 2
    Mbps and 2.5 percent busy; 13.4 at 5 Mbps and 10 percent) and once with round 1's (16 and 20
    Mbps a beam at the same usage, 320 and 40 people a beam); then that view with the split 0.75,
    and with the small terminal's busy-hour data 2.8 GB.

    Expected outcome: both pinned views build; the two changed ones raise
    ``EngineeringArtifactError`` naming the field, its value and the value the pools give.
    """
    pools = {
        "committed": (TerminalPool(10.72, 2.0, 0.025), TerminalPool(13.4, 5.0, 0.1)),
        "round 1": (TerminalPool(16.0, 2.0, 0.025), TerminalPool(20.0, 5.0, 0.1)),
    }
    views = [
        EngineeringView(
            path="round3/pinned",
            sha256="0" * 64,
            schema_version="iridium-v7",
            version_stamp="2026-10-06",
            coverage_floor_reached_year=2031,
            small_terminal_pool=small,
            mounted_terminal_pool=mounted,
            small_terminal_share=PB3_CLASS_SPLIT,
            busy_hour_gb_per_month_small=2.7,
            busy_hour_gb_per_month_mounted=27.0,
            message_bytes=340,
            burst_bytes=100_000,
            airtime_high_s=7.0,
            years=(),
        )
        for small, mounted in pools.values()
    ]
    assert [view.small_terminal_share for view in views] == [PB3_CLASS_SPLIT] * len(pools)
    with pytest.raises(EngineeringArtifactError, match=r"small_terminal_share is 0\.75, but"):
        dataclasses.replace(views[0], small_terminal_share=0.75)
    with pytest.raises(
        EngineeringArtifactError, match=r"busy_hour_gb_per_month_small is 2\.8, but its pools"
    ):
        dataclasses.replace(views[1], busy_hour_gb_per_month_small=2.8)
