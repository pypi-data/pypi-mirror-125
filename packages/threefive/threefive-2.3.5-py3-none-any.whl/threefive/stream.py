"""
Mpeg-TS Stream parsing class Stream
"""
import sys
from functools import partial
from .cue import Cue
from .packetdata import PacketData
from .reader import reader


def no_op(cue):
    """
    no_op is just a dummy func to pass to Stream.decode()
    to suppress output.
    """
    return cue


def show_cue(cue):
    """
    default function call for Stream.decode
    when a SCTE-35 packet is found.
    """
    cue.show()


def show_cue_stderr(cue):
    """
    print cue data to sys.stderr
    for Stream.decode_proxy
    """
    cue.to_stderr()


class ProgramInfo:
    """
    ProgramInfo is a class to
    hold Program information
    for use with Stream.show()
    """

    def __init__(self):
        self.pid = None
        self.provider = b""
        self.service = b""
        self.streams = {}  # pid to stream_type mapping

    def show(self):
        """
        show print the Program Infomation
        in a familiar format.
        """
        serv = self.service.decode(errors="ignore")
        prov = self.provider.decode(errors="ignore")
        print(f"\n    Service: { serv}\n    Provider: {prov}\n")
        for k, vee in self.streams.items():
            print(f"    Stream:  pid:{k}[{hex(k)}]\ttype:{vee}")
        print()


