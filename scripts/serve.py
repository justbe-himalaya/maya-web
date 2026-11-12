#!/usr/bin/env python3
"""로컬 미리보기 서버: python3 scripts/serve.py [port]  (기본 8765, 폴더 루트에서 실행)

python3 -m http.server는 Range 요청을 지원하지 않아 iPhone Safari에서 히어로 영상이 재생되지 않는다.
GitHub Pages처럼 206 Partial Content로 응답해 주는 최소 서버.
"""
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class RangeHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        rng = self.headers.get('Range')
        path = self.translate_path(self.path)
        if not rng or not os.path.isfile(path):
            return super().send_head()

        m = re.match(r'bytes=(\d*)-(\d*)$', rng.strip())
        size = os.path.getsize(path)
        if not m or (not m.group(1) and not m.group(2)):
            return super().send_head()
        if m.group(1):
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else size - 1
        else:  # bytes=-N : 마지막 N바이트
            start = max(0, size - int(m.group(2)))
            end = size - 1
        end = min(end, size - 1)
        if start > end:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.end_headers()
            return None

        f = open(path, 'rb')
        f.seek(start)
        self._remaining = end - start + 1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(self._remaining))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        remaining = getattr(self, '_remaining', None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        self._remaining = None
        while remaining > 0:
            chunk = source.read(min(64 * 1024, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)

    def end_headers(self):
        if self.command in ('GET', 'HEAD') and not self.headers.get('Range'):
            self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f'Serving on http://0.0.0.0:{port}')
    ThreadingHTTPServer(('', port), RangeHandler).serve_forever()
