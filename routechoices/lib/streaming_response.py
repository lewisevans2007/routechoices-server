import os
import re
from io import BytesIO
from wsgiref.util import FileWrapper

import magic
from django.http import StreamingHttpResponse

range_re = re.compile(r"bytes\s*=\s*(\d+)\s*-\s*(\d*)", re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, "close"):
            self.filelike.close()

    def __iter__(self):
        return self

    def next(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def StreamingHttpRangeResponse(request, data, **kwargs):
    range_header = request.META.get("HTTP_RANGE", "").strip()
    range_match = range_re.match(range_header)
    size = len(data)
    content_type = kwargs.pop("content_type", None)
    if not content_type:
        content_type = magic.from_buffer(data, mime=True) or "application/octet-stream"
    fileIO = BytesIO(data)

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(
            RangeFileWrapper(fileIO, offset=first_byte, length=length),
            status=206,
            content_type=content_type,
            **kwargs,
        )
        resp["Content-Length"] = str(length)
        resp["Content-Range"] = "bytes %s-%s/%s" % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(
            FileWrapper(fileIO), content_type=content_type, **kwargs
        )
        resp["Content-Length"] = str(size)
    resp["Accept-Ranges"] = "bytes"
    return resp