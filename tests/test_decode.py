#
# This file is part of wav2vec2_stt.
# (c) Copyright 2021 by David Zurow
# Licensed under the AGPL-3.0; see LICENSE file.
#

import os

import pytest

test_model_path = os.path.join(os.path.dirname(__file__), 'model')
test_wav_path = os.path.join(os.path.dirname(__file__), 'test.wav')


@pytest.fixture
def decoder():
    from wav2vec2_stt import Wav2Vec2STT
    return Wav2Vec2STT(test_model_path)

@pytest.fixture
def wav_samples():
    import wave
    wave_file = wave.open(test_wav_path, 'rb')
    data = wave_file.readframes(wave_file.getnframes())
    return data


def test_init(decoder):
    pass

def test_destruct(decoder):
    del decoder

def test_decode(decoder, wav_samples):
    assert decoder.decode(wav_samples).strip().lower() == 'it depends on the context'
