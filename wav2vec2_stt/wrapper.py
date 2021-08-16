#
# This file is part of wav2vec2_stt.
# (c) Copyright 2021 by David Zurow
# Licensed under the AGPL-3.0; see LICENSE file.
#

import os, re, sys

from cffi import FFI
import numpy as np

if sys.platform.startswith('win'): _platform = 'windows'
elif sys.platform.startswith('linux'): _platform = 'linux'
elif sys.platform.startswith('darwin'): _platform = 'macos'
else: raise Exception("unknown sys.platform")

_ffi = FFI()
_library_directory_path = os.path.dirname(os.path.abspath(__file__))
_library_binary_path = os.path.join(_library_directory_path,
    dict(windows='wav2vec2_stt_lib.dll', linux='libwav2vec2_stt_lib.so', macos='libwav2vec2_stt_lib.dylib')[_platform])
_c_source_ignore_regex = re.compile(r'(\b(extern|WAV2VEC2_STT_API)\b)|("C")|(//.*$)', re.MULTILINE)  # Pattern for extraneous stuff to be removed

def encode(text):
    """ For C interop: encode unicode text -> binary utf-8. """
    return text.encode('utf-8')
def decode(binary):
    """ For C interop: decode binary utf-8 -> unicode text. """
    return binary.decode('utf-8')

class FFIObject(object):

    def __init__(self):
        self.init_ffi()

    @classmethod
    def init_ffi(cls):
        cls._lib = _ffi.init_once(cls._init_ffi, cls.__name__ + '._init_ffi')

    @classmethod
    def _init_ffi(cls):
        _ffi.cdef(_c_source_ignore_regex.sub(' ', cls._library_header_text))
        return _ffi.dlopen(_library_binary_path)

class Wav2Vec2STT(FFIObject):

    _library_header_text = """
        WAV2VEC2_STT_API void *wav2vec2_stt__construct(const char *model_dirname);
        WAV2VEC2_STT_API bool wav2vec2_stt__destruct(void *model_vp);
        WAV2VEC2_STT_API bool wav2vec2_stt__decode(void *model_vp, float *wav_samples, int32_t wav_samples_len, char *text, int32_t text_max_len);
    """

    def __init__(self, model_dirname):
        super().__init__()
        if not os.path.exists(model_dirname):
            raise FileNotFoundError("model directory '%s' does not exist" % model_dirname)
        if not os.path.exists(os.path.join(model_dirname, 'encoder.zip')):
            raise FileNotFoundError("model directory '%s' does not contain 'encoder.zip'" % model_dirname)
        if not os.path.exists(os.path.join(model_dirname, 'decoder.zip')):
            raise FileNotFoundError("model directory '%s' does not contain 'decoder.zip'" % model_dirname)
        result = self._lib.wav2vec2_stt__construct(encode(model_dirname))
        if result == _ffi.NULL:
            raise Exception("wav2vec2_stt__construct failed")
        self._model = result

    def __del__(self):
        if hasattr(self, '_model'):
            result = self._lib.wav2vec2_stt__destruct(self._model)
            if not result:
                raise Exception("wav2vec2_stt__destruct failed")

    def decode(self, wav_samples, text_max_len=1024):
        if not isinstance(wav_samples, np.ndarray): wav_samples = np.frombuffer(wav_samples, np.int16)
        wav_samples = wav_samples.astype(np.float32)
        wav_samples_char = _ffi.from_buffer(wav_samples)
        wav_samples_float = _ffi.cast('float *', wav_samples_char)
        text_p = _ffi.new('char[]', text_max_len)

        result = self._lib.wav2vec2_stt__decode(self._model, wav_samples_float, len(wav_samples), text_p, text_max_len)
        if not result:
            raise Exception("wav2vec2_stt__decode failed")

        text = decode(_ffi.string(text_p))
        if len(text) >= (text_max_len - 1):
            raise Exception("text may be too long")
        return text
