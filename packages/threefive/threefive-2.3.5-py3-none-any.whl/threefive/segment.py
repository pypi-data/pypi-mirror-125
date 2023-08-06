"""
The threefive.Segment class
"""
import os

import pyaes

from .reader import reader
from .stream import Stream


class Segment:
    """
    The Segment class is used to process
    hls mpegts segments for segment start time
    and SCTE35 cues.
    local and http(s) segments are supported
    aes encoded segments are decrypted.
    Segment.start is the first timestamp found
    in the segment.
    Segment.cues is a list of
    SCTE35 cues found in the segment.

    Example:

        from threefive import Segment

        >>>> uri = "https://example.com/1.ts"
        >>>> seg = Segment(uri)
        >>>> seg.decode()
        >>>> seg.start
        89715.976944
        >>>> [cue.encode() for cue in cues]
        ['/DARAAAAAAAAAP/wAAAAAHpPv/8=',
        '/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=']

        # For aes encrypted files

        >>>> key = "https://example.com/aes.key"
        >>>> IV=0x998C575D24F514AEC84EDC5CABCCDB81
        >>>> uri = "https://example.com/aes-1.ts"

        >>>> seg = Segment(uri,key_uri=key, iv=IV)
        >>>> seg.decode()
        >>>> seg.start
        89715.976944
        >>>> {cue.packet_data.pcr:cue.encode() for cue in seg.cues}

       { 89718.451333: '/DARAAAAAAAAAP/wAAAAAHpPv/8=',
       89730.281789: '/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc='}

    """

    def __init__(self, seg_uri, key_uri=None, iv=None):
        self.seg_uri = seg_uri
        self.key_uri = key_uri
        self.key = None
        self.iv = None
        self.cues = []
        self.start = None
        self.tmp = None
        if iv:
            self.iv = int.to_bytes(int(iv), 16, byteorder="big")
        if self.key_uri:
            self._aes_get_key()
            self._aes_decrypt()

    def __repr__(self):
        return str(self.__dict__)

    def _mk_tmp(self):
        self.tmp = "tf-"
        self.tmp += self.seg_uri.rsplit("/", 1)[-1]

    def _aes_get_key(self):
        with reader(self.key_uri) as quay:
            self.key = quay.read()

    def _aes_decrypt(self):
        mode = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        self._mk_tmp()
        with open(self.tmp, "wb") as outfile:
            with reader(self.seg_uri) as infile:
                pyaes.decrypt_stream(mode, infile, outfile)
            self.seg_uri = self.tmp

    def add_cue(self, cue):
        """
        add_cue is passed to a Stream instance
        to collect SCTE35 cues.
        """
        self.cues.append(cue)

    def decode(self):
        """
        decode a mpegts hls segment for start time
        and scte35 cues.
        """
        with reader(self.seg_uri) as seg:
            strm = Stream(seg)
            # strm.show_start = False
            strm.decode(func=self.add_cue)
            self.start = strm.start
            if self.tmp:
                os.unlink(self.tmp)
