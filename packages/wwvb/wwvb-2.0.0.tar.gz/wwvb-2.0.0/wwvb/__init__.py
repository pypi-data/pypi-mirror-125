#!/usr/bin/python3
"""A library for WWVB timecodes"""

# Copyright (C) 2011-2020 Jeff Epler <jepler@gmail.com>
# SPDX-FileCopyrightText: 2021 Jeff Epler
#
# SPDX-License-Identifier: GPL-3.0-only

import collections
import datetime
import enum
import warnings
from typing import Generator, List, Optional, TextIO, Tuple, TypeVar, Union
import io
from dateutil.tz import gettz
from . import iersdata

HOUR = datetime.timedelta(seconds=3600)
DateOrDatetime = TypeVar("DateOrDatetime", datetime.date, datetime.datetime)
T = TypeVar("T")  # pylint: disable=invalid-name


def require(x: Optional[T]) -> T:
    """Assert that an Optional value is not None, and then return the value,
    giving a hint to the type system."""
    assert x is not None
    return x


Mountain = require(gettz("America/Denver"))


def _date(dt: DateOrDatetime) -> datetime.date:
    """Return the date object itself, or the date property of a datetime"""
    if isinstance(dt, datetime.datetime):
        return dt.date()
    return dt


def maybe_warn_update(dt: datetime.date) -> None:
    """Maybe print a notice to run updateiers, if it seems useful to do so."""
    # We already know this date is not covered.
    # If the date is less than 330 days after today, there should be (possibly)
    # prospective available now.
    today = datetime.date.today()
    if dt < today + datetime.timedelta(days=330):
        warnings.warn(
            "Note: Running `updateiers` may provide better DUT1 and LS information"
        )


def get_dut1(dt: DateOrDatetime) -> float:
    """Return the DUT1 number for the given timestamp"""
    date = _date(dt)
    i = (date - iersdata.DUT1_DATA_START).days
    if i < 0:
        v = iersdata.DUT1_OFFSETS[0]
    elif i >= len(iersdata.DUT1_OFFSETS):
        maybe_warn_update(dt)
        v = iersdata.DUT1_OFFSETS[-1]
    else:
        v = iersdata.DUT1_OFFSETS[i]
    return (ord(v) - ord("k")) / 10.0


def isly(year: int) -> bool:
    """Return True if the year is a leap year"""
    d1 = datetime.date(year, 1, 1)
    d2 = d1 + datetime.timedelta(days=365)
    return d1.year == d2.year


def isls(t: DateOrDatetime) -> bool:
    """Return True if a leap second occurs at the end of this month"""
    dut1_today = get_dut1(t)
    month_today = t.month
    while t.month == month_today:
        t += datetime.timedelta(1)
    dut1_next_month = get_dut1(t)
    return dut1_today * dut1_next_month < 0


def isdst(t: datetime.date, tz: datetime.tzinfo = Mountain) -> bool:
    """Return true if daylight saving time is active at the given moment"""
    t = datetime.datetime(t.year, t.month, t.day)
    return bool(t.astimezone(tz).dst())


def first_sunday_on_or_after(dt: DateOrDatetime) -> DateOrDatetime:
    """Return the first sunday on or after the reference time"""
    days_to_go = 6 - dt.weekday()
    if days_to_go:
        return dt + datetime.timedelta(days_to_go)
    return dt


def first_sunday_in_month(y: int, m: int) -> datetime.date:
    """Find the first sunday in a given month"""
    return first_sunday_on_or_after(datetime.datetime(y, m, 1))


def is_dst_change_day(t: datetime.date) -> bool:
    """Return True if the day is a DST change day"""
    return isdst(t) != isdst(t + datetime.timedelta(1))


def get_dst_change_hour(
    t: DateOrDatetime, tz: datetime.tzinfo = Mountain
) -> Optional[int]:
    """Return the hour when DST changes"""
    lt0 = datetime.datetime(t.year, t.month, t.day, hour=0, tzinfo=tz)
    dst0 = lt0.dst()
    for i in (1, 2, 3, 4):
        lt1 = (lt0.astimezone(datetime.timezone.utc) + HOUR * i).astimezone(tz)
        dst1 = lt1.dst()
        if dst0 != dst1:
            return i - 1
    return None