class Stream:
    """
    Stream class for parsing MPEG-TS data.
    """

    _PACKET_SIZE = 188
    _SDT_PID = 0x0011  # Stream Descriptor Table Pid
    _PAT_PID = 0x00  # Program Association Pid

    def __init__(self, tsdata, show_null=True):
        """
        tsdata is an file or http/https url
        set show_null=False to exclude Splice Nulls

        Use like...

        from threefive import Stream
        strm = Stream("vid.ts",show_null=False)
        strm.decode()

        """
        if isinstance(tsdata, str):
            self._tsdata = reader(tsdata)
        else:
            self._tsdata = tsdata
        self.show_null = show_null
        self.start = {}
        self.info = None
        self.the_program = None
        self._pids = {"pcr": set(), "tables": set(), "scte35": set()}
        self._pids["tables"].add(self._PAT_PID)
        self._pids["tables"].add(self._SDT_PID)
        self._pid_prgm = {}
        self._prgm_pcr = {}
        self._prgm_pts = {}
        self._prgm = {}
        self.the_cue = None
        self._partial = {}
        self._last = {}

    def __repr__(self):
        return str(self.__dict__)

    def _find_start(self):
        sync_byte = 0x47
        while self._tsdata:
            one = self._tsdata.read(1)
            if not one:
                return False
            if one[0] == sync_byte:
                if self._tsdata.read(self._PACKET_SIZE - 1):
                    return True
        return False

    def decode(self, func=show_cue):
        """
        Stream.decode reads self.tsdata to find SCTE35 packets.
        func can be set to a custom function that accepts
        a threefive.Cue instance as it's only argument.
        """
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                cue = self._parse(pkt)
                if cue:
                    if not func:
                        return cue
                    func(cue)
        self._tsdata.close()

        return None

    def _mk_pkts(self, chunk):
        return [
            self._parse(chunk[i : i + self._PACKET_SIZE])
            for i in range(0, len(chunk), self._PACKET_SIZE)
        ]

    def decode_fu(self, func=show_cue):
        """
        Stream.decode_fu decodes
        1880 packets at a time.
        """
        pkts = 1880
        if self._find_start():
            for chunk in iter(
                partial(self._tsdata.read, (self._PACKET_SIZE * pkts)), b""
            ):
                for cue in self._mk_pkts(chunk):
                    if cue:
                        func(cue)
        self._tsdata.close()

    def decode_next(self):
        """
        Stream.decode_next returns the next
        SCTE35 cue as a threefive.Cue instance.
        """
        cue = self.decode(func=False)
        if cue:
            return cue
        return None

    def decode_program(self, the_program, func=show_cue):
        """
        Stream.decode_program limits SCTE35 parsing
        to a specific MPEGTS program.
        """
        self.the_program = the_program
        return self.decode(func)

    def decode_proxy(self, func=show_cue_stderr):
        """
        Stream.decode_proxy writes all ts packets are written to stdout
        for piping into another program like mplayer.
        SCTE-35 cues are printed to stderr.
        """
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                cue = self._parse(pkt)
                if cue:
                    func(cue)
                sys.stdout.buffer.write(pkt)
        self._tsdata.close()

    def strip_scte35(self, func=show_cue_stderr):
        """
        Stream.strip_scte35 works just likle Stream.decode_proxy,
        MPEGTS packets, ( Except the SCTE-35 packets) ,
        are written to stdout after being parsed.
        SCTE-35 cues are printed to stderr.
        """
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                cue = self._parse(pkt)
                if cue:
                    func(cue)
                else:
                    sys.stdout.buffer.write(pkt)
        self._tsdata.close()

    def show(self):
        """
        displays streams that will be
        parsed for SCTE-35.
        """
        self.info = True
        self.decode(func=False)
        for k, vee in self._prgm.items():
            print(f"Program: {k}")
            vee.show()

    def decode_start_time(self):
        """
        displays streams that will be
        parsed for SCTE-35.
        """
        self.decode(func=no_op)
        return self.start.popitem()[1]

    def _mk_packet_data(self, pid):
        prgm = self._pid_prgm[pid]
        pdata = PacketData(pid, prgm)
        pdata.mk_pcr(self._prgm_pcr)
        pdata.mk_pts(self._prgm_pts)
        return pdata

    @staticmethod
    def _split_by_idx(payload, marker):
        try:
            return payload[payload.index(marker) :]
        except (LookupError, TypeError, ValueError):
            return False

    @staticmethod
    def _parse_payload(pkt):
        head_size = 4
        afc = (pkt[3] >> 5) & 1
        if afc:
            afl = pkt[4]
            head_size += afl + 1  # +1 for afl byte
        return pkt[head_size:]

    @staticmethod
    def _parse_length(byte1, byte2):
        """
        parse a 12 bit length value
        """
        return ((byte1 & 0xF) << 8) | byte2

    @staticmethod
    def _parse_pid(byte1, byte2):
        """
        parse a 13 bit pid value
        """
        return (byte1 << 8 | byte2) & 0x01FFF

    @staticmethod
    def _parse_program(byte1, byte2):
        """
        parse a 16 bit program number value
        """
        return (byte1 << 8) | byte2

    @staticmethod
    def _parse_pusi(byte1):
        """
        used to determine if pts data is available.
        """
        return (byte1 >> 6) & 1

    def _parse_pts(self, pkt, pid):
        """
        parse pts and store by program key
        in the dict Stream._pid_pts
        """
        if self._parse_pusi(pkt[1]):
            if pkt[11] & 128:
                pts = ((pkt[13] >> 1) & 7) << 30
                pts |= pkt[14] << 22
                pts |= (pkt[15] >> 1) << 15
                pts |= pkt[16] << 7
                pts |= pkt[17] >> 1
                prgm = self._pid_prgm[pid]
                self._prgm_pts[prgm] = pts

    def _parse_pcr(self, pkt, pid):
        """
        Parse PCR base and ext from
        PCR PID packets
        """
        if (pkt[3] >> 5) & 1:
            if (pkt[5] >> 4) & 1:
                pcr = pkt[6] << 25
                pcr |= pkt[7] << 17
                pcr |= pkt[8] << 9
                pcr |= pkt[9] << 1
                pcr |= pkt[10] >> 7
                prgm = self._pid_prgm[pid]
                self._prgm_pcr[prgm] = pcr
                if prgm not in self.start:
                    self.start[prgm] = pcr

    def _parse_tables(self, pkt, pid):
        """
        _parse_tables parse for
        PAT, PMT,  and SDT tables
        based on pid of the pkt
        """
        payload = self._parse_payload(pkt)
        if not self._chk_last(payload, pid):
            if pid == self._PAT_PID:
                self._program_association_table(payload)
            elif pid == self._SDT_PID:
                if self.info:
                    self._stream_descriptor_table(payload)
            else:
                self._program_map_table(payload, pid)

    def _parse(self, pkt):
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid in self._pids["tables"]:
            return self._parse_tables(pkt, pid)
        if pid in self._pids["pcr"]:
            return self._parse_pcr(pkt, pid)
        if pid in self._pids["scte35"]:
            return self._parse_scte35(pkt, pid)
        if pid in self._pid_prgm:
            return self._parse_pts(pkt, pid)
        return None

    def _chk_partial(self, payload, pid):
        if pid in self._partial:
            payload = self._partial.pop(pid) + payload
        return payload

    def _chk_last(self, payload, pid):
        if pid in self._last:
            return payload == self._last[pid]
        self._last[pid] = payload
        return False

    def _chk_scte35_payload(self, pkt, pid):
        payload = self._parse_payload(pkt)
        if not self.the_cue:
            payload = self._split_by_idx(payload, b"\xfc0")
            if not payload:
                self._pids["scte35"].remove(pid)
                return False
            if payload[13] == self.show_null:
                return False
            self._parse_cue(payload, pid)
        else:
            self.the_cue.bites = self._chk_partial(payload, pid)
        # + 3 for the bytes before section starts
        if (self.the_cue.info_section.section_length + 3) > len(self.the_cue.bites):
            self._partial[pid] = payload
            return False
        self.the_cue.bites = payload[: self.the_cue.info_section.section_length + 3]
        return True

    def _parse_cue(self, payload, pid):
        packet_data = None
        packet_data = self._mk_packet_data(pid)
        self.the_cue = Cue(payload, packet_data)
        self.the_cue.info_section.decode(payload)
        self.the_cue.bites = payload

    def _parse_scte35(self, pkt, pid):
        """
        parse a scte35 cue from one or more packets
        """
        if not self._chk_scte35_payload(pkt, pid):
            return None
        if not self.the_cue.decode():
            self._pids["scte35"].remove(pid)
            return None
        cue, self.the_cue = self.the_cue, None
        return cue

    def _stream_descriptor_table(self, payload):
        payload = self._chk_partial(payload, self._SDT_PID)
        section_length = self._parse_length(payload[2], payload[3])
        if section_length + 3 > len(payload):
            self._partial[self._SDT_PID] = payload
            return None
        idx = 12
        while idx < section_length + 3:
            service_id = self._parse_program(payload[idx], payload[idx + 1])
            idx += 3
            dloop_len = self._parse_length(payload[idx], payload[idx + 1])
            idx += 2
            i = 0
            while i < dloop_len:
                if payload[idx] == 0x48:
                    i += 3
                    spnl = payload[idx + i]
                    i += 1
                    service_provider_name = payload[idx + i : idx + i + spnl]
                    i += spnl
                    snl = payload[idx + i]
                    i += 1
                    service_name = payload[idx + i : idx + i + snl]
                    i += snl
                    if service_id not in self._prgm:
                        self._prgm[service_id] = ProgramInfo()
                    pinfo = self._prgm[service_id]
                    pinfo.provider = service_provider_name
                    pinfo.service = service_name
                i = dloop_len
                idx += i

    def _program_association_table(self, payload):
        """
        parse program association table ( pid 0 )
        for program to pmt_pid mappings.
        """
        pid = 0
        payload = self._chk_partial(payload, pid)
        section_length = self._parse_length(payload[2], payload[3])
        if section_length + 3 > len(payload):
            self._partial[pid] = payload
            return None
        section_length -= 5  # payload bytes 4,5,6,7,8
        idx = 9
        chunk_size = 4
        while section_length > 4:  #  4 bytes for crc
            program_number = self._parse_program(payload[idx], payload[idx + 1])
            if program_number > 0:
                pmt_pid = self._parse_pid(payload[idx + 2], payload[idx + 3])
                self._pids["tables"].add(pmt_pid)
            section_length -= chunk_size
            idx += chunk_size

    def _program_map_table(self, payload, pid):
        """
        parse program maps for streams
        """
        payload = self._chk_partial(payload, pid)
        payload = self._split_by_idx(payload, b"\x02")
        if not payload:
            return
        sectioninfolen = self._parse_length(payload[1], payload[2])
        if sectioninfolen + 3 > len(payload):
            self._partial[pid] = payload
            return
        program_number = self._parse_program(payload[3], payload[4])
        if self.the_program and (program_number != self.the_program):
            return
        pcr_pid = self._parse_pid(payload[8], payload[9])
        if program_number not in self._prgm:
            pinfo = ProgramInfo()
            pinfo.pid = pid
            self._prgm[program_number] = pinfo
        self._pids["pcr"].add(pcr_pid)
        proginfolen = self._parse_length(payload[10], payload[11])
        idx = 12
        idx += proginfolen
        si_len = sectioninfolen - 9
        si_len -= proginfolen
        self._parse_program_streams(si_len, payload, idx, program_number)

    def _parse_program_streams(self, si_len, payload, idx, program_number):
        """
        parse the elementary streams
        from a program
        """
        # 5 bytes for stream_type info
        chunk_size = 5
        end_idx = (idx + si_len) - chunk_size
        while idx < end_idx:
            stream_type, pid, ei_len = self._parse_stream_type(payload, idx)
            if self.info:
                pinfo = self._prgm[program_number]
                pinfo.streams[pid] = stream_type
            idx += chunk_size
            idx += ei_len
            self._pid_prgm[pid] = program_number
            self._chk_pid_stream_type(pid, stream_type)

    def _parse_stream_type(self, payload, idx):
        """
        extract stream pid and type
        """
        stream_type = hex(payload[idx])
        el_pid = self._parse_pid(payload[idx + 1], payload[idx + 2])
        ei_len = self._parse_length(payload[idx + 3], payload[idx + 4])
        return stream_type, el_pid, ei_len

    def _chk_pid_stream_type(self, pid, stream_type):
        """
        if stream_type is 0x06 or 0x86
        add it to self._scte35_pids.
        """
        if stream_type in ["0x6", "0x86"]:
            self._pids["scte35"].add(pid)