def get_dst_change_date_and_row(
    d: DateOrDatetime,
) -> Tuple[Optional[datetime.date], Optional[int]]:
    """Classify DST information for the WWVB phase modulation signal"""
    if isdst(d):
        n = first_sunday_in_month(d.year, 11)
        for offset in range(-28, 28, 7):  # pragma no branch
            d1 = n + datetime.timedelta(days=offset)
            if is_dst_change_day(d1):
                return d1, (offset + 28) // 7
    else:
        m = first_sunday_in_month(d.year + (d.month > 3), 3)
        for offset in range(0, 52, 7):
            d1 = m + datetime.timedelta(days=offset)
            if is_dst_change_day(d1):
                return d1, offset // 7

    return None, None


# "Table 8", likely with transcrption errors
dsttable = [
    [
        [
            0b110001,
            0b100110,
            0b100101,
            0b010101,
            0b111110,
            0b010110,
            0b110111,
            0b111101,
        ],
        [
            0b101010,
            0b011011,
            0b001110,
            0b000001,
            0b000010,
            0b001000,
            0b001101,
            0b101001,
        ],
        [
            0b000100,
            0b100000,
            0b110100,
            0b101100,
            0b111000,
            0b010000,
            0b110010,
            0b011100,
        ],
    ],
    [
        [
            0b110111,
            0b010101,
            0b110001,
            0b010110,
            0b100110,
            0b111110,
            0b100101,
            0b111101,
        ],
        [
            0b001101,
            0b000001,
            0b101010,
            0b001000,
            0b011011,
            0b000010,
            0b001110,
            0b101001,
        ],
        [
            0b110010,
            0b101100,
            0b000100,
            0b010000,
            0b100000,
            0b111000,
            0b110100,
            0b011100,
        ],
    ],
]


def lfsr_gen(x: List[int]) -> None:
    """Generate the 127-bit sequence used in the extended 6-minute codes
    except generate 255 bits so that we can simply use any range of [x:x+127]
    bits"""
    x.append(x[-7] ^ x[-6] ^ x[-5] ^ x[-2])


lfsr_seq = [1] * 7
while len(lfsr_seq) < 255:
    lfsr_gen(lfsr_seq)

# Table 12 - Fixed 106-bit timing word
ftw = [
    int(c)
    for c in "1101000111"
    "0101100101"
    "1001101110"
    "0011000010"
    "1101001110"
    "1001010100"
    "0010111000"
    "1011010110"
    "1101111111"
    "1000000100"
    "100100"
]


def get_dst_next(d: DateOrDatetime, tz: datetime.tzinfo = Mountain) -> int:
    """Find the "dst next" value for the phase modulation signal"""
    dst_now = isdst(d)  # dst_on[1]
    dst_midwinter = isdst(datetime.datetime(d.year, 1, 1))
    dst_midsummer = isdst(datetime.datetime(d.year, 7, 1))

    if dst_midwinter and dst_midsummer:  # pragma no coverage
        return 0b101111
    if not (dst_midwinter or dst_midsummer):
        return 0b000111

    # Are we in NZ or something?
    if dst_midwinter or not dst_midsummer:  # pragma no coverage
        return 0b100011

    dst_change_date, dst_next_row = get_dst_change_date_and_row(d)
    if dst_change_date is None or dst_next_row is None:  # pragma no coverage
        return 0b100011

    dst_change_hour = get_dst_change_hour(dst_change_date, tz)
    if dst_change_hour is None:  # pragma no coverage
        return 0b100011

    return dsttable[dst_now][dst_change_hour][dst_next_row]


hamming_weight = [
    [23, 21, 20, 17, 16, 15, 14, 13, 9, 8, 6, 5, 4, 2, 0],
    [24, 22, 21, 18, 17, 16, 15, 14, 10, 9, 7, 6, 5, 3, 1],
    [25, 23, 22, 19, 18, 17, 16, 15, 11, 10, 8, 7, 6, 4, 2],
    [24, 21, 19, 18, 15, 14, 13, 12, 11, 7, 6, 4, 3, 2, 0],
    [25, 22, 20, 19, 16, 15, 14, 13, 12, 8, 7, 5, 4, 3, 1],
]

# Identifies the phase data as a time signal (SYNC_T bits present)
# or a message signal (SYNC_M bits present); No message signals are defined
# by NIST at this time.
SYNC_T = 0x768
SYNC_M = 0x1A3A


def extract_bit(v: int, p: int) -> bool:
    """Extract bit 'p' from integer 'v' as a bool"""
    return bool((v >> p) & 1)


def hamming_parity(value: int) -> int:
    """Compute the "hamming parity" of a 26-bit number, such as the minute-of-century [See Enhanced WWVB Broadcast Format 4.3]"""
    parity = 0
    for i in range(4, -1, -1):
        bit = 0
        for j in range(0, 15):
            bit ^= extract_bit(value, hamming_weight[i][j])
        parity = (parity << 1) | bit
    return parity


dst_ls_lut = [
    0b01000,
    0b10101,
    0b10110,
    0b00011,
    0b01000,
    0b10101,
    0b10110,
    0b00011,
    0b00100,
    0b01110,
    0b10000,
    0b01101,
    0b11001,
    0b11100,
    0b11010,
    0b11111,
]

_WWVBMinute = collections.namedtuple("_WWVBMinute", "year days hour min dst ut1 ls ly")


class WWVBMinute(_WWVBMinute):
    """Uniquely identifies a minute of time in the WWVB system. To use ut1 and ls information from IERS, create a WWVBMinuteIERS value instead."""

    year: int
    hour: int
    minute: int
    dst: int
    ut1: int
    ly: bool
    ls: bool

    def __new__(  # pylint: disable=too-many-arguments
        cls,
        year: int,
        days: int,
        hour: int,
        minute: int,
        dst: Optional[int] = None,
        ut1: Optional[int] = None,
        ls: Optional[bool] = None,
        ly: Optional[bool] = None,
    ) -> "WWVBMinute":
        """Construct a WWVBMinute"""
        if dst is None:
            dst = cls.get_dst(year, days)
        if dst not in (0, 1, 2, 3):
            raise ValueError("dst value should be 0..3")
        if ut1 is None and ls is None:
            ut1, ls = cls.get_dut1_info(year, days)
        elif ut1 is None or ls is None:
            raise ValueError("sepecify both ut1 and ls or neither one")
        if year < 70:
            year = year + 2000
        elif year < 100:
            year = year + 1900
        if ly is None:
            ly = isly(year)
        return _WWVBMinute.__new__(cls, year, days, hour, minute, dst, ut1, ls, ly)

    @staticmethod
    def get_dst(year: int, days: int) -> int:
        """Get the 2-bit WWVB DST value for the given day"""
        d0 = datetime.datetime(year, 1, 1) + datetime.timedelta(days - 1)
        d1 = d0 + datetime.timedelta(1)
        dst0 = isdst(d0)
        dst1 = isdst(d1)
        return dst1 * 2 + dst0

    def __str__(self) -> str:
        """Implement str()"""
        return f"year={self.year:4d} days={self.days:03d} hour={self.hour:02d} min={self.min:02d} dst={self.dst} ut1={self.ut1} ly={int(self.ly)} ls={int(self.ls)}"

    def as_datetime_utc(self) -> datetime.datetime:
        """Convert to a UTC datetime"""
        d = datetime.datetime(self.year, 1, 1, tzinfo=datetime.timezone.utc)
        d += datetime.timedelta(self.days - 1, self.hour * 3600 + self.min * 60)
        return d

    as_datetime = as_datetime_utc

    def as_datetime_local(
        self, standard_time_offset: int = 7 * 3600, dst_observed: bool = True
    ) -> datetime.datetime:
        """Convert to a local datetime according to the DST bits"""
        u = self.as_datetime_utc()
        d = u - datetime.timedelta(seconds=standard_time_offset)
        if not dst_observed:
            dst = False
        elif self.dst == 0b10:
            transition_time = u.replace(hour=2)
            dst = d >= transition_time
        elif self.dst == 0b11:
            dst = True
        elif self.dst == 0b01:
            transition_time = u.replace(hour=1)
            dst = d < transition_time
        else:  # self.dst == 0b00
            dst = False
        if dst:
            d += datetime.timedelta(seconds=3600)
        return d

    def is_ly(self) -> bool:
        """Return True if minute is during a leap year"""
        warnings.warn("Deprecated, use ly property instead", DeprecationWarning)
        return self.ly

    def is_end_of_month(self) -> bool:
        """Return True if minute is the last minute in a month"""
        d = self.as_datetime()
        e = d + datetime.timedelta(1)
        return d.month != e.month

    def minute_length(self) -> int:
        """Return the length of the minute, 60, 61, or (theoretically) 59 seconds"""
        if not self.ls:
            return 60
        if not self.is_end_of_month():
            return 60
        if self.hour != 23 or self.min != 59:
            return 60
        if self.ut1 > 0:
            return 59
        return 61

    def as_timecode(self) -> "WWVBTimecode":
        """Fill a WWVBTimecode structure representing this minute.  Fills both the amplitude and phase codes."""
        t = WWVBTimecode(self.minute_length())

        self.fill_am_timecode(t)
        self.fill_pm_timecode(t)

        return t

    @property
    def leap_sec(self) -> int:
        """Return the 2-bit leap_sec value used by the PM code"""
        if not self.ls:
            return 0
        if self.ut1 < 0:
            return 3
        return 2

    @property
    def minute_of_century(self) -> int:
        """Return the minute of the century"""
        century = (self.year // 100) * 100
        # note: This relies on timedelta seconds never including leapseconds!
        return (
            int(
                (
                    self.as_datetime()
                    - datetime.datetime(century, 1, 1, tzinfo=datetime.timezone.utc)
                ).total_seconds()
            )
            // 60
        )

    def fill_am_timecode(self, t: "WWVBTimecode") -> None:
        """Fill the amplitude (AM) portion of a timecode object"""
        for i in [0, 9, 19, 29, 39, 49]:
            t.am[i] = AmplitudeModulation.MARK
        if len(t.am) > 59:
            t.am[59] = AmplitudeModulation.MARK
        if len(t.am) > 60:
            t.am[60] = AmplitudeModulation.MARK
        for i in [4, 10, 11, 14, 20, 21, 24, 34, 35, 44, 54]:
            t.am[i] = AmplitudeModulation.ZERO
        t.put_am_bcd(self.min, 1, 2, 3, 5, 6, 7, 8)
        t.put_am_bcd(self.hour, 12, 13, 15, 16, 17, 18)
        t.put_am_bcd(self.days, 22, 23, 25, 26, 27, 28, 30, 31, 32, 33)
        ut1_sign = self.ut1 >= 0
        t.am[36] = t.am[38] = AmplitudeModulation(ut1_sign)
        t.am[37] = AmplitudeModulation(not ut1_sign)
        t.put_am_bcd(abs(self.ut1) // 100, 40, 41, 42, 43)
        t.put_am_bcd(self.year, 45, 46, 47, 48, 50, 51, 52, 53)
        t.am[55] = AmplitudeModulation(self.ly)
        t.am[56] = AmplitudeModulation(self.ls)
        t.put_am_bcd(self.dst, 57, 58)

    def fill_pm_timecode_extended(self, t: "WWVBTimecode") -> None:
        """During minutes 10..15 and 40..45, the amplitude signal holds 'extended information'"""
        assert 10 <= self.min < 16 or 40 <= self.min < 46
        minno = self.min % 10
        assert minno < 6

        dst = self.dst
        # Note that these are 1 different than Table 11
        # because our LFSR sequence is zero-based
        seqno = (self.min // 30) * 2
        if dst == 0:
            pass
        elif dst == 3:
            seqno = seqno + 1
        elif dst == 2:
            if self.hour < 4:
                pass
            elif self.hour < 11:
                seqno = seqno + 90
            else:
                seqno = seqno + 1
        else:  # dst == 1
            if self.hour < 4:
                seqno = seqno + 1
            elif self.hour < 11:
                seqno = seqno + 91

        info_seq = lfsr_seq[seqno : seqno + 127]
        full_seq = info_seq + ftw + info_seq[::-1]
        assert len(full_seq) == 360

        offset = minno * 60
        for i in range(60):
            t.put_pm_bit(i, full_seq[i + offset])

    def fill_pm_timecode_regular(  # pylint: disable=too-many-statements
        self, t: "WWVBTimecode"
    ) -> None:
        """Except during minutes 10..15 and 40..45, the amplitude signal holds 'regular information'"""
        t.put_pm_bin(0, 13, SYNC_T)

        moc = self.minute_of_century
        leap_sec = self.leap_sec
        dst_on = self.dst
        dst_ls = dst_ls_lut[dst_on | (leap_sec << 2)]
        dst_next = get_dst_next(self.as_datetime())
        t.put_pm_bin(13, 5, hamming_parity(moc))
        t.put_pm_bit(18, extract_bit(moc, 25))
        t.put_pm_bit(19, extract_bit(moc, 0))
        t.put_pm_bit(20, extract_bit(moc, 24))
        t.put_pm_bit(21, extract_bit(moc, 23))
        t.put_pm_bit(22, extract_bit(moc, 22))
        t.put_pm_bit(23, extract_bit(moc, 21))
        t.put_pm_bit(24, extract_bit(moc, 20))
        t.put_pm_bit(25, extract_bit(moc, 19))
        t.put_pm_bit(26, extract_bit(moc, 18))
        t.put_pm_bit(27, extract_bit(moc, 17))
        t.put_pm_bit(28, extract_bit(moc, 16))
        t.put_pm_bit(29, False)  # Reserved
        t.put_pm_bit(30, extract_bit(moc, 15))
        t.put_pm_bit(31, extract_bit(moc, 14))
        t.put_pm_bit(32, extract_bit(moc, 13))
        t.put_pm_bit(33, extract_bit(moc, 12))
        t.put_pm_bit(34, extract_bit(moc, 11))
        t.put_pm_bit(35, extract_bit(moc, 10))
        t.put_pm_bit(36, extract_bit(moc, 9))
        t.put_pm_bit(37, extract_bit(moc, 8))
        t.put_pm_bit(38, extract_bit(moc, 7))
        t.put_pm_bit(39, True)  # Reserved
        t.put_pm_bit(40, extract_bit(moc, 6))
        t.put_pm_bit(41, extract_bit(moc, 5))
        t.put_pm_bit(42, extract_bit(moc, 4))
        t.put_pm_bit(43, extract_bit(moc, 3))
        t.put_pm_bit(44, extract_bit(moc, 2))
        t.put_pm_bit(45, extract_bit(moc, 1))
        t.put_pm_bit(46, extract_bit(moc, 0))
        t.put_pm_bit(47, extract_bit(dst_ls, 4))
        t.put_pm_bit(48, extract_bit(dst_ls, 3))
        t.put_pm_bit(49, True)  # Notice
        t.put_pm_bit(50, extract_bit(dst_ls, 2))
        t.put_pm_bit(51, extract_bit(dst_ls, 1))
        t.put_pm_bit(52, extract_bit(dst_ls, 0))
        t.put_pm_bit(53, extract_bit(dst_next, 5))
        t.put_pm_bit(54, extract_bit(dst_next, 4))
        t.put_pm_bit(55, extract_bit(dst_next, 3))
        t.put_pm_bit(56, extract_bit(dst_next, 2))
        t.put_pm_bit(57, extract_bit(dst_next, 1))
        t.put_pm_bit(58, extract_bit(dst_next, 0))
        if len(t.phase) > 59:
            t.put_pm_bit(59, PhaseModulation.ZERO)
        if len(t.phase) > 60:
            t.put_pm_bit(60, PhaseModulation.ZERO)

    def fill_pm_timecode(self, t: "WWVBTimecode") -> None:
        """Fill the phase portion of a timecode object"""
        if 10 <= self.min < 16 or 40 <= self.min < 46:
            self.fill_pm_timecode_extended(t)
        else:
            self.fill_pm_timecode_regular(t)

    def next_minute(
        self, newut1: Optional[int] = None, newls: Optional[bool] = None
    ) -> "WWVBMinute":
        """Return an object representing the next minute"""
        d = self.as_datetime() + datetime.timedelta(minutes=1)
        return self.from_datetime(d, newut1, newls, self)

    def previous_minute(
        self, newut1: Optional[int] = None, newls: Optional[bool] = None
    ) -> "WWVBMinute":
        """Return an object representing the previous minute"""
        d = self.as_datetime() - datetime.timedelta(minutes=1)
        return self.from_datetime(d, newut1, newls, self)

    @classmethod
    def get_dut1_info(  # pylint: disable=unused-argument
        cls: type, year: int, days: int, old_time: "Optional[WWVBMinute]" = None
    ) -> Tuple[int, bool]:
        """Return the DUT1 information for a given day, possibly propagating information from a previous timestamp"""
        if old_time is not None:
            if old_time.minute_length() != 60:
                newls = False
                if old_time.ut1 < 0:
                    newut1 = old_time.ut1 + 1000
                else:
                    newut1 = old_time.ut1 - 1000
            else:
                newls = old_time.ls
                newut1 = old_time.ut1
            return newut1, newls
        return 0, False

    @classmethod
    def fromstring(cls, s: str) -> "WWVBMinute":
        """Construct a WWVBMinute from a string representation created by print_timecodes"""
        if s.startswith("WWVB timecode: "):
            s = s[len("WWVB timecode: ") :]
        d = {}
        for part in s.split():
            k, v = part.split("=")
            if k == "min":
                k = "minute"
            d[k] = int(v)
        year = d.pop("year")
        days = d.pop("days")
        hour = d.pop("hour")
        minute = d.pop("minute")
        dst = d.pop("dst", None)
        ut1 = d.pop("ut1", None)
        ls = d.pop("ls", None)
        d.pop("ly", None)
        if d:
            raise ValueError(f"Invalid options: {d}")
        return cls(year, days, hour, minute, dst, ut1, None if ls is None else bool(ls))

    @classmethod
    def from_datetime(
        cls,
        d: datetime.datetime,
        newut1: Optional[int] = None,
        newls: Optional[bool] = None,
        old_time: Optional["WWVBMinute"] = None,
    ) -> "WWVBMinute":
        """Construct a WWVBMinute from a datetime, possibly specifying ut1/ls data or propagating it from an old time"""
        u = d.utctimetuple()
        if newls is None and newut1 is None:
            newut1, newls = cls.get_dut1_info(u.tm_year, u.tm_yday, old_time)
        return cls(u.tm_year, u.tm_yday, u.tm_hour, u.tm_min, ut1=newut1, ls=newls)

    @classmethod
    def from_timecode_am(  # pylint: disable=too-many-return-statements
        cls, t: "WWVBTimecode"
    ) -> Optional["WWVBMinute"]:
        """Construct a WWVBMinute from a WWVBTimecode"""
        for i in (0, 9, 19, 29, 39, 49, 59):
            if t.am[i] != AmplitudeModulation.MARK:
                return None
        for i in (4, 10, 11, 14, 20, 21, 24, 34, 35, 44, 54):
            if t.am[i] != AmplitudeModulation.ZERO:
                return None
        if t.am[36] == t.am[37]:
            return None
        if t.am[36] != t.am[38]:
            return None
        minute = t.get_am_bcd(1, 2, 3, 5, 6, 7, 8)
        if minute is None:
            return None
        hour = t.get_am_bcd(12, 13, 15, 16, 17, 18)
        if hour is None:
            return None
        days = t.get_am_bcd(22, 23, 25, 26, 27, 28, 30, 31, 32, 33)
        if days is None:
            return None
        abs_ut1 = t.get_am_bcd(40, 41, 42, 43)
        if abs_ut1 is None:
            return None
        abs_ut1 *= 100
        ut1_sign = t.am[38]
        ut1 = abs_ut1 if ut1_sign else -abs_ut1
        year = t.get_am_bcd(45, 46, 47, 48, 50, 51, 52, 53)
        if year is None:
            return None
        ly = bool(t.am[55])
        if days > 366 or (not ly and days > 365):
            return None
        ls = bool(t.am[56])
        dst = require(t.get_am_bcd(57, 58))
        return cls(year, days, hour, minute, dst, ut1, ls, ly)


class WWVBMinuteIERS(WWVBMinute):
    """A WWVBMinute that uses a database of DUT1 information"""

    @classmethod
    def get_dut1_info(
        cls, year: int, days: int, old_time: Optional[WWVBMinute] = None
    ) -> Tuple[int, bool]:
        d = datetime.datetime(year, 1, 1) + datetime.timedelta(days - 1)
        return int(round(get_dut1(d) * 10)) * 100, isls(d)


def bcd_bits(n: int) -> Generator[bool, None, None]:
    """Return the bcd representation of n, starting with the least significant bit"""
    while True:
        d = n % 10
        n = n // 10
        for i in (1, 2, 4, 8):
            yield bool(d & i)


@enum.unique
class AmplitudeModulation(enum.IntEnum):
    """Constants that describe an Amplitude Modulation value"""

    ZERO = 0
    ONE = 1
    MARK = 2
    UNSET = -1


@enum.unique
class PhaseModulation(enum.IntEnum):
    """Constants that describe a Phase Modulation value"""

    ZERO = 0
    ONE = 1
    UNSET = -1


class WWVBTimecode:
    """Represent the amplitude and/or phase signal, usually over 1 minute"""

    am: List[AmplitudeModulation]
    phase: List[PhaseModulation]

    def __init__(self, sz: int) -> None:
        self.am = [AmplitudeModulation.UNSET] * sz  # pylint: disable=invalid-name
        self.phase = [PhaseModulation.UNSET] * sz

    @property
    def data(self) -> List[AmplitudeModulation]:
        """An alias for `self.am`"""
        return self.am

    def get_am_bcd(self, *poslist: int) -> Optional[int]:
        """Convert the bits seq[positions[0]], ... seq[positions[len(positions-1)]] [in MSB order] from BCD to decimal"""
        seq = self.am
        pos = list(poslist)[::-1]
        val = [int(seq[p]) for p in pos]
        while len(val) % 4 != 0:
            val.append(0)
        result = 0
        base = 1
        for i in range(0, len(val), 4):
            digit = 0
            for j in range(4):
                digit += 1 << j if val[i + j] else 0
            if digit > 9:
                return None
            result += digit * base
            base *= 10
        return result

    def put_am_bcd(self, v: int, *poslist: int) -> None:
        """Treating 'poslist' as a sequence of indices, update the AM signal with the value as a BCD number"""
        pos = list(poslist)[::-1]
        for p, b in zip(pos, bcd_bits(v)):
            if b:
                self.am[p] = AmplitudeModulation.ONE
            else:
                self.am[p] = AmplitudeModulation.ZERO

    def put_pm_bit(self, i: int, v: Union[PhaseModulation, int, bool]) -> None:
        """Update a bit of the Phase Modulation signal"""
        self.phase[i] = PhaseModulation(v)

    def put_pm_bin(self, st: int, n: int, v: int) -> None:
        """Update an n-digit binary number in the Phase Modulation signal"""
        for i in range(n):
            self.put_pm_bit(st + i, extract_bit(v, (n - i - 1)))

    def __str__(self) -> str:
        """implement str()"""
        undefined = [
            i for i in range(len(self.am)) if self.am[i] == AmplitudeModulation.UNSET
        ]
        if undefined:
            warnings.warn(f"am{undefined} is unset")

        def convert_one(am: AmplitudeModulation, phase: PhaseModulation) -> str:
            if phase is PhaseModulation.UNSET:
                return ("0", "1", "2", "?")[am]
            if phase:
                return ("⁰", "¹", "²", "¿")[am]
            return ("₀", "₁", "₂", "⸮")[am]

        return "".join(convert_one(i, j) for i, j in zip(self.am, self.phase))

    def __repr__(self) -> str:
        """implement repr()"""
        return "<WWVBTimecode " + str(self) + ">"

    def to_am_string(self, charset: List[str]) -> str:
        """Convert the amplitude signal to a string"""
        return "".join(charset[i] for i in self.am)

    to_string = to_am_string

    def to_pm_string(self, charset: List[str]) -> str:
        """Convert the phase signal to a string"""
        return "".join(charset[i] for i in self.phase)


styles = {
    "default": ["0", "1", "2"],
    "duration": ["2", "5", "8"],
    "cradek": ["0", "1", "-"],
    "bar": ["▟█", "▄█", "▄▟"],
}


# pylint: disable=too-many-arguments
def print_timecodes(
    w: WWVBMinute,
    minutes: int,
    channel: str,
    style: str,
    file: TextIO,
    *,
    all_timecodes: bool = False,
) -> None:
    """Print a range of timecodes with a header.  This header is in a format understood by WWVBMinute.fromstring"""
    channel_text = "" if channel == "amplitude" else f" --channel={channel}"
    style_text = "" if style == "default" else f" --style={style}"
    style_chars = styles.get(style, ["0", "1", "2"])
    first = True
    for _ in range(minutes):
        if first or all_timecodes:
            if not first:
                print(file=file)
            print(f"WWVB timecode: {str(w)}{channel_text}{style_text}", file=file)
        first = False
        pfx = f"{w.year:04d}-{w.days:03d} {w.hour:02d}:{w.min:02d} "
        tc = w.as_timecode()
        if channel in ("amplitude", "both"):
            print(f"{pfx} {tc.to_am_string(style_chars)}", file=file)
            pfx = " " * len(pfx)
        if channel in ("phase", "both"):
            print(f"{pfx} {tc.to_pm_string(style_chars)}", file=file)
        if channel == "both":
            print(file=file)
        w = w.next_minute()
